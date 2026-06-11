import Anthropic from "@anthropic-ai/sdk";
import { z } from "zod";

export {};

const MODEL = "claude-sonnet-4-6";
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

const prompt = `
Extrae la información de la factura.
Responde únicamente JSON válido.
No agregues explicación fuera del JSON.
`;

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const invoiceText = "Factura de ACME S.A. emitida el 2026-05-01. 2 horas de consultoría a 50 USD cada una. Total: USD 100.";
const client = new Anthropic({ apiKey });
const response = await client.messages.create({
  model: MODEL,
  max_tokens: 500,
  system: prompt,
  messages: [{ role: "user", content: invoiceText }],
});

const rawText = response.content.filter((block) => block.type === "text").map((block) => block.text).join("");
console.log(JSON.stringify(InvoiceData.parse(JSON.parse(rawText)), null, 2));
