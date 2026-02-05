# langchain-crynux

![PyPI - Version](https://img.shields.io/pypi/v/langchain-crynux?style=flat-square)

Drop-in replacement for `langchain-openai` ChatOpenAI that lets existing OpenAI-compatible LLM code run on the Crynux network without changes.

## Installation
```bash
pip install langchain-crynux
```

Dependencies:
- langchain-openai>=1.0.1

## Usage

```python
import os
from langchain_crynux import ChatCrynux

# Option 1: environment variable (same as langchain-openai)
os.environ["OPENAI_API_KEY"] = "your-api-key"

chat = ChatCrynux(
    base_url="https://bridge.crynux-as.xyz/v1/llm",
    model="Qwen/Qwen-2.5-7B-Instruct",
    vram_limit=24,
    timeout=60,
    # Option 2: pass api_key directly
    # api_key="your-api-key",
)

response = chat.invoke("Hello from Crynux.")
print(response.content)
```

 * `base_url` defaults to `https://bridge.crynux-as.xyz/v1/llm`.

 * `vram_limit` is the minimum GPU VRAM (in GB) required for the inference run. Default is 24.

## Structured Output

You can use the `with_structured_output` method to get structured output from the model. This is useful for extraction or function calling tasks.

**Why Function Calling?**

`langchain-crynux` defaults to `method="function_calling"` automatically. This is because many open-source models (like Qwen) running on the decentralized Crynux Network do not fully support OpenAI's native strict `json_mode` or `response_format`. Using tool calling is the most reliable way to strictly enforce the output schema on these models. See [Crynux Structured Output Docs](https://docs.crynux.io/application-development/how-to-run-llm-using-crynux-network/structured-ouput) for details.

```python
from typing import Optional
from langchain_crynux import ChatCrynux
from pydantic import BaseModel, Field

class Weather(BaseModel):
    """The weather in a specific location."""
    city: str = Field(description="The city to get the weather for")
    temperature: float = Field(description="The temperature in celsius")
    condition: Optional[str] = Field(description="The weather condition (e.g., sunny, rainy)")

chat = ChatCrynux(
    model="Qwen/Qwen-2.5-7B-Instruct",
    temperature=0
)

# Automatically uses method="function_calling" for reliability
structured_llm = chat.with_structured_output(Weather)

response = structured_llm.invoke("The weather in Tokyo is 25.5 degrees celsius and sunny.")
print(response)
# Weather(city='Tokyo', temperature=25.5, condition='sunny')
```
