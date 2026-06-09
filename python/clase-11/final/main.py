"""Ejecutar una herramienta local y responder con tool_result."""

from __future__ import annotations

import os
from anthropic import Anthropic

MODEL = "claude-3-5-sonnet-latest"


def get_weather(city: str) -> str:
    """Herramienta fake para clase: reemplázala por una API real."""
    return f"Clima en {city}: 24°C, parcialmente nublado."


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    messages = [{"role": "user", "content": "Dime el clima de Bogotá y dame una recomendación."}]
    first = client.messages.create(
        model=MODEL,
        max_tokens=400,
        tools=[{"name": "get_weather", "description": "Clima por ciudad.", "input_schema": {
            "type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}],
        messages=messages,
    )

    messages.append({"role": "assistant", "content": first.content})
    for block in first.content:
        if block.type == "tool_use":
            result = get_weather(str(block.input["city"]))
            messages.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": block.id, "content": result}]})

    final = client.messages.create(model=MODEL, max_tokens=400, messages=messages)
    for block in final.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
