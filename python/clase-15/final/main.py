"""Rate limits, reintentos con jitter y observabilidad mínima."""

from __future__ import annotations

import json
import os
import random
import time
from collections.abc import Callable
from typing import TypeVar
from anthropic import Anthropic
from anthropic.types import Message

MODEL = "claude-sonnet-4-6"
T = TypeVar("T")


def retry_with_backoff(fn: Callable[[], T], max_retries: int = 5) -> T:
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as error:
            wait = (2 ** attempt) + random.random()
            print(f"Error: {error}. Reintentando en {wait:.2f}s")
            time.sleep(wait)
    raise RuntimeError("Se agotaron los reintentos")


def safe_claude_call(client: Anthropic, **kwargs: object) -> Message:
    start = time.perf_counter()

    def call() -> Message:
        return client.messages.create(**kwargs)

    response = retry_with_backoff(call)
    elapsed_ms = round((time.perf_counter() - start) * 1000)
    print(json.dumps({
        "model": response.model,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "elapsed_ms": elapsed_ms,
        "status": "success",
    }, ensure_ascii=False))
    return response


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    response = safe_claude_call(
        client,
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": "Dame un tip de observabilidad."}],
    )
    print("".join(block.text for block in response.content if block.type == "text"))


if __name__ == "__main__":
    main()
