import Anthropic from "@anthropic-ai/sdk";
import { readFile, writeFile } from "node:fs/promises";
import { InvoiceData } from "./schemas.js";

export {};

const MODEL = "claude-sonnet-4-6";

function getPdfPath(): string {
  const pdfPath = process.argv[2];
  if (!pdfPath) throw new Error("Uso: npm run clase:09:final -- ./samples/factura_001.pdf");
  return pdfPath;
}

async function extractInvoice(client: Anthropic, pdfPath: string): Promise<unknown> {
  const pdfData = (await readFile(pdfPath)).toString("base64");
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 1000,
    system: "Extrae la factura como JSON válido con provider, date, total, currency e items.",
    messages: [{ role: "user", content: [
      { type: "document", source: { type: "base64", media_type: "application/pdf", data: pdfData } },
      { type: "text", text: "Devuelve únicamente JSON válido. No uses Markdown." },
    ] }],
  });
  const rawText = response.content.filter((block) => block.type === "text").map((block) => block.text).join("");
  return InvoiceData.parse(JSON.parse(rawText));
}

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

try {
  const invoice = await extractInvoice(new Anthropic({ apiKey }), getPdfPath());
  await writeFile("output.json", JSON.stringify(invoice, null, 2));
  console.log("Factura extraída en output.json");
} catch (error) {
  console.log(`La factura no pudo procesarse: ${error instanceof Error ? error.message : "error desconocido"}`);
  process.exitCode = 1;
}
