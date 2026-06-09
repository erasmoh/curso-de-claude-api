import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam } from "@anthropic-ai/sdk/resources/messages";
import { createInterface } from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { readFile, writeFile } from "node:fs/promises";

export {};

const MODEL = "claude-sonnet-4-6";
const HISTORY_PATH = "history.json";

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

async function streamClaudeResponse(client: Anthropic, messages: MessageParam[]): Promise<string> {
  let assistantText = "";
  const stream = client.messages.stream({ model: MODEL, max_tokens: 700, messages: messages.slice(-12) });
  stream.on("text", (text) => {
    assistantText += text;
    process.stdout.write(text);
  });
  await stream.finalMessage();
  process.stdout.write("\n");
  return assistantText;
}

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const rl = createInterface({ input, output });
let messages = await loadHistory();
console.log("Chatbot listo. Comandos: /salir para terminar, /reset para borrar historial.");

while (true) {
  const userInput = (await rl.question("\nTú: ")).trim();
  if (userInput === "/salir") break;
  if (userInput === "/reset") {
    messages = [];
    await saveHistory(messages);
    console.log("Historial reiniciado.");
    continue;
  }
  if (!userInput) continue;

  messages.push({ role: "user", content: userInput });
  process.stdout.write("Claude: ");
  try {
    const assistantText = await streamClaudeResponse(client, messages);
    messages.push({ role: "assistant", content: assistantText });
    await saveHistory(messages);
  } catch (error) {
    messages.pop();
    console.log(`Error llamando a Claude: ${error instanceof Error ? error.message : "desconocido"}`);
  }
}

rl.close();
