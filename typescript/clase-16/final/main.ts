import Anthropic from "@anthropic-ai/sdk";

export {};

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const batch = await client.messages.batches.create({
  requests: [{
    custom_id: "resumen-001",
    params: {
      model: "claude-3-5-sonnet-latest",
      max_tokens: 120,
      messages: [{ role: "user", content: "Resume qué es Claude API." }],
    },
  }],
});

console.log(`Batch creado: ${batch.id} con estado ${batch.processing_status}`);
