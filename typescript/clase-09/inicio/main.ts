/**
 * Clase 09 - inicio: Construye un extractor de facturas en PDF.
 *
 * Punto de partida para resolver en vivo. Mantiene comentarios explícitos
 * para que el estudiante entienda qué parte debe completar.
 */

export {};

const MODEL = "claude-3-5-sonnet-latest";

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
