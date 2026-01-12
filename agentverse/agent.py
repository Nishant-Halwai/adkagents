from google.adk.agents.llm_agent import Agent
import datetime
# from google.adk.tools import google_search


# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {
        "status": "success",
        "city": city,
        "time": datetime.datetime.now().strftime("%I:%M %p"),
    }


root_agent = Agent(
    model="gemini-3-flash-preview",
    name="root_agent",
    description="you are assistant answer the question of user and Tells the current time in a specified city.",
    instruction="You are a helpful assistant that help the user and Tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time],
)
