"""JSON estructurado con prompt estricto y validación Pydantic."""

from __future__ import annotations

import json
import os
from anthropic import Anthropic
from pydantic import BaseModel, Field

MODEL = "claude-3-5-sonnet-latest"


class TaskSummary(BaseModel):
    title: str = Field(description="Título corto de la tarea.")
    priority: str = Field(description="low, medium o high.")
    next_step: str = Field(description="Siguiente acción concreta.")


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system="Responde únicamente JSON válido, sin Markdown ni texto extra.",
        messages=[{"role": "user", "content": "Convierte esta idea en tarea: lanzar chatbot con memoria."}],
    )

    raw_text = "".join(block.text for block in response.content if block.type == "text")
    parsed = TaskSummary.model_validate(json.loads(raw_text))
    print(parsed.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
