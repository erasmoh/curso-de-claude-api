export {};

const MAX_STEPS = 5;

function getWeather(city: string): string {
  return `Clima en ${city}: lluvia ligera.`;
}

const availableTools = {
  get_weather: (args: Record<string, unknown>): string => {
    const city = typeof args.city === "string" ? args.city : "ciudad desconocida";
    return getWeather(city);
  },
};

function runTool(name: string, args: Record<string, unknown>): string {
  if (name !== "get_weather") return "Error: herramienta no permitida.";

  try {
    return availableTools.get_weather(args);
  } catch (error) {
    return `Error ejecutando ${name}: ${error instanceof Error ? error.message : "desconocido"}`;
  }
}

for (let step = 0; step < MAX_STEPS; step += 1) {
  if (step === MAX_STEPS - 1) {
    console.log("El agente alcanzó el máximo de pasos permitidos.");
    break;
  }
  console.log(runTool("get_weather", { city: "Bogotá" }));
  break;
}

console.log("Reglas: allowlist de herramientas, validación de argumentos, max steps y nunca ejecutar código arbitrario.");
