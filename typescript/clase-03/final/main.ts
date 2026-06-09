import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam } from "@anthropic-ai/sdk/resources/messages";

export {};

const MODEL = "claude-3-5-sonnet-latest";
const MAX_HISTORY_MESSAGES = 6;

function trimHistory(messages: MessageParam[]): MessageParam[] {
  return messages.length <= MAX_HISTORY_MESSAGES ? messages : messages.slice(-MAX_HISTORY_MESSAGES);
}

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const history: MessageParam[] = Array.from({ length: 10 }, (_, index) => ({
  role: "user",
  content: `Mensaje antiguo #${index}`,
}));
history.push({ role: "user", content: "Resume qué decisiones importantes recuerdas." });

const client = new Anthropic({ apiKey });
const response = await client.messages.create({
  model: MODEL,
  max_tokens: 250,
  system: "Si falta contexto, dilo explícitamente y pide más información.",
  messages: trimHistory(history),
});

for (const block of response.content) {
  if (block.type === "text") console.log(block.text);
}
