import Anthropic from "@anthropic-ai/sdk";
import { readFile } from "node:fs/promises";
import { z } from "zod";

export {};

const Invoice = z.object({
  provider: z.string().nullable(),
  date: z.string().nullable(),
  total: z.number().nullable(),
  currency: z.string().nullable(),
  items: z.array(z.object({ description: z.string(), quantity: z.number(), unit_price: z.number() })),
});

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const pdfData = (await readFile("invoice.pdf")).toString("base64");
const client = new Anthropic({ apiKey });
const response = await client.messages.create({
  model: "claude-3-5-sonnet-latest",
  max_tokens: 900,
  system: "Extrae factura como JSON válido. No agregues Markdown.",
  messages: [{ role: "user", content: [
    { type: "document", source: { type: "base64", media_type: "application/pdf", data: pdfData } },
    { type: "text", text: "Campos: provider, date, total, currency, items[]." },
  ] }],
});

const rawText = response.content.filter((block) => block.type === "text").map((block) => block.text).join("");
console.log(JSON.stringify(Invoice.parse(JSON.parse(rawText)), null, 2));
