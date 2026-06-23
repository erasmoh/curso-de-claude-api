import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam, ToolResultBlockParam, ToolUnion } from "@anthropic-ai/sdk/resources/messages";
import Fastify from "fastify";
import type { FastifyReply } from "fastify";
import { z } from "zod";

export {};

const MODEL = "claude-sonnet-4-6";
const MAX_AGENT_STEPS = 4;

const ChatRequest = z.object({ message: z.string().min(1) });
const ExtractRequest = z.object({ text: z.string().min(1) });
const AgentRequest = z.object({ question: z.string().min(1) });
const CalculatorInput = z.object({ expression: z.string() });
const InvoiceData = z.object({
  provider: z.string(),
  date: z.string(),
  currency: z.string(),
  total: z.number(),
  items: z.array(z.object({
    description: z.string(),
    quantity: z.number().nullable().optional(),
    unit_price: z.number().nullable().optional(),
    total: z.number(),
  })),
});

const invoicePrompt = `
Extrae la información de la factura.
Responde únicamente JSON válido con provider, date, currency, total e items.
No agregues explicación fuera del JSON.
`;

const calculatorTool: ToolUnion = {
  name: "calculator",
  description: "Calculadora aritmética para sumas, restas, multiplicaciones y divisiones.",
  input_schema: {
    type: "object",
    properties: { expression: { type: "string" } },
    required: ["expression"],
  },
};

const indexHtml = `<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Claude API Hub</title>
    <style>
      :root { color-scheme: light; font-family: Inter, ui-sans-serif, system-ui, sans-serif; background: #eef2ff; color: #172033; }
      body { margin: 0; }
      main { width: min(1120px, calc(100% - 32px)); margin: 0 auto; padding: 40px 0; }
      header { background: linear-gradient(135deg, #172033, #5b4bff); border-radius: 28px; color: white; padding: 32px; }
      h1 { font-size: clamp(2rem, 5vw, 4rem); line-height: 1; margin: 0 0 12px; }
      .grid { display: grid; gap: 20px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); margin-top: 24px; }
      section { background: rgba(255, 255, 255, 0.88); border: 1px solid rgba(91, 75, 255, 0.14); border-radius: 24px; padding: 22px; }
      label { display: block; font-weight: 700; margin-bottom: 8px; }
      textarea, input { width: 100%; border: 1px solid #c7d2fe; border-radius: 16px; box-sizing: border-box; font: inherit; min-height: 120px; padding: 14px; resize: vertical; }
      input { min-height: 0; }
      button { background: #5b4bff; border: 0; border-radius: 999px; color: white; cursor: pointer; font-weight: 800; margin-top: 12px; padding: 12px 18px; }
      pre { background: #0f172a; border-radius: 18px; color: #dbeafe; min-height: 120px; overflow: auto; padding: 16px; white-space: pre-wrap; }
    </style>
  </head>
  <body>
    <main>
      <header>
        <p>Clase 17 · Frontend + Fastify</p>
        <h1>Todos los proyectos del curso en una sola app</h1>
        <p>Un frontend llama tres endpoints: chatbot, extractor JSON y agente con herramienta calculadora.</p>
      </header>
      <div class="grid">
        <section>
          <h2>Chatbot</h2>
          <label for="chat-message">Mensaje</label>
          <textarea id="chat-message">Dame 3 ideas para practicar Claude API.</textarea>
          <button data-run="chat">Enviar</button>
          <pre id="chat-output">Respuesta pendiente...</pre>
        </section>
        <section>
          <h2>Extractor JSON</h2>
          <label for="invoice-text">Factura</label>
          <textarea id="invoice-text">Factura de ACME S.A. emitida el 2026-05-01. 2 horas de consultoría a 50 USD cada una. Total: USD 100.</textarea>
          <button data-run="extract">Extraer</button>
          <pre id="extract-output">JSON pendiente...</pre>
        </section>
        <section>
          <h2>Agente con tools</h2>
          <label for="agent-question">Pregunta</label>
          <input id="agent-question" value="Calcula (128 * 7) + 34 y explica el resultado." />
          <button data-run="agent">Resolver</button>
          <pre id="agent-output">Respuesta pendiente...</pre>
        </section>
      </div>
    </main>
    <script>
      async function postJson(path, body) {
        const response = await fetch(path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || JSON.stringify(data));
        return data;
      }
      function show(id, value) {
        document.getElementById(id).textContent = typeof value === 'string' ? value : JSON.stringify(value, null, 2);
      }
      document.querySelector('[data-run="chat"]').addEventListener('click', async () => {
        show('chat-output', 'Cargando...');
        try { const data = await postJson('/api/chat', { message: document.getElementById('chat-message').value }); show('chat-output', data.reply); } catch (error) { show('chat-output', error.message); }
      });
      document.querySelector('[data-run="extract"]').addEventListener('click', async () => {
        show('extract-output', 'Cargando...');
        try { const data = await postJson('/api/extract', { text: document.getElementById('invoice-text').value }); show('extract-output', data.data); } catch (error) { show('extract-output', error.message); }
      });
      document.querySelector('[data-run="agent"]').addEventListener('click', async () => {
        show('agent-output', 'Cargando...');
        try { const data = await postJson('/api/agent', { question: document.getElementById('agent-question').value }); show('agent-output', data); } catch (error) { show('agent-output', error.message); }
      });
    </script>
  </body>
</html>`;

