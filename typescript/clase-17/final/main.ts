import Anthropic, { RateLimitError } from "@anthropic-ai/sdk";

export {};

function logEvent(event: string, fields: Record<string, unknown>): void {
  console.log(JSON.stringify({ event, ...fields }));
}

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
for (let attempt = 1; attempt <= 3; attempt += 1) {
  try {
    const response = await client.messages.create({
      model: "claude-3-5-sonnet-latest",
      max_tokens: 200,
      messages: [{ role: "user", content: "Dame un tip de observabilidad." }],
    });
    logEvent("claude_response", { attempt, usage: response.usage });
    console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
    break;
  } catch (error) {
    if (!(error instanceof RateLimitError)) throw error;
    const waitMs = 1000 * 2 ** attempt;
    logEvent("rate_limited", { attempt, waitMs });
    await new Promise((resolve) => setTimeout(resolve, waitMs));
  }
}
