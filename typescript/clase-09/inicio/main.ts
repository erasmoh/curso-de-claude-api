/**
 * Clase 09 - inicio: Tool use: cómo Claude llama funciones externas.
 *
 * Punto de partida para resolver en vivo. Mantiene comentarios explícitos
 * para que el estudiante entienda qué parte debe completar.
 */

export {};

const MODEL = "claude-sonnet-4-6";

async function main(): Promise<void> {
  const apiKey = process.env.ANTHROPIC_API_KEY;

  // TODO 1: valida que exista ANTHROPIC_API_KEY.
  // TODO 2: crea el cliente de Anthropic.
  // TODO 3: envía el mensaje principal de esta clase.
  // TODO 4: imprime la respuesta en consola.
  console.log("Inicio de la clase 09. Configura el ejercicio aquí.");
  if (!apiKey) {
    console.log("Tip: exporta ANTHROPIC_API_KEY antes de ejecutar el ejemplo.");
  }

  void MODEL;
}

await main();
