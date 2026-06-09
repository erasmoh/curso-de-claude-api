"""Extractor de factura PDF con salida JSON validada."""

from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from anthropic import Anthropic
from pydantic import BaseModel

MODEL = "claude-3-5-sonnet-latest"


class InvoiceItem(BaseModel):
    description: str
    quantity: float
    unit_price: float


class Invoice(BaseModel):
    provider: str | None
    date: str | None
    total: float | None
    currency: str | None
    items: list[InvoiceItem]


def extract_invoice(pdf_path: Path) -> Invoice:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    pdf_data = base64.b64encode(pdf_path.read_bytes()).decode("utf-8")
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=900,
        system="Extrae factura como JSON válido. No agregues Markdown.",
        messages=[{"role": "user", "content": [
            {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_data}},
            {"type": "text", "text": "Campos: provider, date, total, currency, items[]."},
        ]}],
    )
    raw_text = "".join(block.text for block in response.content if block.type == "text")
    return Invoice.model_validate(json.loads(raw_text))


if __name__ == "__main__":
    invoice = extract_invoice(Path("invoice.pdf"))
    print(invoice.model_dump_json(indent=2))
