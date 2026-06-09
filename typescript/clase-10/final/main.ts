import Anthropic from "@anthropic-ai/sdk";
import type { ToolUnion } from "@anthropic-ai/sdk/resources/messages";

export {};

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const weatherTool: ToolUnion = {
  name: "get_weather",
  description: "Obtiene el clima actual para una ciudad.",
  input_schema: {
    type: "object",
    properties: { city: { type: "string", description: "Ciudad a consultar." } },
    required: ["city"],
  },
};

const client = new Anthropic({ apiKey });
const response = await client.messages.create({
  model: "claude-3-5-sonnet-latest",
  max_tokens: 400,
  tools: [weatherTool],
  messages: [{ role: "user", content: "¿Cómo está el clima en Guatemala?" }],
});

for (const block of response.content) {
  if (block.type === "tool_use") console.log(`Claude quiere usar ${block.name}:`, block.input);
  if (block.type === "text") console.log(block.text);
}