type TextBlockLike = { type: string; text?: string };

function createClient(): Anthropic {
  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) throw new Error("ANTHROPIC_API_KEY no configurada.");
  return new Anthropic({ apiKey });
}

function responseText(content: TextBlockLike[]): string {
  return content
    .filter((block): block is { type: string; text: string } => block.type === "text" && typeof block.text === "string")
    .map((block) => block.text)
    .join("");
}

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

function sendError(reply: FastifyReply, error: unknown) {
  const message = error instanceof Error ? error.message : "Error inesperado.";
  return reply.code(500).send({ error: message });
}

const server = Fastify({ logger: true });

server.get("/", async (_request, reply) => reply.type("text/html").send(indexHtml));
server.get("/health", async () => ({ status: "ok" }));

server.post("/api/chat", async (request, reply) => {
  try {
    const payload = ChatRequest.parse(request.body);
    const response = await createClient().messages.create({
      model: MODEL,
      max_tokens: 700,
      messages: [{ role: "user", content: payload.message }],
    });
    return { reply: responseText(response.content) };
  } catch (error) {
    return sendError(reply, error);
  }
});

server.post("/api/extract", async (request, reply) => {
  try {
    const payload = ExtractRequest.parse(request.body);
    const response = await createClient().messages.create({
      model: MODEL,
      max_tokens: 700,
      system: invoicePrompt,
      messages: [{ role: "user", content: payload.text }],
    });
    return { data: InvoiceData.parse(JSON.parse(responseText(response.content))) };
  } catch (error) {
    return sendError(reply, error);
  }
});

server.post("/api/agent", async (request, reply) => {
  try {
    const payload = AgentRequest.parse(request.body);
    const client = createClient();
    const messages: MessageParam[] = [{ role: "user", content: payload.question }];
    const steps: string[] = [];

    for (let step = 0; step < MAX_AGENT_STEPS; step += 1) {
      const response = await client.messages.create({
        model: MODEL,
        max_tokens: 700,
        tools: [calculatorTool],
        messages,
      });
      messages.push({ role: "assistant", content: response.content });
      const toolResults: ToolResultBlockParam[] = [];

      for (const block of response.content) {
        if (block.type === "tool_use" && block.name === "calculator") {
          const parsed = CalculatorInput.safeParse(block.input);
          const expression = parsed.success ? parsed.data.expression : "";
          const result = calculator(expression);
          steps.push(`calculator(${expression}) -> ${result}`);
          toolResults.push({ type: "tool_result", tool_use_id: block.id, content: result });
        }
      }

      if (toolResults.length === 0) {
        return { answer: responseText(response.content), steps };
      }
      messages.push({ role: "user", content: toolResults });
    }

    return reply.code(504).send({ error: "El agente alcanzó el límite de pasos." });
  } catch (error) {
    return sendError(reply, error);
  }
});

await server.listen({ port: Number(process.env.PORT ?? 3000), host: "0.0.0.0" });
