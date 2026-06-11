import Anthropic from "@anthropic-ai/sdk";
import Fastify from "fastify";
import { z } from "zod";

export {};

const MODEL = "claude-sonnet-4-6";
const APP_API_KEY = process.env.APP_API_KEY;
const ChatRequest = z.object({ message: z.string().min(1) });
const server = Fastify({ logger: true });

server.get("/health", async () => ({ status: "ok" }));

server.post("/chat", async (request, reply) => {
  if (!APP_API_KEY) return reply.code(500).send({ error: "APP_API_KEY no configurada." });
  if (request.headers["x-api-key"] !== APP_API_KEY) {
    return reply.code(401).send({ error: "Unauthorized" });
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return reply.code(500).send({ error: "ANTHROPIC_API_KEY no configurada." });

  const payload = ChatRequest.parse(request.body);
  const client = new Anthropic({ apiKey });
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 600,
    messages: [{ role: "user", content: payload.message }],
  });
  const replyText = response.content.filter((block) => block.type === "text").map((block) => block.text).join("");
  return { reply: replyText };
});

await server.listen({ port: Number(process.env.PORT ?? 3000), host: "0.0.0.0" });
