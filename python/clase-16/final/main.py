"""Batch API: preparar muchas solicitudes asincrónicas."""

import os
from anthropic import Anthropic

MODEL = "claude-3-5-sonnet-latest"


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    batch = client.messages.batches.create(requests=[
        {
            "custom_id": "resumen-001",
            "params": {
                "model": MODEL,
                "max_tokens": 120,
                "messages": [{"role": "user", "content": "Resume qué es Claude API."}],
            },
        }
    ])
    print(f"Batch creado: {batch.id} con estado {batch.processing_status}")


if __name__ == "__main__":
    main()
