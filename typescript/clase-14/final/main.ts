import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam, ToolUnion } from "@anthropic-ai/sdk/resources/messages";

export {};

const MODEL = "claude-sonnet-4-6";
const MAX_STEPS = 4;
const LOCAL_PAGES = new Map([
  ["https://docs.anthropic.com/en/api/messages", "La Messages API permite enviar messages, system prompts y herramientas."],
  ["https://docs.anthropic.com/en/docs/tool-use", "Tool use permite que Claude solicite funciones externas y reciba tool_result."],
]);

const tools: ToolUnion[] = [
  {
    name: "search_web",
    description: "Busca páginas relevantes para una pregunta.",
    input_schema: { type: "object", properties: { query: { type: "string" } }, required: ["query"] },
  },
  {
    name: "read_url",
    description: "Lee el contenido textual de una URL.",
    input_schema: { type: "object", properties: { url: { type: "string" } }, required: ["url"] },
  },
];

function searchWeb(): string {
  return [...LOCAL_PAGES.keys()].map((url) => `- ${url}`).join("\n");
}

function readUrl(url: string): string {
  return LOCAL_PAGES.get(url) ?? "Fuente no disponible en el set local de la demo.";
}

function runTool(name: string, input: Record<string, unknown>): string {
  if (name === "search_web") return searchWeb();
  if (name === "read_url") return readUrl(typeof input.url === "string" ? input.url : "");
  return "Herramienta no permitida.";
}

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const messages: MessageParam[] = [{ role: "user", content: "Investiga cómo funciona tool use en Claude API y cita fuentes." }];

for (let step = 0; step < MAX_STEPS; step += 1) {
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 900,
    system: "Responde con resumen corto, hallazgos principales, fuentes consultadas y limitaciones.",
    tools,
    messages,
  });
  const toolResults = response.content
    .filter((block) => block.type === "tool_use")
    .map((block) => ({
      type: "tool_result" as const,
      tool_use_id: block.id,
      content: runTool(block.name, block.input as Record<string, unknown>),
    }));

  if (toolResults.length === 0) {
    console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
    break;
  }

  messages.push({ role: "assistant", content: response.content });
  messages.push({ role: "user", content: toolResults });
}
