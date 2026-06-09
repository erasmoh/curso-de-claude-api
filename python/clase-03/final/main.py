"""Gestión básica de contexto para conversaciones largas."""

from __future__ import annotations

import os
from anthropic import Anthropic

MODEL = "claude-3-5-sonnet-latest"
MAX_HISTORY_MESSAGES = 6


def trim_history(messages: list[dict[str, str]], max_messages: int = MAX_HISTORY_MESSAGES) -> list[dict[str, str]]:
    """Conserva los mensajes más recientes para controlar costo y contexto."""
    if len(messages) <= max_messages:
        return messages
    return messages[-max_messages:]


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    history = [{"role": "user", "content": f"Mensaje antiguo #{index}"} for index in range(10)]
    history.append({"role": "user", "content": "Resume qué decisiones importantes recuerdas."})

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=250,
        system="Si falta contexto, dilo explícitamente y pide más información.",
        messages=trim_history(history),
    )

    for block in response.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
