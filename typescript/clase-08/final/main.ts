import Anthropic from "@anthropic-ai/sdk";

export {};

const EXTRACTION_PROMPT = `
Extrae datos del texto usando estas reglas:
- Si un campo no aparece, usa null.
- No inventes fechas, totales ni nombres.
- Devuelve JSON válido con provider, date, total y currency.
- Si el documento es ambiguo, agrega una lista warnings.
`;

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const response = await client.messages.create({
  model: "claude-3-5-sonnet-latest",
  max_tokens: 350,
  system: EXTRACTION_PROMPT,
  messages: [{ role: "user", content: "Factura ACME emitida el 2026-05-01. Total: USD 129.90" }],
});

for (const block of response.content) {
  if (block.type === "text") console.log(block.text);
}
