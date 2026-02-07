import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from langchain_crynux import ChatCrynux
from pydantic import BaseModel, Field

if "OPENAI_API_KEY" not in os.environ:
    print("OPENAI_API_KEY not found in environment or .env file.")


class Weather(BaseModel):
    city: str = Field(description="The city to get the weather for")
    temperature: float = Field(description="The temperature in celsius")

def test_structured_output():
    print("Testing ChatCrynux structured output...")
    chat = ChatCrynux(
        base_url=os.environ.get("CRYNUX_BASE_URL", "https://bridge.crynux-as.xyz/v1/llm"),
        model=os.environ.get("CRYNUX_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
        temperature=0,
        timeout=60
    )

    structured_llm = chat.with_structured_output(Weather)

    query = "The weather in Tokyo is 25.5 degrees celsius."
    print(f"Invoking with query: '{query}'")

    try:
        response = structured_llm.invoke(query)

        print("Response received:")
        print(response)

        if isinstance(response, Weather):
            print("Successfully parsed structured output:")
            print(f"City: {response.city}")
            print(f"Temperature: {response.temperature}")
        else:
            print("Response is not of expected type Weather.")
            print(f"Actual type: {type(response)}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_structured_output()
