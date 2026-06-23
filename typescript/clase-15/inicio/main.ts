/**
 * Clase 15 - inicio: Frontend + hub de proyectos con Fastify.
 *
 * Punto de partida que combina dos cosas:
 * 1. Lo último de la clase 14 (Batch API) como referencia para continuidad.
 * 2. El esqueleto del hub web que completaremos en vivo durante la clase.
 *
 * Ejecuta el frontend con: npm run clase:15:inicio
 */

import Anthropic from "@anthropic-ai/sdk";
import Fastify from "fastify";
import { z } from "zod";

export {};

const MODEL = "claude-sonnet-4-6";

// ===== Parte 1: Lo último de la clase 14 (Batch API) - referencia =====
async function demoBatch(): Promise<void> {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

  const client = new Anthropic({ apiKey });
  const batch = await client.messages.batches.create({
    requests: [{
      custom_id: "invoice-001",
      params: {
        model: MODEL,
        max_tokens: 500,
        messages: [{ role: "user", content: "Resume esta factura de ejemplo." }],
      },
    }],
  });

  console.log(batch.id, batch.processing_status);
  const batchStatus = await client.messages.batches.retrieve(batch.id);
  console.log(batchStatus.processing_status);

  if (batchStatus.processing_status === "ended") {
    const results = await client.messages.batches.results(batch.id);
    for await (const result of results) {
      console.log(result.custom_id, result.result.type);
    }
  } else {
    console.log("El batch todavía no termina. Vuelve a consultar más tarde antes de leer results.");
  }
}

void demoBatch;

// ===== Parte 2: Nuevo - esqueleto del hub frontend (a completar en vivo) =====
const ChatRequest = z.object({ message: z.string().min(1) });
const server = Fastify({ logger: true });

const indexHtml = `<!doctype html>
<html lang="es">
  <head><meta charset="utf-8" /><title>Claude API Hub</title></head>
  <body>
    <main>
      <h1>Claude API Hub</h1>
      <p>TODO: diseña el frontend y conecta /api/chat, /api/extract y /api/agent.</p>
    </main>
  </body>
</html>`;

server.get("/", async (_request, reply) => reply.type("text/html").send(indexHtml));
server.get("/health", async () => ({ status: "ok" }));

server.post("/api/chat", async (request) => {
  const payload = ChatRequest.parse(request.body);
  return { reply: `TODO: conectar Claude para: ${payload.message}` };
});

// TODO: agrega /api/extract (clase 07) y /api/agent (clase 11).
await server.listen({ port: Number(process.env.PORT ?? 3000), host: "0.0.0.0" });
