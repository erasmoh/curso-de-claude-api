import Anthropic from "@anthropic-ai/sdk";
import Fastify from "fastify";
import { z } from "zod";

export {};

const ChatRequest = z.object({ message: z.string().min(1) });
const server = Fastify({ logger: true });

server.get("/health", async () => ({ status: "ok" }));

server.post("/chat", async (request, reply) => {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return reply.code(500).send({ error: "ANTHROPIC_API_KEY no configurada." });

  const payload = ChatRequest.parse(request.body);
  const client = new Anthropic({ apiKey });
  const response = await client.messages.create({
    model: "claude-3-5-sonnet-latest",
    max_tokens: 500,
    messages: [{ role: "user", content: payload.message }],
  });
  const answer = response.content.filter((block) => block.type === "text").map((block) => block.text).join("");
  return { answer };
});

await server.listen({ port: Number(process.env.PORT ?? 3000), host: "0.0.0.0" });
