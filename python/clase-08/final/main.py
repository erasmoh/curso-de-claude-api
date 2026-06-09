"""Prompt engineering para extraer datos de documentos ambiguos."""

import os
from anthropic import Anthropic

MODEL = "claude-3-5-sonnet-latest"

EXTRACTION_PROMPT = """
Extrae datos del texto usando estas reglas:
- Si un campo no aparece, usa null.
- No inventes fechas, totales ni nombres.
- Devuelve JSON válido con provider, date, total y currency.
- Si el documento es ambiguo, agrega una lista warnings.
"""


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    document_text = "Factura ACME emitida el 2026-05-01. Total: USD 129.90"
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=350,
        system=EXTRACTION_PROMPT,
        messages=[{"role": "user", "content": document_text}],
    )

    for block in response.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
