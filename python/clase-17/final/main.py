"""Reintentos con backoff y logs estructurados para producción."""

from __future__ import annotations

import json
import os
import time
from anthropic import Anthropic, RateLimitError

MODEL = "claude-3-5-sonnet-latest"


def log_event(event: str, **fields: object) -> None:
    print(json.dumps({"event": event, **fields}, ensure_ascii=False))


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    for attempt in range(1, 4):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=200,
                messages=[{"role": "user", "content": "Dame un tip de observabilidad."}],
            )
            log_event("claude_response", attempt=attempt, usage=response.usage.model_dump())
            print("".join(block.text for block in response.content if block.type == "text"))
            return
        except RateLimitError:
            wait_seconds = 2 ** attempt
            log_event("rate_limited", attempt=attempt, wait_seconds=wait_seconds)
            time.sleep(wait_seconds)

    raise RuntimeError("No se pudo completar la request después de 3 intentos.")


if __name__ == "__main__":
    main()
