from google.adk.agents.llm_agent import Agent
import datetime
import warnings
import logging
from google.adk.models.lite_llm import LiteLlm
# from google.adk.models.llm_agent import LlmAgent

# import os
from dotenv import load_dotenv

load_dotenv()
# import google.generativeai as genai
# from google.adk.tools import google_search


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
logging.basicConfig(level=logging.ERROR)
