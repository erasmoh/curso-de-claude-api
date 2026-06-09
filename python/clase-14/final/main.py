"""Agente de búsqueda y resumen web con herramientas simuladas."""

from __future__ import annotations

import os
from anthropic import Anthropic

MODEL = "claude-3-5-sonnet-latest"


def search_web(query: str) -> str:
    """Stub didáctico: cambia esto por Tavily, Brave, SerpAPI u otro proveedor."""
    return "1. Anthropic Docs - https://docs.anthropic.com/en/api/messages\n2. Claude Tool Use - https://docs.anthropic.com/en/docs/tool-use"


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    query = "Cómo funciona tool use en Claude API"
    search_results = search_web(query)
    response = client.messages.create(
        model=MODEL,
        max_tokens=700,
        system="Resume con bullets y cita fuentes por URL.",
        messages=[{"role": "user", "content": f"Pregunta: {query}\nFuentes encontradas:\n{search_results}"}],
    )
    print("".join(block.text for block in response.content if block.type == "text"))


if __name__ == "__main__":
    main()
