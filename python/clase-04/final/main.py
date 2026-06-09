"""Streaming: imprime la respuesta conforme llega desde Claude."""

import os
from anthropic import Anthropic

MODEL = "claude-3-5-sonnet-latest"


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    with client.messages.stream(
        model=MODEL,
        max_tokens=500,
        messages=[{"role": "user", "content": "Explícame streaming en Claude API con una analogía."}],
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print()


if __name__ == "__main__":
    main()
