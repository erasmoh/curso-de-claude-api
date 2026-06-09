"""Prompt engineering para extracción precisa de datos de facturas."""

import os
from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"

EXTRACTION_PROMPT = """
Extrae datos de la factura adjunta.
Responde únicamente JSON válido.
No inventes datos. Si un campo no aparece, usa null.
Normaliza montos como números, sin símbolos de moneda.
La moneda debe ser un código ISO si puedes inferirlo.

Campos requeridos:
- provider
- date
- currency
- total
- items: description, quantity, unit_price, total

Ejemplos de reglas:
- Si la factura no muestra moneda explícita, usa null.
- Si hay impuestos separados, inclúyelos en items solo si aparecen como línea propia.
- Si no puedes leer un campo, usa null en lugar de adivinar.
"""


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    document_text = "Factura ACME emitida el 2026-05-01. Servicio: soporte, total: USD 129.90"
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=700,
        system=EXTRACTION_PROMPT,
        messages=[{"role": "user", "content": document_text}],
    )

    for block in response.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
