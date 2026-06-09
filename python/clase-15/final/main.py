"""Prompt caching: marca instrucciones largas y reutilizables."""

import os
from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    long_policy = "Reglas internas del asistente. " * 400
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=[{"type": "text", "text": long_policy, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": "Resume las 3 reglas principales."}],
    )
    print("".join(block.text for block in response.content if block.type == "text"))
    print(response.usage)


if __name__ == "__main__":
    main()
