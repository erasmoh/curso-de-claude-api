"""Agente de búsqueda y resumen web con search_web, read_url y fuentes."""

from __future__ import annotations

import os
from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"
MAX_STEPS = 4

LOCAL_PAGES = {
    "https://docs.anthropic.com/en/api/messages": "La Messages API permite enviar messages, system prompts y herramientas.",
    "https://docs.anthropic.com/en/docs/tool-use": "Tool use permite que Claude solicite funciones externas y reciba tool_result.",
}

TOOLS = [
    {
        "name": "search_web",
        "description": "Busca páginas relevantes para una pregunta.",
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
    },
    {
        "name": "read_url",
        "description": "Lee el contenido textual de una URL.",
        "input_schema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]},
    },
]


def search_web(query: str) -> str:
    return "\n".join(f"- {url}" for url in LOCAL_PAGES)


def read_url(url: str) -> str:
    if url not in LOCAL_PAGES:
        return "Fuente no disponible en el set local de la demo."
    return LOCAL_PAGES[url]


def run_tool(name: str, args: dict[str, object]) -> str:
    if name == "search_web":
        query = str(args.get("query", ""))
        return search_web(query)
    if name == "read_url":
        url = str(args.get("url", ""))
        return read_url(url)
    return "Herramienta no permitida."


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    messages = [{"role": "user", "content": "Investiga cómo funciona tool use en Claude API y cita fuentes."}]

    for step in range(MAX_STEPS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=900,
            system="Responde con resumen corto, hallazgos principales, fuentes consultadas y limitaciones.",
            tools=TOOLS,
            messages=messages,
        )
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": run_tool(block.name, block.input),
                })

        if not tool_results:
            print("".join(block.text for block in response.content if block.type == "text"))
            return

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    print("El agente alcanzó el máximo de pasos sin respuesta final.")


if __name__ == "__main__":
    main()
