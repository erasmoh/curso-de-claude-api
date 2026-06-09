import Anthropic from "@anthropic-ai/sdk";

export {};

const MODEL = "claude-3-5-sonnet-latest";

function requireApiKey(): string {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    throw new Error("Define ANTHROPIC_API_KEY antes de ejecutar este script.");
  }
  return apiKey;
}

async function main(): Promise<void> {
  const client = new Anthropic({ apiKey: requireApiKey() });
  const message = await client.messages.create({
    model: MODEL,
    max_tokens: 300,
    system: "Responde como un mentor breve y práctico de TypeScript.",
    messages: [{ role: "user", content: "Dame 3 ideas para practicar Claude API." }],
  });

  for (const block of message.content) {
    if (block.type === "text") console.log(block.text);
  }
}

await main();
