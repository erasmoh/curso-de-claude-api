/**
 * Clase 17 - inicio: Frontend y hub de proyectos con Fastify.
 *
 * Adaptación TypeScript del hub web. Ejecuta con npm run clase:17:inicio.
 */

import Fastify from "fastify";
import { z } from "zod";

export {};

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

await server.listen({ port: Number(process.env.PORT ?? 3000), host: "0.0.0.0" });
