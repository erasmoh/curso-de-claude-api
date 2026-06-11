import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam, ToolUnion } from "@anthropic-ai/sdk/resources/messages";

export {};

const MODEL = "claude-sonnet-4-6";

type Weather = { city: string; temperature: number; condition: string };
type ToolInput = Record<string, unknown>;

function getWeather(city: string): Weather {
  return { city, temperature: 18, condition: "lluvia ligera" };
}

const availableTools = {
  get_weather: (input: ToolInput): Weather => {
    const city = typeof input.city === "string" ? input.city : "Bogotá";
    return getWeather(city);
  },
};

const tool: ToolUnion = {
  name: "get_weather",
  description: "Obtiene el clima actual de una ciudad.",
  input_schema: { type: "object", properties: { city: { type: "string" } }, required: ["city"] },
};

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const messages: MessageParam[] = [{ role: "user", content: "¿Necesito paraguas hoy en Bogotá?" }];
const response = await client.messages.create({ model: MODEL, max_tokens: 800, tools: [tool], messages });

messages.push({ role: "assistant", content: response.content });
for (const block of response.content) {
  if (block.type === "tool_use" && block.name === "get_weather") {
    const result = availableTools.get_weather(block.input as ToolInput);
    messages.push({ role: "user", content: [{
      type: "tool_result",
      tool_use_id: block.id,
      content: JSON.stringify(result),
    }] });
  }
}

const final = await client.messages.create({ model: MODEL, max_tokens: 500, messages });
console.log(final.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
