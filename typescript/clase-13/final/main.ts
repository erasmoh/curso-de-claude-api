export {};

const ALLOWED_DOMAINS = new Set(["docs.anthropic.com", "www.anthropic.com"]);

function validateUrl(rawUrl: string): string {
  const url = new URL(rawUrl);
  if (url.protocol !== "https:") throw new Error("Solo se permite HTTPS.");
  if (!ALLOWED_DOMAINS.has(url.hostname)) throw new Error(`Dominio no permitido: ${url.hostname}`);
  return url.toString();
}

const safeUrl = validateUrl("https://docs.anthropic.com/en/api/messages");
console.log(`URL validada para la herramienta fetch: ${safeUrl}`);
console.log("En el agente real, combina esta validación con MAX_STEPS y timeouts.");
