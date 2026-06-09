import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam, ToolUnion } from "@anthropic-ai/sdk/resources/messages";

export {};

function getWeather(city: string): string {
  return `Clima en ${city}: 24°C, parcialmente nublado.`;
}

const tool: ToolUnion = {
  name: "get_weather",
  description: "Clima por ciudad.",
  input_schema: { type: "object", properties: { city: { type: "string" } }, required: ["city"] },
};

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const messages: MessageParam[] = [{ role: "user", content: "Dime el clima de Bogotá y dame una recomendación." }];
const first = await client.messages.create({ model: "claude-3-5-sonnet-latest", max_tokens: 400, tools: [tool], messages });

messages.push({ role: "assistant", content: first.content });
for (const block of first.content) {
  if (block.type === "tool_use") {
    const input = block.input as Record<string, unknown>;
    const city = typeof input.city === "string" ? input.city : "ciudad desconocida";
    messages.push({ role: "user", content: [{ type: "tool_result", tool_use_id: block.id, content: getWeather(city) }] });
  }
}

const final = await client.messages.create({ model: "claude-3-5-sonnet-latest", max_tokens: 400, messages });
for (const block of final.content) {
  if (block.type === "text") console.log(block.text);
}
