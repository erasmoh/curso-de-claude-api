import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam } from "@anthropic-ai/sdk/resources/messages";
import { createInterface } from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { readFile, writeFile } from "node:fs/promises";

export {};

const MODEL = "claude-3-5-sonnet-latest";
const HISTORY_PATH = "chat_history.json";

async function loadHistory(): Promise<MessageParam[]> {
  try {
    return JSON.parse(await readFile(HISTORY_PATH, "utf8")) as MessageParam[];
  } catch {
    return [];
  }
}

async function saveHistory(messages: MessageParam[]): Promise<void> {
  await writeFile(HISTORY_PATH, JSON.stringify(messages, null, 2));
}

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const rl = createInterface({ input, output });
const messages = await loadHistory();
console.log("Chatbot listo. Escribe 'salir' para terminar.");

while (true) {
  const userText = (await rl.question("\nTú: ")).trim();
  if (userText.toLowerCase() === "salir") break;

  messages.push({ role: "user", content: userText });
  let assistantText = "";
  process.stdout.write("Claude: ");

  const stream = client.messages.stream({ model: MODEL, max_tokens: 600, messages: messages.slice(-12) });
  stream.on("text", (text) => {
    assistantText += text;
    process.stdout.write(text);
  });
  await stream.finalMessage();
  process.stdout.write("\n");

  messages.push({ role: "assistant", content: assistantText });
  await saveHistory(messages);
}

rl.close();
