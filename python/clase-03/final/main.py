"""Estrategias de contexto: truncado, resumen y uso de tokens."""

from __future__ import annotations

import os
from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"
MAX_HISTORY_MESSAGES = 12


def keep_recent_messages(messages: list[dict[str, str]], max_messages: int = MAX_HISTORY_MESSAGES) -> list[dict[str, str]]:
    """Conserva solo los últimos turnos para controlar latencia, contexto y costo."""
    return messages[-max_messages:]


def summarize_history(client: Anthropic, messages: list[dict[str, str]]) -> str:
    """Resume la conversación cuando ya no conviene enviar todo el historial."""
    transcript = "\n".join(f"{message['role']}: {message['content']}" for message in messages)
    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system="Resume una conversación para preservar contexto importante.",
        messages=[{"role": "user", "content": transcript}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    messages = [
        {"role": "user", "content": "Estoy creando un chatbot para soporte técnico."},
        {"role": "assistant", "content": "Perfecto. Lo enfocaremos en respuestas claras."},
        {"role": "user", "content": "El bot debe escalar casos urgentes."},
    ]

    summary = summarize_history(client, messages)
    controlled_history = [{"role": "user", "content": f"Resumen previo: {summary}"}]
    controlled_history.extend(keep_recent_messages(messages))
    controlled_history.append({"role": "user", "content": "¿Qué decisión importante debo recordar?"})

    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=controlled_history,
    )

    print("Respuesta:")
    print("".join(block.text for block in response.content if block.type == "text"))
    print("\nUso de tokens:")
    print({"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens})


if __name__ == "__main__":
    main()
