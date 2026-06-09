import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";

export {};

const TaskSummary = z.object({
  title: z.string(),
  priority: z.enum(["low", "medium", "high"]),
  next_step: z.string(),
});

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const response = await client.messages.create({
  model: "claude-3-5-sonnet-latest",
  max_tokens: 300,
  system: "Responde únicamente JSON válido, sin Markdown ni texto extra.",
  messages: [{ role: "user", content: "Convierte esta idea en tarea: lanzar chatbot con memoria." }],
});

const rawText = response.content.filter((block) => block.type === "text").map((block) => block.text).join("");
const parsed = TaskSummary.parse(JSON.parse(rawText));
console.log(JSON.stringify(parsed, null, 2));
