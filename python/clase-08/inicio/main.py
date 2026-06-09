"""Clase 08 - inicio: Prompt engineering para extracción de datos.

Este archivo es el punto de partida de la clase. Está lleno de pistas y
TODOs para que el estudiante escriba el código durante la explicación.
"""

import os


MODEL = "claude-3-5-sonnet-latest"


def main() -> None:
    """Completa este ejercicio durante la clase."""
    api_key = os.getenv("ANTHROPIC_API_KEY")

    # TODO 1: valida que exista ANTHROPIC_API_KEY antes de llamar a la API.
    # TODO 2: crea el cliente de Anthropic.
    # TODO 3: envía el mensaje principal de esta clase.
    # TODO 4: imprime la respuesta de Claude en la terminal.
    print("Inicio de la clase 08. Configura el ejercicio aquí.")
    if not api_key:
        print("Tip: exporta ANTHROPIC_API_KEY antes de ejecutar el ejemplo.")


if __name__ == "__main__":
    main()
