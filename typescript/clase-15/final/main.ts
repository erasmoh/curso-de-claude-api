import Anthropic from "@anthropic-ai/sdk";

export {};

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const longPolicy = "Reglas internas del asistente. ".repeat(400);
const client = new Anthropic({ apiKey });
const response = await client.messages.create({
  model: "claude-3-5-sonnet-latest",
  max_tokens: 300,
  system: [{ type: "text", text: longPolicy, cache_control: { type: "ephemeral" } }],
  messages: [{ role: "user", content: "Resume las 3 reglas principales." }],
});

console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
console.log(response.usage);
