"""Tool use: Claude solicita una función externa mediante tool_use."""

import os
from anthropic import Anthropic

MODEL = "claude-3-5-sonnet-latest"

WEATHER_TOOL = {
    "name": "get_weather",
    "description": "Obtiene el clima actual para una ciudad.",
    "input_schema": {
        "type": "object",
        "properties": {"city": {"type": "string", "description": "Ciudad a consultar."}},
        "required": ["city"],
    },
}


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        tools=[WEATHER_TOOL],
        messages=[{"role": "user", "content": "¿Cómo está el clima en Guatemala?"}],
    )

    for block in response.content:
        if block.type == "tool_use":
            print(f"Claude quiere usar {block.name} con input: {block.input}")
        elif block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
