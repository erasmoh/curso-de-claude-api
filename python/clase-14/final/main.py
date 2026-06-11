"""Batch API: crear batch, consultar estado y procesar resultados cuando termine."""

import os
from anthropic import Anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

MODEL = "claude-sonnet-4-6"


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    batch = client.messages.batches.create(requests=[
        Request(
            custom_id="invoice-001",
            params=MessageCreateParamsNonStreaming(
                model=MODEL,
                max_tokens=500,
                messages=[{"role": "user", "content": "Resume esta factura de ejemplo."}],
            ),
        )
    ])
    print(batch.id, batch.processing_status)

    batch_status = client.messages.batches.retrieve(batch.id)
    print(batch_status.processing_status)

    if batch_status.processing_status == "ended":
        for result in client.messages.batches.results(batch.id):
            print(result.custom_id, result.result.type)
    else:
        print("El batch todavía no termina. Vuelve a consultar más tarde antes de leer results.")


if __name__ == "__main__":
    main()
