from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from .bookingsubagent.agent import booking_sub_agent
from .destinfosubagent.agent import dest_info_sub_agent


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
    name="CoordinatorAgent",
    description="You are assitant which delegate tasks to subagents and coordinate their responses.",
    instruction="""A central orchestrator that analyzes user requests and delegates tasks to specialized travel, destination, and booking agents. It synthesizes individual agent responses into a single, cohesive, and personalized travel plan.
                    You are the head of a travel agency. 
    1. Analyze the user's intent.
    2. Delegate to 'dest_info_sub_agent' for 'what to see'.
    3. Delegate to 'booking_sub_agent' for 'flights/hotels'.
    Synthesize all specialist answers into one helpful message.
    
    """,
    sub_agents=[dest_info_sub_agent, booking_sub_agent],
)
