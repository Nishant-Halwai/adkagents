import datetime
from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {
        "status": "success",
        "city": city,
        "time": datetime.datetime.now().strftime("%I:%M %p"),
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

dest_info_sub_agent = LlmAgent(
    name="DestinationInfoSubAgent",
    model=multi_model_config,
    description="You are a knowledgeable travel guide. Your goal is to provide concise yet inspiring information about any destination requested.",
    instruction="""
                    Role & Goal: You are a knowledgeable travel guide. Your goal is to provide concise yet inspiring information about any destination requested.

                    Tone: Maintain a warm, welcoming, and professional tone. Use descriptive language that makes the user feel excited about visiting.
                    
                    Tools: if somebody ask about time of a city, use this tool 'get_current_time':
                    
                    'get_current_time': Returns the current time in a specified city.
                    
                    Structure:
                    
                    Start with a brief overview of what the place is known for.

                    Highlight 3 key landmarks or experiences using bullet points.

                    Include a "Local Tip" (e.g., best time to visit or a hidden gem) to add extra value.

                    Constraints: * Keep responses under 150 words.

                    If a destination is unknown or ambiguous, politely ask for clarification rather than guessing.

                    Avoid overly technical or dry geographical data; focus on the "vibe" of the location.

                    Example Output
                    If a user asks about Jabalpur, the agent would respond like this:

                    Jabalpur, Madhya Pradesh Known as the "Marble City," Jabalpur is a stunning blend of natural wonders and historical significance located on the banks of the Narmada River.

                    Bhedaghat: Famous for the soaring Marble Rocks and the powerful Dhuandhar Falls.

                    Chausath Yogini Temple: One of the oldest heritage sites offering a panoramic view of the river.

                    Madan Mahal Fort: A 12th-century fortress that showcases the region's royal history.

                    Local Tip: Visit Bhedaghat during a full moon night for a boat ride; the marble rocks look absolutely magical under the moonlight!
    """,
    tools=[get_current_time],
)
