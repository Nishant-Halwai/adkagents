import datetime
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import DatabaseSessionService
from google.adk.tools import ToolContext
from google.adk.runners import Runner

# --- 1. PERSISTENCE CONFIG ---
# We use aiosqlite for the required async database engine
DB_URL = "sqlite+aiosqlite:///./Persistent/adk_persistence.db"
session_service = DatabaseSessionService(db_url=DB_URL)


# --- 2. TOOLS WITH USER-SCOPE STATE ---
def update_user_profile(tool_context: ToolContext, key: str, value: str) -> str:
    """
    Save user information permanently.
    Using the 'user:' prefix ensures it persists across NEW sessions.
    """
    # Writing to tool_context.state with 'user:' prefix triggers cross-session persistence
    tool_context.state[f"user:{key}"] = value
    return f"Successfully updated your {key} to {value}. I will remember this in our future chats!"


def view_my_profile(tool_context: ToolContext) -> str:
    """Retrieves and displays everything stored in the user's persistent memory."""
    # Convert the State object to a standard Python dictionary first
    current_state = tool_context.state.to_dict()

    # Filter for only keys that start with 'user:'
    user_data = {
        k.replace("user:", ""): v
        for k, v in current_state.items()
        if k.startswith("user:")
    }

    if not user_data:
        return "Your profile is currently empty. I don't know your name or city yet."

    summary = "\n".join([f"- {k.capitalize()}: {v}" for k, v in user_data.items()])
    return f"Here is what I remember about you:\n{summary}"


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {
        "status": "success",
        "city": city,
        "time": datetime.datetime.now().strftime("%I:%M %p"),
    }


def get_weather(city: str) -> dict:
    """Retrieve the current weather of the specified city."""
    weather_db = {"delhi": "foggy winter", "tokyo": "mist"}
    report = weather_db.get(city.lower().replace(" ", ""), "City not found")
    return {
        "status": "success" if report != "City not found" else "failed",
        "report": report,
    }


# --- 3. MODEL & AGENT CONFIG ---
# Ensure your GOOGLE_API_KEY is in your environment or .env file
# model_config = LiteLlm(model="gemini/gemini-2.0-flash")
multi_model_config = LiteLlm(
    model="gemini/gemini-2.5-flash",
    fallbacks=[
        "gemini/gemini-2.5-pro",
        "gemini/gemini-2.5-flash-lite",
        "gemini/gemini-3-flash-preview",
        "gemini/gemini-3-pro-preview",
        "openai/gpt-4o-mini",
    ],
    num_retries=2,
)

# Note: We use '?' in the template variables to prevent crashes if the keys are empty
root_agent = Agent(
    model=multi_model_config,
    name="PersistentAgent",
    description="An agent that remembers user details across sessions using SQLite.",
    instruction="""You are a helpful assistant.
    
    1. Greeting: If you know the user's name ({user:name?}), greet them by name. 
       Otherwise, greet them as 'Guest' and ask for their name.
    2. Context: If you know their favorite city ({user:favorite_city?}), 
       mention it when discussing weather or time.
    3. Use 'view_my_profile' if the user asks 'What do you know about me?' or 'Show my profile' etc.
    4. Memory: Whenever the user gives you personal details (name, city, email), 
       ALWAYS use the 'update_user_profile' tool to save them.
    5. Current Data: Use 'get_weather' and 'get_current_time' for city-related queries.""",
    tools=[view_my_profile, update_user_profile, get_weather, get_current_time],
)

runner = Runner(
    agent=root_agent,
    app_name="persistentapp",
    session_service=session_service,
)
