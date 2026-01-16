# import os
from dotenv import load_dotenv
import uuid
import datetime
import asyncio

# google adk
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import DatabaseSessionService, InMemorySessionService
from google.adk.tools import ToolContext
from google.adk.runners import Runner
from google.genai import types
# from google.adk.genai import genai


load_dotenv()

APP_NAME = "PersistentApp"
# USER_ID = str(uuid.uuid4())
USER_ID = "user01"
SESSION_ID = "session01"


# def update_user_profile(tool_context: ToolContext, key: str, value: str) -> str:
#     """Save permanently user profile information like name, email, phone number and favorite city."""
#     # Prefix 'user': make it presist across sessions for this user
#     tool_context.state[f"user:{key}"] = value
#     return f"User profile updated successfully. {key}: {value}"


def update_user_profile(tool_context: ToolContext, key: str, value: str) -> str:
    """Save permanently user profile information across ALL sessions."""
    # Prefix 'user:' is the magic key for cross-session persistence
    tool_context.state[f"user:{key}"] = value
    return f"I've updated your profile. I will remember your {key} in future chats too."


# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {
        "status": "success",
        "city": city,
        "time": datetime.datetime.now().strftime("%I:%M %p"),
    }


def get_weather(tool_context: ToolContext, city: str = None) -> dict:
    """
    Retrieve the current weather of the specified city

    Args:
        city (str): The name of the city for which to retrieve the weather

    Returns:
        dict: A dictionary containing the weather information for specified city
              include a status key either success or failed
              If status as success then include report key as weather message
              If status as failed then include report key as error_message
    """
    target_city = city or tool_context.state.get("user:favorite_city")
    # print(f"- Tool - get_weather called for the city {city}-")

    specified_city = target_city.lower().replace(" ", "")

    weather_db = {
        "delhi": {"status": "success", "report": "foggy winter"},
        "tokyo": {"status": "success", "report": "mist"},
    }

    if specified_city in weather_db:
        return weather_db[specified_city]
    else:
        return {
            "status": "failed",
            "report": "I don't know the name of which city are you talking about",
        }


# llm = LiteLlm(os.getenv("GOOGLE_API_KEY"))

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


root_agent = Agent(
    model=multi_model_config,
    name="root_agent",
    description=(
        " you are help full assistant that answer of question and give weather information, give current time of city"
    ),
    instruction="""You are a helpful assistant. 
               Hello {user:name|Guest}! 
               I see your favorite city is {user:favorite_city|not set yet}.
               
               If the name is 'Guest', ask the user for their name and 
               update it using 'update_user_profile'.
               """,
    tools=[update_user_profile],
)

# session
# session_service = InMemorySessionService()
# --- 2. CONFIG & DATABASE ---
# SQLite connection string: 'sqlite:///./filename.db'
# This creates 'adk_persistence.db' in your local project folder
DB_URL = "sqlite+aiosqlite:///./Persistent/adk_persistence.db"
session_service = DatabaseSessionService(db_url=DB_URL)

# create session


# async def initialize_session(
#     app_name: str, user_id: str, session_id: str
# ) -> InMemorySessionService:
#     session = await session_service.create_session(
#         app_name=app_name, user_id=user_id, session_id=session_id
#     )
#     return session


async def initialize_session(app_name, user_id, session_id):
    # This ensures the keys exist so the parser doesn't crash
    initial_state = {"user:name": "Guest", "user:favorite_city": "Unknown"}

    session = await session_service.get_or_create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )

    # Fill in missing keys only if they don't already exist
    for key, value in initial_state.items():
        if key not in session.state:
            session.state[key] = value

    return session


try:
    session = asyncio.run(initialize_session(APP_NAME, USER_ID, SESSION_ID))
except Exception as e:
    print(str(e))

# runner
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


# def call_agent(query):
#     content = types.Content(role="user", parts=[types.Part(text=query)])
#     events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
#     for event in events:
#         if event.is_final_response():
#             print(event.content.parts[0].text)


# while True:
#     user_inputs = input("User: ")
#     for user_input in user_inputs.split():
#         if user_input == "exit" or user_input == "quit" or user_input == "bye":
#             break
#     call_agent(user_input)

# if __name__ == "__main__":
#     asyncio.run(main())
# while True:
#     user_input = input("User: ")
#     response = await runner.run(user_input)
#     print("Agent: ", response)

# Agent
# root_agent = Agent(
#     name=APP_NAME,
#     Model="gpt-4o",
#     description="A persistent agent that can remember previous interactions.",
#     user_id=USER_ID,
#     session_id=SESSION_ID,
#     tools=[
#         ToolContext(
#             name="Search",
#             description="Search for information on the web.",
#             func=genai.search,
#         )
#     ],
# )
