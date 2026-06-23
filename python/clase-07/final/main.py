"""JSON estructurado para facturas con prompt estricto y validación Pydantic."""

from __future__ import annotations

import json
import os
from anthropic import Anthropic
from pydantic import BaseModel

MODEL = "claude-sonnet-4-6"


class InvoiceItem(BaseModel):
    description: str
    quantity: float | None = None
    unit_price: float | None = None
    total: float


class InvoiceData(BaseModel):
    provider: str
    date: str
    currency: str
    total: float
    items: list[InvoiceItem]


PROMPT = """
Extrae la información de la factura.
Responde únicamente JSON válido.
No agregues explicación fuera del JSON.
"""


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    invoice_text = """
    Factura de ACME S.A. emitida el 2026-05-01.
    2 horas de consultoría a 50 USD cada una. Total: USD 100.
    """
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        system=PROMPT,
        messages=[{"role": "user", "content": invoice_text}],
    )

    raw_text = "".join(block.text for block in response.content if block.type == "text")
    invoice = InvoiceData.model_validate(json.loads(raw_text))
    print(invoice.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
