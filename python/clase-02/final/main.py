"""Conversación multi-turn: el cliente guarda y reenvía el historial."""

import os
from anthropic import Anthropic

MODEL = "claude-3-5-sonnet-latest"


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    messages = [
        {"role": "user", "content": "Mi proyecto será un chatbot para recetas."},
        {"role": "assistant", "content": "Perfecto. Puedo ayudarte con ingredientes y pasos."},
        {"role": "user", "content": "Recuérdame cuál era mi proyecto y sugiere el primer feature."},
    ]

    response = client.messages.create(model=MODEL, max_tokens=400, messages=messages)
    for block in response.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
