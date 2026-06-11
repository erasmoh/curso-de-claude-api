import Anthropic from "@anthropic-ai/sdk";

export {};

const MODEL = "claude-sonnet-4-6";
const EXTRACTION_PROMPT = `
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
`;

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const response = await client.messages.create({
  model: MODEL,
  max_tokens: 700,
  system: EXTRACTION_PROMPT,
  messages: [{ role: "user", content: "Factura ACME emitida el 2026-05-01. Servicio: soporte, total: USD 129.90" }],
});

for (const block of response.content) {
  if (block.type === "text") console.log(block.text);
}
