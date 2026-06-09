"""Extractor de facturas PDF con CLI, validación y salida output.json."""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
from anthropic import Anthropic
from schemas import InvoiceData

MODEL = "claude-sonnet-4-6"
OUTPUT_PATH = Path("output.json")


def to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def parse_and_validate(raw_text: str) -> InvoiceData:
    return InvoiceData.model_validate(json.loads(raw_text))


def extract_invoice(client: Anthropic, pdf_path: Path) -> InvoiceData:
    pdf_data = to_base64(pdf_path)
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system="Extrae la factura como JSON válido con provider, date, total, currency e items.",
        messages=[{"role": "user", "content": [
            {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_data}},
            {"type": "text", "text": "Devuelve únicamente JSON válido. No uses Markdown."},
        ]}],
    )
    raw_text = "".join(block.text for block in response.content if block.type == "text")
    return parse_and_validate(raw_text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrae datos de una factura PDF con Claude API.")
    parser.add_argument("pdf_path", type=Path, help="Ruta al PDF de factura. Ej: ./samples/factura_001.pdf")
    args = parser.parse_args()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    try:
        invoice = extract_invoice(Anthropic(api_key=api_key), args.pdf_path)
    except FileNotFoundError:
        print("No encontramos el archivo PDF.")
        raise SystemExit(1)
    except (json.JSONDecodeError, ValueError) as error:
        print(f"La respuesta no pudo validarse: {error}")
        raise SystemExit(1)

    OUTPUT_PATH.write_text(json.dumps(invoice.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Factura extraída en {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
