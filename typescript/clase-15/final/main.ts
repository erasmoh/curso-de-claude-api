import Anthropic from "@anthropic-ai/sdk";
import type { Message } from "@anthropic-ai/sdk/resources/messages";

export {};

const MODEL = "claude-sonnet-4-6";

async function retryWithBackoff<T>(fn: () => Promise<T>, maxRetries = 5): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt += 1) {
    try {
      return await fn();
    } catch (error) {
      const waitMs = (2 ** attempt + Math.random()) * 1000;
      console.log(`Error: ${error}. Reintentando en ${(waitMs / 1000).toFixed(2)}s`);
      await new Promise((resolve) => setTimeout(resolve, waitMs));
    }
  }
  throw new Error("Se agotaron los reintentos");
}

async function safeClaudeCall(client: Anthropic): Promise<Message> {
  const start = performance.now();
  const response = await retryWithBackoff(() => client.messages.create({
    model: MODEL,
    max_tokens: 200,
    messages: [{ role: "user", content: "Dame un tip de observabilidad." }],
  }));
  console.log(JSON.stringify({
    model: response.model,
    input_tokens: response.usage.input_tokens,
    output_tokens: response.usage.output_tokens,
    elapsed_ms: Math.round(performance.now() - start),
    status: "success",
  }));
  return response;
}

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const response = await safeClaudeCall(new Anthropic({ apiKey }));
console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
