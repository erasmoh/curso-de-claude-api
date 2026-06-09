import Anthropic from "@anthropic-ai/sdk";

export {};

function searchWeb(query: string): string {
  return [
    `Consulta: ${query}`,
    "1. Anthropic Docs - https://docs.anthropic.com/en/api/messages",
    "2. Claude Tool Use - https://docs.anthropic.com/en/docs/tool-use",
  ].join("\n");
}

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const query = "Cómo funciona tool use en Claude API";
const client = new Anthropic({ apiKey });
const response = await client.messages.create({
  model: "claude-3-5-sonnet-latest",
  max_tokens: 700,
  system: "Resume con bullets y cita fuentes por URL.",
  messages: [{ role: "user", content: `Pregunta: ${query}\nFuentes encontradas:\n${searchWeb(query)}` }],
});

console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
