import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam, ToolResultBlockParam, ToolUnion } from "@anthropic-ai/sdk/resources/messages";

export {};

const MAX_STEPS = 4;

function readNumber(tokens: string[], cursor: { index: number }): number {
  const token = tokens[cursor.index];
  if (token === undefined || !/^\d+(\.\d+)?$/.test(token)) throw new Error("Número esperado.");
  cursor.index += 1;
  return Number(token);
}

function evaluateExpression(expression: string): number {
  const tokens = expression.match(/\d+(?:\.\d+)?|[()+\-*/]/g) ?? [];
  const cursor = { index: 0 };

  function factor(): number {
    if (tokens[cursor.index] === "(") {
      cursor.index += 1;
      const value = expr();
      if (tokens[cursor.index] !== ")") throw new Error("Paréntesis sin cerrar.");
      cursor.index += 1;
      return value;
    }
    if (tokens[cursor.index] === "-") {
      cursor.index += 1;
      return -factor();
    }
    return readNumber(tokens, cursor);
  }

  function term(): number {
    let value = factor();
    while (tokens[cursor.index] === "*" || tokens[cursor.index] === "/") {
      const operator = tokens[cursor.index];
      cursor.index += 1;
      const right = factor();
      value = operator === "*" ? value * right : value / right;
    }
    return value;
  }

  function expr(): number {
    let value = term();
    while (tokens[cursor.index] === "+" || tokens[cursor.index] === "-") {
      const operator = tokens[cursor.index];
      cursor.index += 1;
      const right = term();
      value = operator === "+" ? value + right : value - right;
    }
    return value;
  }

  const result = expr();
  if (cursor.index !== tokens.length) throw new Error("Tokens extra no permitidos.");
  return result;
}

function calculator(expression: string): string {
  try {
    return String(evaluateExpression(expression));
  } catch (error) {
    return `Expresión rechazada: ${error instanceof Error ? error.message : "input inválido"}`;
  }
}

const tool: ToolUnion = {
  name: "calculator",
  description: "Calculadora aritmética.",
  input_schema: { type: "object", properties: { expression: { type: "string" } }, required: ["expression"] },
};

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const messages: MessageParam[] = [{ role: "user", content: "Calcula (128 * 7) + 34 y explica el resultado." }];

for (let step = 0; step < MAX_STEPS; step += 1) {
  const response = await client.messages.create({ model: "claude-3-5-sonnet-latest", max_tokens: 500, tools: [tool], messages });
  messages.push({ role: "assistant", content: response.content });
  const toolResults: ToolResultBlockParam[] = [];

  for (const block of response.content) {
    if (block.type === "tool_use") {
      const input = block.input as Record<string, unknown>;
      const expression = typeof input.expression === "string" ? input.expression : "";
      toolResults.push({ type: "tool_result", tool_use_id: block.id, content: calculator(expression) });
    }
  }

  if (toolResults.length === 0) {
    console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
    break;
  }
  messages.push({ role: "user", content: toolResults });
}
