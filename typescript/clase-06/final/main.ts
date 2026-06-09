import Anthropic from "@anthropic-ai/sdk";
import { readFile } from "node:fs/promises";

export {};

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const pdfBuffer = await readFile("sample.pdf");
const pdfData = pdfBuffer.toString("base64");
const client = new Anthropic({ apiKey });

const response = await client.messages.create({
  model: "claude-3-5-sonnet-latest",
  max_tokens: 500,
  messages: [{
    role: "user",
    content: [
      { type: "document", source: { type: "base64", media_type: "application/pdf", data: pdfData } },
      { type: "text", text: "Resume el contenido principal en 5 bullets." },
    ],
  }],
});

for (const block of response.content) {
  if (block.type === "text") console.log(block.text);
}
