import os
from dotenv import load_dotenv

import litellm
from litellm import completion


load_dotenv()

# print(os.getenv("GOOGLE_API_KEY"))
# print(os.getenv("OPENAI_API_KEY"))

print("Google_API_KEY exists" if os.getenv("Google_API_KEY") else "Key not exists")
print("OpenAI_API_KEY exists" if os.getenv("OpenAI_API_KEY") else "Key not exists")


def smart_query(user_prompt):
    """
    Attempts to call Gemini first.
    If a 429 (Rate Limit) or any error occurs, it rotates through fallbacks.
    """
    try:
        response = completion(
            model="gemini/gemini-2.5-flash-preview",
            messages=[{"role": "user", "content": user_prompt}],
            # If Gemini fails, LiteLLM tries these in order:
            fallbacks=["openai/gpt-4o-mini", "anthropic/claude-3-haiku"],
            # Optional: retry the same model before moving to the next fallback
            num_retries=2,
        )

        # Identify which model actually answered
        print(f"--- Success! Answered by: {response.model} ---")
        return response.choices[0].message.content

    except Exception as e:
        return f"All models failed. Error: {str(e)}"


# Example Usage
if __name__ == "__main__":
    result = smart_query("Explain how a relay works in 50 words.")
    print(result)
