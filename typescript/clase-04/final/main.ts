import Anthropic from "@anthropic-ai/sdk";

export {};

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const stream = client.messages.stream({
  model: "claude-3-5-sonnet-latest",
  max_tokens: 500,
  messages: [{ role: "user", content: "Explícame streaming en Claude API con una analogía." }],
});

stream.on("text", (text) => process.stdout.write(text));
await stream.finalMessage();
process.stdout.write("\n");
