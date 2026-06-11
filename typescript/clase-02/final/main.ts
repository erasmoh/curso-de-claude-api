import Anthropic from "@anthropic-ai/sdk";

export {};

const MODEL = "claude-sonnet-4-6";

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const response = await client.messages.create({
  model: MODEL,
  max_tokens: 400,
  messages: [
    { role: "user", content: "Mi proyecto será un chatbot para recetas." },
    { role: "assistant", content: "Perfecto. Puedo ayudarte con ingredientes y pasos." },
    { role: "user", content: "Recuérdame cuál era mi proyecto y sugiere el primer feature." },
  ],
});

for (const block of response.content) {
  if (block.type === "text") console.log(block.text);
}
