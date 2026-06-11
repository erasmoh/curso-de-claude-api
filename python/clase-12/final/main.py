"""Runner seguro para agentes con allowlist, errores y límite de pasos."""

from __future__ import annotations

from collections.abc import Callable

MAX_STEPS = 5


def get_weather(city: str) -> str:
    return f"Clima en {city}: lluvia ligera."


available_tools: dict[str, Callable[..., str]] = {"get_weather": get_weather}


def run_tool(name: str, args: dict[str, object]) -> str:
    if name not in available_tools:
        return "Error: herramienta no permitida."

    try:
        return str(available_tools[name](**args))
    except Exception as error:
        return f"Error ejecutando {name}: {error}"


def main() -> None:
    for step in range(MAX_STEPS):
        if step == MAX_STEPS - 1:
            print("El agente alcanzó el máximo de pasos permitidos.")
            break
        print(run_tool("get_weather", {"city": "Bogotá"}))
        break

    print("Reglas: allowlist de herramientas, validación de argumentos, max steps y nunca ejecutar código arbitrario.")


if __name__ == "__main__":
    main()
