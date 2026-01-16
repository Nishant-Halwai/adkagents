import datetime
import warnings
import logging
import asyncio

# Google ADK packages
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents.llm_agent import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.tools.tool_context import ToolContext

# import os
from dotenv import load_dotenv

load_dotenv()


def update_user_profile(tool_context: ToolContext, key: str, value: str) -> str:
    """Save permanently user profile information like name, email, phone number and favorite city."""
    # Prefix 'user': make it presist across sessions for this user
    tool_context.state["user"][key] = value
    return f"User profile updated successfully. {key}: {value}"


# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {
        "status": "success",
        "city": city,
        "time": datetime.datetime.now().strftime("%I:%M %p"),
    }


def get_weather(city: str) -> dict:
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

    print(f"- Tool - get_weather called for the city {city}-")

    specified_city = city.lower().replace(" ", "")

    weather_db = {
        "delhi": {"status": "success", "report": "foggy winter"},
        "tokyo": {"status": "success", "report": "mist"},
    }

    if specified_city in weather_db:
        return weather_db[specified_city]
    else:
        return {
            "status": "failed",
            "report": "City not found in the database",
        }


# llm = LiteLlm(os.getenv("GOOGLE_API_KEY"))

multi_model_config = LiteLlm(
    model="gemini/gemini-2.5-flash",
    fallbacks=["openai/gpt-4o-mini", "anthropic/claude-3-haiku"],
    num_retries=2,
)


root_agent = Agent(
    model=multi_model_config,
    name="root_agent",
    description=(
        "You are a helpful assistant that help the user of any user query and give weather information, give current time of city"
    ),
    instruction="""You are a helpful assistant that help the user of any user query
                User profile:
                - Name: {user: name}
                - Email: {user: email}
                - Phone Number: {user: phone_number}
                - Favorite City: {user: favorite_city}
                
                1. If you know the user's name, use it.
                2. If you know the user's favorite city, use it.
                3. User 'update_user_profile' tool to update user profile and remember it..
                4. You also remember the conversation history, naturally. 
                5. If user ask about weather of city then Tells the weather of city. Use the 'get_weather' tool for this purpose,
                6. If user ask about current time of city then use 'get_current_time' tool to tell current time of city.""",
    tools=[update_user_profile, get_weather, get_current_time],
)

# llm = LiteLlm(os.getenv("GOOGLE_API_KEY"))

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)


session_service = InMemorySessionService()

# # Runner connect the Agent to the session
runner = Runner(
    agent=root_agent, session_service=session_service, app_name="weather_app"
)
