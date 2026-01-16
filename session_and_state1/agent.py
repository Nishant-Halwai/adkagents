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

# import os
from dotenv import load_dotenv

load_dotenv()


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
    instruction="You are a helpful assistant that help the user of any user query"
    + " and if user ask about weather of city then Tells the weather of city. Use the 'get_weather' tool for this purpose"
    + " If the user ask about current time of city then use get_current_time tool to tell current time of city",
    tools=[get_weather, get_current_time],
)

# llm = LiteLlm(os.getenv("GOOGLE_API_KEY"))

warnings.filterwarnings("ignore")
# warnings.("ADK_SUPPRESS_GEMINI_LITELLM_WARNINGS=true")
logging.basicConfig(level=logging.ERROR)

# session = asyncio.run(init_session(APP_NAME, USER_ID, SESSION_ID))

session_service = InMemorySessionService()

# # Runner connect the Agent to the session
# APP_NAME = "weather_app"
# runner = Runner(agent=root_agent, session_service=session_service, app_name=APP_NAME)


# async def main():
#     USER_ID = "user_1"
#     SESSION_ID = "session_01"

#     while True:
#         user_input = input("User: ")
#         if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
#             break

#         message = types.Content(role="user", parts=[types.Part(text=user_input)])

#     async for event in runner.run_async(
#         user_id=USER_ID, session_id=SESSION_ID, message=message
#     ):
#         if event.is_final_response():
#             print("Agent: ", event.response.text)


APP_NAME = "weather_app"
USER_ID = "user_1"
SESSION_ID = "session_01"


async def init_session(
    app_name: str, user_id: str, session_id: str
) -> InMemorySessionService:
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )

    # print(f"Application Name {app_name}")
    # print(f"User ID {user_id}")
    # print(f"Session ID {session_id}")

    return session


runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)

# print(f"Runner created for agent '{runner.agent.name}'.")

if __name__ == "__main__":
    session = asyncio.run(init_session(APP_NAME, USER_ID, SESSION_ID))
    # print(f"Manual session test complete for session: {session.session_id}")

# if __name__ == "__main__":
#     asyncio.run(main())
