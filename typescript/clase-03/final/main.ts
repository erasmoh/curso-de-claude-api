import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam } from "@anthropic-ai/sdk/resources/messages";

export {};

const MODEL = "claude-sonnet-4-6";
const MAX_HISTORY_MESSAGES = 12;

function keepRecentMessages(messages: MessageParam[], maxMessages = MAX_HISTORY_MESSAGES): MessageParam[] {
  return messages.slice(-maxMessages);
}

async function summarizeHistory(client: Anthropic, messages: MessageParam[]): Promise<string> {
  const transcript = messages.map((message) => `${message.role}: ${message.content}`).join("\n");
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 400,
    system: "Resume una conversación para preservar contexto importante.",
    messages: [{ role: "user", content: transcript }],
  });
  return response.content.filter((block) => block.type === "text").map((block) => block.text).join("");
}

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const messages: MessageParam[] = [
  { role: "user", content: "Estoy creando un chatbot para soporte técnico." },
  { role: "assistant", content: "Perfecto. Lo enfocaremos en respuestas claras." },
  { role: "user", content: "El bot debe escalar casos urgentes." },
];

const summary = await summarizeHistory(client, messages);
const controlledHistory: MessageParam[] = [{ role: "user", content: `Resumen previo: ${summary}` }, ...keepRecentMessages(messages), { role: "user", content: "¿Qué decisión importante debo recordar?" }];
const response = await client.messages.create({ model: MODEL, max_tokens: 500, messages: controlledHistory });

console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
console.log({ input_tokens: response.usage.input_tokens, output_tokens: response.usage.output_tokens });
