"""Chatbot de terminal con historial persistente y streaming."""

from __future__ import annotations

import json
import os
from pathlib import Path
from anthropic import Anthropic

MODEL = "claude-3-5-sonnet-latest"
HISTORY_PATH = Path("chat_history.json")


def load_history() -> list[dict[str, str]]:
    if not HISTORY_PATH.exists():
        return []
    return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))


def save_history(messages: list[dict[str, str]]) -> None:
    HISTORY_PATH.write_text(json.dumps(messages, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    messages = load_history()
    print("Chatbot listo. Escribe 'salir' para terminar.")

    while True:
        user_text = input("\nTú: ").strip()
        if user_text.lower() == "salir":
            break

        messages.append({"role": "user", "content": user_text})
        assistant_text = ""
        print("Claude: ", end="", flush=True)
        with client.messages.stream(model=MODEL, max_tokens=600, messages=messages[-12:]) as stream:
            for text in stream.text_stream:
                assistant_text += text
                print(text, end="", flush=True)
        print()

        messages.append({"role": "assistant", "content": assistant_text})
        save_history(messages)


if __name__ == "__main__":
    main()
