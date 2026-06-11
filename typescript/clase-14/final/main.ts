import Anthropic from "@anthropic-ai/sdk";

export {};

const MODEL = "claude-sonnet-4-6";
const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const batch = await client.messages.batches.create({
  requests: [{
    custom_id: "invoice-001",
    params: {
      model: MODEL,
      max_tokens: 500,
      messages: [{ role: "user", content: "Resume esta factura de ejemplo." }],
    },
  }],
});

console.log(batch.id, batch.processing_status);
const batchStatus = await client.messages.batches.retrieve(batch.id);
console.log(batchStatus.processing_status);

if (batchStatus.processing_status === "ended") {
  const results = await client.messages.batches.results(batch.id);
  for await (const result of results) {
    console.log(result.custom_id, result.result.type);
  }
} else {
  console.log("El batch todavía no termina. Vuelve a consultar más tarde antes de leer results.");
}
