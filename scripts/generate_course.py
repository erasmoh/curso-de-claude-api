from __future__ import annotations

from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]


CLASSES = [
    (1, "Quickstart: tu primera llamada a Claude API", "Instalar el SDK, leer ANTHROPIC_API_KEY y hacer una primera request."),
    (2, "Conversaciones multi-turn: el array de messages", "Mantener historial explícito con roles user y assistant."),
    (3, "Estrategias de gestión de contexto y tokens", "Controlar costo y contexto con truncado, resumen y max_tokens."),
    (4, "Streaming de respuestas en tiempo real", "Mostrar texto incrementalmente mientras Claude responde."),
    (5, "Construye el chatbot con interfaz de terminal", "Unir historial, persistencia, streaming y manejo de errores."),
    (6, "Inputs multimedia: imágenes y documentos PDF", "Enviar imágenes y PDFs como bloques image/document."),
    (7, "Outputs estructurados con JSON mode", "Forzar JSON válido y validarlo con Pydantic/Zod."),
    (8, "Prompt engineering para extracción de datos", "Diseñar instrucciones robustas para documentos ambiguos."),
    (9, "Construye un extractor de facturas en PDF", "Procesar una factura PDF y devolver JSON validado."),
    (10, "Tool use: cómo Claude llama funciones externas", "Declarar herramientas y detectar bloques tool_use."),
    (11, "Definir herramientas y manejar tool_result", "Ejecutar una función local y devolver su resultado a Claude."),
    (12, "Loop agentico: razonar → actuar → observar", "Implementar el ciclo while de un agente con herramientas."),
    (13, "Manejo de errores y seguridad en agentes", "Limitar pasos, validar inputs y evitar loops peligrosos."),
    (14, "Construye un agente de búsqueda y resumen web", "Investigar una pregunta y responder con fuentes citadas."),
    (15, "Prompt caching: reduce costos hasta un 90%", "Marcar contenido reusable con cache_control."),
    (16, "Batch API para procesar miles de requests", "Crear batches, consultar estado y leer resultados."),
    (17, "Rate limits, reintentos y observabilidad", "Aplicar backoff, logs estructurados y métricas de tokens."),
    (18, "Deploy tu app con FastAPI + Railway", "Exponer el chatbot como API REST lista para Railway."),
]


def write(path: str, content: str) -> None:
    file_path = ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(dedent(content).strip() + "\n", encoding="utf-8")


def py_starter(number: int, title: str) -> str:
    return f'''
    """Clase {number:02d} - inicio: {title}.

    Este archivo es el punto de partida de la clase. Está lleno de pistas y
    TODOs para que el estudiante escriba el código durante la explicación.
    """

    import os


    MODEL = "claude-sonnet-4-6"


    def main() -> None:
        """Completa este ejercicio durante la clase."""
        api_key = os.getenv("ANTHROPIC_API_KEY")

        # TODO 1: valida que exista ANTHROPIC_API_KEY antes de llamar a la API.
        # TODO 2: crea el cliente de Anthropic.
        # TODO 3: envía el mensaje principal de esta clase.
        # TODO 4: imprime la respuesta de Claude en la terminal.
        print("Inicio de la clase {number:02d}. Configura el ejercicio aquí.")
        if not api_key:
            print("Tip: exporta ANTHROPIC_API_KEY antes de ejecutar el ejemplo.")


    if __name__ == "__main__":
        main()
    '''


def ts_starter(number: int, title: str) -> str:
    return f'''
    /**
     * Clase {number:02d} - inicio: {title}.
     *
     * Punto de partida para resolver en vivo. Mantiene comentarios explícitos
     * para que el estudiante entienda qué parte debe completar.
     */

    export {{}};

    const MODEL = "claude-sonnet-4-6";

    async function main(): Promise<void> {{
      const apiKey = process.env.ANTHROPIC_API_KEY;

      // TODO 1: valida que exista ANTHROPIC_API_KEY.
      // TODO 2: crea el cliente de Anthropic.
      // TODO 3: envía el mensaje principal de esta clase.
      // TODO 4: imprime la respuesta en consola.
      console.log("Inicio de la clase {number:02d}. Configura el ejercicio aquí.");
      if (!apiKey) {{
        console.log("Tip: exporta ANTHROPIC_API_KEY antes de ejecutar el ejemplo.");
      }}

      void MODEL;
    }}

    await main();
    '''


PY_FINALS = {
    1: '''
    """Primera llamada real a Claude API con Python."""

    import os
    from anthropic import Anthropic

    MODEL = "claude-sonnet-4-6"


    def require_api_key() -> str:
        """Lee la API key desde el entorno para no escribir secretos en código."""
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY antes de ejecutar este script.")
        return api_key


    def main() -> None:
        client = Anthropic(api_key=require_api_key())
        message = client.messages.create(
            model=MODEL,
            max_tokens=300,
            system="Responde como un mentor breve y práctico de Python.",
            messages=[{"role": "user", "content": "Dame 3 ideas para practicar Claude API."}],
        )

        for block in message.content:
            if block.type == "text":
                print(block.text)


    if __name__ == "__main__":
        main()
    ''',
    2: '''
    """Conversación multi-turn: el cliente guarda y reenvía el historial."""

    import os
    from anthropic import Anthropic

    MODEL = "claude-sonnet-4-6"


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        client = Anthropic(api_key=api_key)
        messages = [
            {"role": "user", "content": "Mi proyecto será un chatbot para recetas."},
            {"role": "assistant", "content": "Perfecto. Puedo ayudarte con ingredientes y pasos."},
            {"role": "user", "content": "Recuérdame cuál era mi proyecto y sugiere el primer feature."},
        ]

        response = client.messages.create(model=MODEL, max_tokens=400, messages=messages)
        for block in response.content:
            if block.type == "text":
                print(block.text)


    if __name__ == "__main__":
        main()
    ''',
    3: '''
"""Estrategias de contexto: truncado, resumen y uso de tokens."""

from __future__ import annotations

import os
from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"
MAX_HISTORY_MESSAGES = 12


def keep_recent_messages(messages: list[dict[str, str]], max_messages: int = MAX_HISTORY_MESSAGES) -> list[dict[str, str]]:
    """Conserva solo los últimos turnos para controlar latencia, contexto y costo."""
    return messages[-max_messages:]


def summarize_history(client: Anthropic, messages: list[dict[str, str]]) -> str:
    """Resume la conversación cuando ya no conviene enviar todo el historial."""
    transcript = "\\n".join(f"{message['role']}: {message['content']}" for message in messages)
    response = client.messages.create(
        model=MODEL,
        max_tokens=400,
        system="Resume una conversación para preservar contexto importante.",
        messages=[{"role": "user", "content": transcript}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    messages = [
        {"role": "user", "content": "Estoy creando un chatbot para soporte técnico."},
        {"role": "assistant", "content": "Perfecto. Lo enfocaremos en respuestas claras."},
        {"role": "user", "content": "El bot debe escalar casos urgentes."},
    ]

    summary = summarize_history(client, messages)
    controlled_history = [{"role": "user", "content": f"Resumen previo: {summary}"}]
    controlled_history.extend(keep_recent_messages(messages))
    controlled_history.append({"role": "user", "content": "¿Qué decisión importante debo recordar?"})

    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        messages=controlled_history,
    )

    print("Respuesta:")
    print("".join(block.text for block in response.content if block.type == "text"))
    print("\\nUso de tokens:")
    print({"input_tokens": response.usage.input_tokens, "output_tokens": response.usage.output_tokens})


if __name__ == "__main__":
    main()
    ''',
    4: '''
    """Streaming: imprime la respuesta conforme llega desde Claude."""

    import os
    from anthropic import Anthropic

    MODEL = "claude-sonnet-4-6"


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        client = Anthropic(api_key=api_key)
        with client.messages.stream(
            model=MODEL,
            max_tokens=500,
            messages=[{"role": "user", "content": "Explícame streaming en Claude API con una analogía."}],
        ) as stream:
            for text in stream.text_stream:
                print(text, end="", flush=True)
        print()


    if __name__ == "__main__":
        main()
    ''',
    5: '''
"""Chatbot de terminal con historial persistente, comandos, errores y streaming."""

from __future__ import annotations

import json
import os
from pathlib import Path
from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"
HISTORY_PATH = Path("history.json")


def load_history() -> list[dict[str, str]]:
    if HISTORY_PATH.exists():
        return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    return []


def save_history(messages: list[dict[str, str]]) -> None:
    HISTORY_PATH.write_text(json.dumps(messages, indent=2, ensure_ascii=False), encoding="utf-8")


def stream_claude_response(client: Anthropic, messages: list[dict[str, str]]) -> str:
    assistant_text = ""
    with client.messages.stream(model=MODEL, max_tokens=700, messages=messages[-12:]) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
            assistant_text += text
    print()
    return assistant_text


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    messages = load_history()
    print("Chatbot listo. Comandos: /salir para terminar, /reset para borrar historial.")

    while True:
        user_input = input("\\nTú: ").strip()

        if user_input == "/salir":
            break
        if user_input == "/reset":
            messages = []
            save_history(messages)
            print("Historial reiniciado.")
            continue
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        print("Claude: ", end="", flush=True)

        try:
            assistant_text = stream_claude_response(client, messages)
        except Exception as error:
            messages.pop()
            print(f"Error llamando a Claude: {error}")
            continue

        messages.append({"role": "assistant", "content": assistant_text})
        save_history(messages)


if __name__ == "__main__":
    main()
    ''',
    6: '''
    """Enviar imágenes o PDFs a Claude como bloques multimedia."""

    from __future__ import annotations

    import base64
    import mimetypes
    import os
    from pathlib import Path
    from anthropic import Anthropic

    MODEL = "claude-sonnet-4-6"


    def encode_file(path: Path) -> tuple[str, str]:
        media_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        data = base64.b64encode(path.read_bytes()).decode("utf-8")
        return media_type, data


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        file_path = Path("sample.pdf")
        if not file_path.exists():
            raise FileNotFoundError("Agrega un archivo sample.pdf junto a este script.")

        media_type, data = encode_file(file_path)
        content_type = "document" if media_type == "application/pdf" else "image"

        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": [
                    {"type": content_type, "source": {"type": "base64", "media_type": media_type, "data": data}},
                    {"type": "text", "text": "Resume el contenido principal en 5 bullets."},
                ],
            }],
        )

        for block in response.content:
            if block.type == "text":
                print(block.text)


    if __name__ == "__main__":
        main()
    ''',
    7: '''
"""JSON estructurado para facturas con prompt estricto y validación Pydantic."""

from __future__ import annotations

import json
import os
from anthropic import Anthropic
from pydantic import BaseModel

MODEL = "claude-sonnet-4-6"


class InvoiceItem(BaseModel):
    description: str
    quantity: float | None = None
    unit_price: float | None = None
    total: float


class InvoiceData(BaseModel):
    provider: str
    date: str
    currency: str
    total: float
    items: list[InvoiceItem]


PROMPT = """
Extrae la información de la factura.
Responde únicamente JSON válido.
No agregues explicación fuera del JSON.
"""


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    invoice_text = """
    Factura de ACME S.A. emitida el 2026-05-01.
    2 horas de consultoría a 50 USD cada una. Total: USD 100.
    """
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        system=PROMPT,
        messages=[{"role": "user", "content": invoice_text}],
    )

    raw_text = "".join(block.text for block in response.content if block.type == "text")
    invoice = InvoiceData.model_validate(json.loads(raw_text))
    print(invoice.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
    ''',
    8: '''
"""Prompt engineering para extracción precisa de datos de facturas."""

import os
from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"

EXTRACTION_PROMPT = """
Extrae datos de la factura adjunta.
Responde únicamente JSON válido.
No inventes datos. Si un campo no aparece, usa null.
Normaliza montos como números, sin símbolos de moneda.
La moneda debe ser un código ISO si puedes inferirlo.

Campos requeridos:
- provider
- date
- currency
- total
- items: description, quantity, unit_price, total

Ejemplos de reglas:
- Si la factura no muestra moneda explícita, usa null.
- Si hay impuestos separados, inclúyelos en items solo si aparecen como línea propia.
- Si no puedes leer un campo, usa null en lugar de adivinar.
"""


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    document_text = "Factura ACME emitida el 2026-05-01. Servicio: soporte, total: USD 129.90"
    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=700,
        system=EXTRACTION_PROMPT,
        messages=[{"role": "user", "content": document_text}],
    )

    for block in response.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
    ''',
    9: '''
"""Extractor de facturas PDF con CLI, validación y salida output.json."""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
from anthropic import Anthropic
from schemas import InvoiceData

MODEL = "claude-sonnet-4-6"
OUTPUT_PATH = Path("output.json")


def to_base64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def parse_and_validate(raw_text: str) -> InvoiceData:
    return InvoiceData.model_validate(json.loads(raw_text))


def extract_invoice(client: Anthropic, pdf_path: Path) -> InvoiceData:
    pdf_data = to_base64(pdf_path)
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system="Extrae la factura como JSON válido con provider, date, total, currency e items.",
        messages=[{"role": "user", "content": [
            {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_data}},
            {"type": "text", "text": "Devuelve únicamente JSON válido. No uses Markdown."},
        ]}],
    )
    raw_text = "".join(block.text for block in response.content if block.type == "text")
    return parse_and_validate(raw_text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extrae datos de una factura PDF con Claude API.")
    parser.add_argument("pdf_path", type=Path, help="Ruta al PDF de factura. Ej: ./samples/factura_001.pdf")
    args = parser.parse_args()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    try:
        invoice = extract_invoice(Anthropic(api_key=api_key), args.pdf_path)
    except FileNotFoundError:
        print("No encontramos el archivo PDF.")
        raise SystemExit(1)
    except (json.JSONDecodeError, ValueError) as error:
        print(f"La respuesta no pudo validarse: {error}")
        raise SystemExit(1)

    OUTPUT_PATH.write_text(json.dumps(invoice.model_dump(), indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Factura extraída en {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
    ''',
    10: '''
    """Tool use: Claude solicita una función externa mediante tool_use."""

    import os
    from anthropic import Anthropic

    MODEL = "claude-sonnet-4-6"

    WEATHER_TOOL = {
        "name": "get_weather",
        "description": "Obtiene el clima actual para una ciudad.",
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string", "description": "Ciudad a consultar."}},
            "required": ["city"],
        },
    }


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=400,
            tools=[WEATHER_TOOL],
            messages=[{"role": "user", "content": "¿Cómo está el clima en Guatemala?"}],
        )

        for block in response.content:
            if block.type == "tool_use":
                print(f"Claude quiere usar {block.name} con input: {block.input}")
            elif block.type == "text":
                print(block.text)


    if __name__ == "__main__":
        main()
    ''',
    11: '''
"""Ejecutar herramientas permitidas y responder a Claude con tool_result."""

from __future__ import annotations

import json
import os
from collections.abc import Callable
from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"


def get_weather(city: str) -> dict[str, object]:
    return {"city": city, "temperature": 18, "condition": "lluvia ligera"}


available_tools: dict[str, Callable[..., dict[str, object]]] = {"get_weather": get_weather}


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    tools = [{
        "name": "get_weather",
        "description": "Obtiene el clima actual de una ciudad.",
        "input_schema": {"type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]},
    }]
    client = Anthropic(api_key=api_key)
    messages = [{"role": "user", "content": "¿Necesito paraguas hoy en Bogotá?"}]
    response = client.messages.create(model=MODEL, max_tokens=800, tools=tools, messages=messages)

    messages.append({"role": "assistant", "content": response.content})
    for block in response.content:
        if block.type == "tool_use":
            tool = available_tools[block.name]
            result = tool(**block.input)
            messages.append({"role": "user", "content": [{
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result, ensure_ascii=False),
            }]})

    final = client.messages.create(model=MODEL, max_tokens=500, messages=messages)
    print("".join(block.text for block in final.content if block.type == "text"))


if __name__ == "__main__":
    main()
    ''',
    12: '''
    """Loop agentico: razonar, actuar, observar y decidir si termina."""

    from __future__ import annotations

    import ast
    import operator
    import os
    from anthropic import Anthropic

    MODEL = "claude-sonnet-4-6"
    MAX_STEPS = 4
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
    }


    def evaluate(node: ast.AST) -> float:
        if isinstance(node, ast.Expression):
            return evaluate(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, int | float):
            return float(node.value)
        if isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](evaluate(node.left), evaluate(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
            return OPERATORS[type(node.op)](evaluate(node.operand))
        raise ValueError("Expresión no permitida.")


    def calculator(expression: str) -> str:
        try:
            tree = ast.parse(expression, mode="eval")
            return str(evaluate(tree))
        except (SyntaxError, ValueError, ZeroDivisionError) as error:
            return f"Expresión rechazada: {error}"


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        client = Anthropic(api_key=api_key)
        messages = [{"role": "user", "content": "Calcula (128 * 7) + 34 y explica el resultado."}]
        tools = [{"name": "calculator", "description": "Calculadora aritmética.", "input_schema": {
            "type": "object", "properties": {"expression": {"type": "string"}}, "required": ["expression"]}}]

        for _step in range(MAX_STEPS):
            response = client.messages.create(model=MODEL, max_tokens=500, tools=tools, messages=messages)
            messages.append({"role": "assistant", "content": response.content})
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_results.append({"type": "tool_result", "tool_use_id": block.id, "content": calculator(str(block.input["expression"]))})
            if not tool_results:
                print("".join(block.text for block in response.content if block.type == "text"))
                return
            messages.append({"role": "user", "content": tool_results})

        print("El agente alcanzó el límite de pasos.")


    if __name__ == "__main__":
        main()
    ''',
    13: '''
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
    ''',
    14: '''
"""Agente de búsqueda y resumen web con search_web, read_url y fuentes."""

from __future__ import annotations

import os
from anthropic import Anthropic

MODEL = "claude-sonnet-4-6"
MAX_STEPS = 4

LOCAL_PAGES = {
    "https://docs.anthropic.com/en/api/messages": "La Messages API permite enviar messages, system prompts y herramientas.",
    "https://docs.anthropic.com/en/docs/tool-use": "Tool use permite que Claude solicite funciones externas y reciba tool_result.",
}

TOOLS = [
    {
        "name": "search_web",
        "description": "Busca páginas relevantes para una pregunta.",
        "input_schema": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]},
    },
    {
        "name": "read_url",
        "description": "Lee el contenido textual de una URL.",
        "input_schema": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]},
    },
]


def search_web(query: str) -> str:
    return "\\n".join(f"- {url}" for url in LOCAL_PAGES)


def read_url(url: str) -> str:
    if url not in LOCAL_PAGES:
        return "Fuente no disponible en el set local de la demo."
    return LOCAL_PAGES[url]


def run_tool(name: str, args: dict[str, object]) -> str:
    if name == "search_web":
        query = str(args.get("query", ""))
        return search_web(query)
    if name == "read_url":
        url = str(args.get("url", ""))
        return read_url(url)
    return "Herramienta no permitida."


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    messages = [{"role": "user", "content": "Investiga cómo funciona tool use en Claude API y cita fuentes."}]

    for step in range(MAX_STEPS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=900,
            system="Responde con resumen corto, hallazgos principales, fuentes consultadas y limitaciones.",
            tools=TOOLS,
            messages=messages,
        )
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": run_tool(block.name, block.input),
                })

        if not tool_results:
            print("".join(block.text for block in response.content if block.type == "text"))
            return

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

    print("El agente alcanzó el máximo de pasos sin respuesta final.")


if __name__ == "__main__":
    main()
    ''',
    15: '''
    """Prompt caching: marca instrucciones largas y reutilizables."""

    import os
    from anthropic import Anthropic

    MODEL = "claude-sonnet-4-6"


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        long_policy = "Reglas internas del asistente. " * 400
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=300,
            system=[{"type": "text", "text": long_policy, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": "Resume las 3 reglas principales."}],
        )
        print("".join(block.text for block in response.content if block.type == "text"))
        print(response.usage)


    if __name__ == "__main__":
        main()
    ''',
    16: '''
"""Batch API: crear batch, consultar estado y procesar resultados cuando termine."""

import os
from anthropic import Anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request

MODEL = "claude-sonnet-4-6"


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    batch = client.messages.batches.create(requests=[
        Request(
            custom_id="invoice-001",
            params=MessageCreateParamsNonStreaming(
                model=MODEL,
                max_tokens=500,
                messages=[{"role": "user", "content": "Resume esta factura de ejemplo."}],
            ),
        )
    ])
    print(batch.id, batch.processing_status)

    batch_status = client.messages.batches.retrieve(batch.id)
    print(batch_status.processing_status)

    if batch_status.processing_status == "ended":
        for result in client.messages.batches.results(batch.id):
            print(result.custom_id, result.result.type)
    else:
        print("El batch todavía no termina. Vuelve a consultar más tarde antes de leer results.")


if __name__ == "__main__":
    main()
    ''',
    17: '''
"""Rate limits, reintentos con jitter y observabilidad mínima."""

from __future__ import annotations

import json
import os
import random
import time
from collections.abc import Callable
from typing import TypeVar
from anthropic import Anthropic
from anthropic.types import Message

MODEL = "claude-sonnet-4-6"
T = TypeVar("T")


def retry_with_backoff(fn: Callable[[], T], max_retries: int = 5) -> T:
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as error:
            wait = (2 ** attempt) + random.random()
            print(f"Error: {error}. Reintentando en {wait:.2f}s")
            time.sleep(wait)
    raise RuntimeError("Se agotaron los reintentos")


def safe_claude_call(client: Anthropic, **kwargs: object) -> Message:
    start = time.perf_counter()

    def call() -> Message:
        return client.messages.create(**kwargs)

    response = retry_with_backoff(call)
    elapsed_ms = round((time.perf_counter() - start) * 1000)
    print(json.dumps({
        "model": response.model,
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "elapsed_ms": elapsed_ms,
        "status": "success",
    }, ensure_ascii=False))
    return response


def main() -> None:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("Define ANTHROPIC_API_KEY.")

    client = Anthropic(api_key=api_key)
    response = safe_claude_call(
        client,
        model=MODEL,
        max_tokens=200,
        messages=[{"role": "user", "content": "Dame un tip de observabilidad."}],
    )
    print("".join(block.text for block in response.content if block.type == "text"))


if __name__ == "__main__":
    main()
    ''',
    18: '''
"""API REST con FastAPI, API key de app y variables listas para Railway."""

import os
from anthropic import Anthropic
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

MODEL = "claude-sonnet-4-6"
app = FastAPI(title="Curso Claude API")
APP_API_KEY = os.getenv("APP_API_KEY")


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, x_api_key: str = Header(default="")) -> ChatResponse:
    if not APP_API_KEY:
        raise HTTPException(status_code=500, detail="APP_API_KEY no configurada.")
    if x_api_key != APP_API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY no configurada.")

    client = Anthropic(api_key=api_key)
    response = client.messages.create(
        model=MODEL,
        max_tokens=600,
        messages=[{"role": "user", "content": payload.message}],
    )
    reply = "".join(block.text for block in response.content if block.type == "text")
    return ChatResponse(reply=reply)
    ''',
}










PY_EXTRA_FILES = {
    'python/clase-09/final/schemas.py': '''
from __future__ import annotations

from pydantic import BaseModel


class InvoiceItem(BaseModel):
    description: str
    quantity: float | None = None
    unit_price: float | None = None
    total: float


class InvoiceData(BaseModel):
    provider: str | None
    date: str | None
    currency: str | None
    total: float | None
    items: list[InvoiceItem]
    ''',
    'python/clase-09/final/samples/README.md': '''
# Samples

Coloca aquí `factura_001.pdf` o cualquier factura PDF de prueba antes de ejecutar:

```bash
python python/clase-09/final/main.py python/clase-09/final/samples/factura_001.pdf
```
    ''',
    'python/clase-18/README.md': '''
# Clase 18: Deploy tu app con FastAPI + Railway

**Objetivo:** envolver el chatbot en una API REST con FastAPI, añadir autenticación básica y desplegar en Railway con variables de entorno seguras.

## Estructura

- `inicio/`: punto de partida para resolver durante la clase.
- `final/`: solución con `/health`, `/chat`, header `x-api-key` y `APP_API_KEY`.

## Ejecución local

```bash
export ANTHROPIC_API_KEY="tu_api_key"
export APP_API_KEY="clave_para_tu_app"
uvicorn python.clase-18.final.main:app --reload
```

## Railway

Configura `ANTHROPIC_API_KEY`, `APP_API_KEY` y `PORT` como variables de entorno.
El comando de inicio sugerido es `uvicorn python.clase-18.final.main:app --host 0.0.0.0 --port $PORT`.
    ''',
}


TS_FINALS = {
    1: '''
    import Anthropic from "@anthropic-ai/sdk";

    export {};

    const MODEL = "claude-sonnet-4-6";

    function requireApiKey(): string {
      const apiKey = process.env.ANTHROPIC_API_KEY;
      if (!apiKey) {
        throw new Error("Define ANTHROPIC_API_KEY antes de ejecutar este script.");
      }
      return apiKey;
    }

    async function main(): Promise<void> {
      const client = new Anthropic({ apiKey: requireApiKey() });
      const message = await client.messages.create({
        model: MODEL,
        max_tokens: 300,
        system: "Responde como un mentor breve y práctico de TypeScript.",
        messages: [{ role: "user", content: "Dame 3 ideas para practicar Claude API." }],
      });

      for (const block of message.content) {
        if (block.type === "text") console.log(block.text);
      }
    }

    await main();
    ''',
    2: '''
    import Anthropic from "@anthropic-ai/sdk";

    export {};

    const MODEL = "claude-sonnet-4-6";

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const client = new Anthropic({ apiKey });
    const response = await client.messages.create({
      model: MODEL,
      max_tokens: 400,
      messages: [
        { role: "user", content: "Mi proyecto será un chatbot para recetas." },
        { role: "assistant", content: "Perfecto. Puedo ayudarte con ingredientes y pasos." },
        { role: "user", content: "Recuérdame cuál era mi proyecto y sugiere el primer feature." },
      ],
    });

    for (const block of response.content) {
      if (block.type === "text") console.log(block.text);
    }
    ''',
    3: '''
import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam } from "@anthropic-ai/sdk/resources/messages";

export {};

const MODEL = "claude-sonnet-4-6";
const MAX_HISTORY_MESSAGES = 12;

function keepRecentMessages(messages: MessageParam[], maxMessages = MAX_HISTORY_MESSAGES): MessageParam[] {
  return messages.slice(-maxMessages);
}

async function summarizeHistory(client: Anthropic, messages: MessageParam[]): Promise<string> {
  const transcript = messages.map((message) => `${message.role}: ${message.content}`).join("\\n");
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 400,
    system: "Resume una conversación para preservar contexto importante.",
    messages: [{ role: "user", content: transcript }],
  });
  return response.content.filter((block) => block.type === "text").map((block) => block.text).join("");
}

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const messages: MessageParam[] = [
  { role: "user", content: "Estoy creando un chatbot para soporte técnico." },
  { role: "assistant", content: "Perfecto. Lo enfocaremos en respuestas claras." },
  { role: "user", content: "El bot debe escalar casos urgentes." },
];

const summary = await summarizeHistory(client, messages);
const controlledHistory: MessageParam[] = [{ role: "user", content: `Resumen previo: ${summary}` }, ...keepRecentMessages(messages), { role: "user", content: "¿Qué decisión importante debo recordar?" }];
const response = await client.messages.create({ model: MODEL, max_tokens: 500, messages: controlledHistory });

console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
console.log({ input_tokens: response.usage.input_tokens, output_tokens: response.usage.output_tokens });
    ''',
    4: '''
    import Anthropic from "@anthropic-ai/sdk";

    export {};

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const client = new Anthropic({ apiKey });
    const stream = client.messages.stream({
      model: "claude-sonnet-4-6",
      max_tokens: 500,
      messages: [{ role: "user", content: "Explícame streaming en Claude API con una analogía." }],
    });

    stream.on("text", (text) => process.stdout.write(text));
    await stream.finalMessage();
    process.stdout.write("\\n");
    ''',
    5: '''
import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam } from "@anthropic-ai/sdk/resources/messages";
import { createInterface } from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { readFile, writeFile } from "node:fs/promises";

export {};

const MODEL = "claude-sonnet-4-6";
const HISTORY_PATH = "history.json";

async function loadHistory(): Promise<MessageParam[]> {
  try {
    return JSON.parse(await readFile(HISTORY_PATH, "utf8")) as MessageParam[];
  } catch {
    return [];
  }
}

async function saveHistory(messages: MessageParam[]): Promise<void> {
  await writeFile(HISTORY_PATH, JSON.stringify(messages, null, 2));
}

async function streamClaudeResponse(client: Anthropic, messages: MessageParam[]): Promise<string> {
  let assistantText = "";
  const stream = client.messages.stream({ model: MODEL, max_tokens: 700, messages: messages.slice(-12) });
  stream.on("text", (text) => {
    assistantText += text;
    process.stdout.write(text);
  });
  await stream.finalMessage();
  process.stdout.write("\\n");
  return assistantText;
}

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const rl = createInterface({ input, output });
let messages = await loadHistory();
console.log("Chatbot listo. Comandos: /salir para terminar, /reset para borrar historial.");

while (true) {
  const userInput = (await rl.question("\\nTú: ")).trim();
  if (userInput === "/salir") break;
  if (userInput === "/reset") {
    messages = [];
    await saveHistory(messages);
    console.log("Historial reiniciado.");
    continue;
  }
  if (!userInput) continue;

  messages.push({ role: "user", content: userInput });
  process.stdout.write("Claude: ");
  try {
    const assistantText = await streamClaudeResponse(client, messages);
    messages.push({ role: "assistant", content: assistantText });
    await saveHistory(messages);
  } catch (error) {
    messages.pop();
    console.log(`Error llamando a Claude: ${error instanceof Error ? error.message : "desconocido"}`);
  }
}

rl.close();
    ''',
    6: '''
    import Anthropic from "@anthropic-ai/sdk";
    import { readFile } from "node:fs/promises";

    export {};

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const pdfBuffer = await readFile("sample.pdf");
    const pdfData = pdfBuffer.toString("base64");
    const client = new Anthropic({ apiKey });

    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
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
    ''',
    7: '''
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
    ''',
    8: '''
import Anthropic from "@anthropic-ai/sdk";

export {};

const MODEL = "claude-sonnet-4-6";
const EXTRACTION_PROMPT = `
Extrae datos de la factura adjunta.
Responde únicamente JSON válido.
No inventes datos. Si un campo no aparece, usa null.
Normaliza montos como números, sin símbolos de moneda.
La moneda debe ser un código ISO si puedes inferirlo.

Campos requeridos:
- provider
- date
- currency
- total
- items: description, quantity, unit_price, total

Ejemplos de reglas:
- Si la factura no muestra moneda explícita, usa null.
- Si hay impuestos separados, inclúyelos en items solo si aparecen como línea propia.
- Si no puedes leer un campo, usa null en lugar de adivinar.
`;

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const response = await client.messages.create({
  model: MODEL,
  max_tokens: 700,
  system: EXTRACTION_PROMPT,
  messages: [{ role: "user", content: "Factura ACME emitida el 2026-05-01. Servicio: soporte, total: USD 129.90" }],
});

for (const block of response.content) {
  if (block.type === "text") console.log(block.text);
}
    ''',
    9: '''
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
    ''',
    10: '''
    import Anthropic from "@anthropic-ai/sdk";
    import type { ToolUnion } from "@anthropic-ai/sdk/resources/messages";

    export {};

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const weatherTool: ToolUnion = {
      name: "get_weather",
      description: "Obtiene el clima actual para una ciudad.",
      input_schema: {
        type: "object",
        properties: { city: { type: "string", description: "Ciudad a consultar." } },
        required: ["city"],
      },
    };

    const client = new Anthropic({ apiKey });
    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 400,
      tools: [weatherTool],
      messages: [{ role: "user", content: "¿Cómo está el clima en Guatemala?" }],
    });

    for (const block of response.content) {
      if (block.type === "tool_use") console.log(`Claude quiere usar ${block.name}:`, block.input);
      if (block.type === "text") console.log(block.text);
    }
    ''',
    11: '''
import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam, ToolUnion } from "@anthropic-ai/sdk/resources/messages";

export {};

const MODEL = "claude-sonnet-4-6";

type Weather = { city: string; temperature: number; condition: string };
type ToolInput = Record<string, unknown>;

function getWeather(city: string): Weather {
  return { city, temperature: 18, condition: "lluvia ligera" };
}

const availableTools = {
  get_weather: (input: ToolInput): Weather => {
    const city = typeof input.city === "string" ? input.city : "Bogotá";
    return getWeather(city);
  },
};

const tool: ToolUnion = {
  name: "get_weather",
  description: "Obtiene el clima actual de una ciudad.",
  input_schema: { type: "object", properties: { city: { type: "string" } }, required: ["city"] },
};

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const messages: MessageParam[] = [{ role: "user", content: "¿Necesito paraguas hoy en Bogotá?" }];
const response = await client.messages.create({ model: MODEL, max_tokens: 800, tools: [tool], messages });

messages.push({ role: "assistant", content: response.content });
for (const block of response.content) {
  if (block.type === "tool_use" && block.name === "get_weather") {
    const result = availableTools.get_weather(block.input as ToolInput);
    messages.push({ role: "user", content: [{
      type: "tool_result",
      tool_use_id: block.id,
      content: JSON.stringify(result),
    }] });
  }
}

const final = await client.messages.create({ model: MODEL, max_tokens: 500, messages });
console.log(final.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
    ''',
    12: '''
    import Anthropic from "@anthropic-ai/sdk";
    import type { MessageParam, ToolResultBlockParam, ToolUnion } from "@anthropic-ai/sdk/resources/messages";

    export {};

    const MAX_STEPS = 4;

    function readNumber(tokens: string[], cursor: { index: number }): number {
      const token = tokens[cursor.index];
      if (token === undefined || !/^\\d+(\\.\\d+)?$/.test(token)) throw new Error("Número esperado.");
      cursor.index += 1;
      return Number(token);
    }

    function evaluateExpression(expression: string): number {
      const tokens = expression.match(/\\d+(?:\\.\\d+)?|[()+\\-*/]/g) ?? [];
      const cursor = { index: 0 };

      function factor(): number {
        if (tokens[cursor.index] === "(") {
          cursor.index += 1;
          const value = expr();
          if (tokens[cursor.index] !== ")") throw new Error("Paréntesis sin cerrar.");
          cursor.index += 1;
          return value;
        }
        if (tokens[cursor.index] === "-") {
          cursor.index += 1;
          return -factor();
        }
        return readNumber(tokens, cursor);
      }

      function term(): number {
        let value = factor();
        while (tokens[cursor.index] === "*" || tokens[cursor.index] === "/") {
          const operator = tokens[cursor.index];
          cursor.index += 1;
          const right = factor();
          value = operator === "*" ? value * right : value / right;
        }
        return value;
      }

      function expr(): number {
        let value = term();
        while (tokens[cursor.index] === "+" || tokens[cursor.index] === "-") {
          const operator = tokens[cursor.index];
          cursor.index += 1;
          const right = term();
          value = operator === "+" ? value + right : value - right;
        }
        return value;
      }

      const result = expr();
      if (cursor.index !== tokens.length) throw new Error("Tokens extra no permitidos.");
      return result;
    }

    function calculator(expression: string): string {
      try {
        return String(evaluateExpression(expression));
      } catch (error) {
        return `Expresión rechazada: ${error instanceof Error ? error.message : "input inválido"}`;
      }
    }

    const tool: ToolUnion = {
      name: "calculator",
      description: "Calculadora aritmética.",
      input_schema: { type: "object", properties: { expression: { type: "string" } }, required: ["expression"] },
    };

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const client = new Anthropic({ apiKey });
    const messages: MessageParam[] = [{ role: "user", content: "Calcula (128 * 7) + 34 y explica el resultado." }];

    for (let step = 0; step < MAX_STEPS; step += 1) {
      const response = await client.messages.create({ model: "claude-sonnet-4-6", max_tokens: 500, tools: [tool], messages });
      messages.push({ role: "assistant", content: response.content });
      const toolResults: ToolResultBlockParam[] = [];

      for (const block of response.content) {
        if (block.type === "tool_use") {
          const input = block.input as Record<string, unknown>;
          const expression = typeof input.expression === "string" ? input.expression : "";
          toolResults.push({ type: "tool_result", tool_use_id: block.id, content: calculator(expression) });
        }
      }

      if (toolResults.length === 0) {
        console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
        break;
      }
      messages.push({ role: "user", content: toolResults });
    }
    ''',
    13: '''
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
    ''',
    14: '''
import Anthropic from "@anthropic-ai/sdk";
import type { MessageParam, ToolUnion } from "@anthropic-ai/sdk/resources/messages";

export {};

const MODEL = "claude-sonnet-4-6";
const MAX_STEPS = 4;
const LOCAL_PAGES = new Map([
  ["https://docs.anthropic.com/en/api/messages", "La Messages API permite enviar messages, system prompts y herramientas."],
  ["https://docs.anthropic.com/en/docs/tool-use", "Tool use permite que Claude solicite funciones externas y reciba tool_result."],
]);

const tools: ToolUnion[] = [
  {
    name: "search_web",
    description: "Busca páginas relevantes para una pregunta.",
    input_schema: { type: "object", properties: { query: { type: "string" } }, required: ["query"] },
  },
  {
    name: "read_url",
    description: "Lee el contenido textual de una URL.",
    input_schema: { type: "object", properties: { url: { type: "string" } }, required: ["url"] },
  },
];

function searchWeb(): string {
  return [...LOCAL_PAGES.keys()].map((url) => `- ${url}`).join("\\n");
}

function readUrl(url: string): string {
  return LOCAL_PAGES.get(url) ?? "Fuente no disponible en el set local de la demo.";
}

function runTool(name: string, input: Record<string, unknown>): string {
  if (name === "search_web") return searchWeb();
  if (name === "read_url") return readUrl(typeof input.url === "string" ? input.url : "");
  return "Herramienta no permitida.";
}

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const messages: MessageParam[] = [{ role: "user", content: "Investiga cómo funciona tool use en Claude API y cita fuentes." }];

for (let step = 0; step < MAX_STEPS; step += 1) {
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 900,
    system: "Responde con resumen corto, hallazgos principales, fuentes consultadas y limitaciones.",
    tools,
    messages,
  });
  const toolResults = response.content
    .filter((block) => block.type === "tool_use")
    .map((block) => ({
      type: "tool_result" as const,
      tool_use_id: block.id,
      content: runTool(block.name, block.input as Record<string, unknown>),
    }));

  if (toolResults.length === 0) {
    console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
    break;
  }

  messages.push({ role: "assistant", content: response.content });
  messages.push({ role: "user", content: toolResults });
}
    ''',
    15: '''
    import Anthropic from "@anthropic-ai/sdk";

    export {};

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const longPolicy = "Reglas internas del asistente. ".repeat(400);
    const client = new Anthropic({ apiKey });
    const response = await client.messages.create({
      model: "claude-sonnet-4-6",
      max_tokens: 300,
      system: [{ type: "text", text: longPolicy, cache_control: { type: "ephemeral" } }],
      messages: [{ role: "user", content: "Resume las 3 reglas principales." }],
    });

    console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
    console.log(response.usage);
    ''',
    16: '''
import Anthropic from "@anthropic-ai/sdk";

export {};

const MODEL = "claude-sonnet-4-6";
const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const client = new Anthropic({ apiKey });
const batch = await client.messages.batches.create({
  requests: [{
    custom_id: "invoice-001",
    params: {
      model: MODEL,
      max_tokens: 500,
      messages: [{ role: "user", content: "Resume esta factura de ejemplo." }],
    },
  }],
});

console.log(batch.id, batch.processing_status);
const batchStatus = await client.messages.batches.retrieve(batch.id);
console.log(batchStatus.processing_status);

if (batchStatus.processing_status === "ended") {
  const results = await client.messages.batches.results(batch.id);
  for await (const result of results) {
    console.log(result.custom_id, result.result.type);
  }
} else {
  console.log("El batch todavía no termina. Vuelve a consultar más tarde antes de leer results.");
}
    ''',
    17: '''
import Anthropic from "@anthropic-ai/sdk";
import type { Message } from "@anthropic-ai/sdk/resources/messages";

export {};

const MODEL = "claude-sonnet-4-6";

async function retryWithBackoff<T>(fn: () => Promise<T>, maxRetries = 5): Promise<T> {
  for (let attempt = 0; attempt < maxRetries; attempt += 1) {
    try {
      return await fn();
    } catch (error) {
      const waitMs = (2 ** attempt + Math.random()) * 1000;
      console.log(`Error: ${error}. Reintentando en ${(waitMs / 1000).toFixed(2)}s`);
      await new Promise((resolve) => setTimeout(resolve, waitMs));
    }
  }
  throw new Error("Se agotaron los reintentos");
}

async function safeClaudeCall(client: Anthropic): Promise<Message> {
  const start = performance.now();
  const response = await retryWithBackoff(() => client.messages.create({
    model: MODEL,
    max_tokens: 200,
    messages: [{ role: "user", content: "Dame un tip de observabilidad." }],
  }));
  console.log(JSON.stringify({
    model: response.model,
    input_tokens: response.usage.input_tokens,
    output_tokens: response.usage.output_tokens,
    elapsed_ms: Math.round(performance.now() - start),
    status: "success",
  }));
  return response;
}

const apiKey = process.env.ANTHROPIC_API_KEY;
if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

const response = await safeClaudeCall(new Anthropic({ apiKey }));
console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
    ''',
    18: '''
import Anthropic from "@anthropic-ai/sdk";
import Fastify from "fastify";
import { z } from "zod";

export {};

const MODEL = "claude-sonnet-4-6";
const APP_API_KEY = process.env.APP_API_KEY;
const ChatRequest = z.object({ message: z.string().min(1) });
const server = Fastify({ logger: true });

server.get("/health", async () => ({ status: "ok" }));

server.post("/chat", async (request, reply) => {
  if (!APP_API_KEY) return reply.code(500).send({ error: "APP_API_KEY no configurada." });
  if (request.headers["x-api-key"] !== APP_API_KEY) {
    return reply.code(401).send({ error: "Unauthorized" });
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) return reply.code(500).send({ error: "ANTHROPIC_API_KEY no configurada." });

  const payload = ChatRequest.parse(request.body);
  const client = new Anthropic({ apiKey });
  const response = await client.messages.create({
    model: MODEL,
    max_tokens: 600,
    messages: [{ role: "user", content: payload.message }],
  });
  const replyText = response.content.filter((block) => block.type === "text").map((block) => block.text).join("");
  return { reply: replyText };
});

await server.listen({ port: Number(process.env.PORT ?? 3000), host: "0.0.0.0" });
    ''',
}










TS_EXTRA_FILES = {
    'typescript/clase-09/final/schemas.ts': '''
import { z } from "zod";

export const InvoiceData = z.object({
  provider: z.string().nullable(),
  date: z.string().nullable(),
  currency: z.string().nullable(),
  total: z.number().nullable(),
  items: z.array(z.object({
    description: z.string(),
    quantity: z.number().nullable().optional(),
    unit_price: z.number().nullable().optional(),
    total: z.number(),
  })),
});
    ''',
    'typescript/clase-09/final/samples/README.md': '''
# Samples

Coloca aquí `factura_001.pdf` o cualquier factura PDF de prueba antes de ejecutar:

```bash
npm run clase:09:final -- ./clase-09/final/samples/factura_001.pdf
```
    ''',
    'typescript/clase-18/README.md': '''
# Clase 18: Deploy tu app con Fastify + Railway

**Objetivo:** mostrar la alternativa TypeScript de la API REST final con autenticación básica y variables seguras.

## Estructura

- `inicio/`: punto de partida para resolver durante la clase.
- `final/`: solución con `/health`, `/chat`, header `x-api-key` y `APP_API_KEY`.

## Ejecución local

```bash
export ANTHROPIC_API_KEY="tu_api_key"
export APP_API_KEY="clave_para_tu_app"
npm run clase:18:final
```

## Railway

Configura `ANTHROPIC_API_KEY`, `APP_API_KEY` y `PORT` como variables de entorno.
El comando de inicio puede usar el script de esta clase o un entrypoint dedicado para producción.
    ''',
}


def class_readme(language: str, number: int, title: str, objective: str) -> str:
    run = (
        f"python python/clase-{number:02d}/final/main.py"
        if language == "python"
        else f"npm --prefix typescript run clase:{number:02d}:final"
    )
    return f'''
    # Clase {number:02d}: {title}

    **Objetivo:** {objective}

    ## Estructura

    - `inicio/`: punto de partida para resolver durante la clase.
    - `final/`: solución comentada y lista para comparar.

    ## Ejecución sugerida

    ```bash
    cp .env.example .env
    export ANTHROPIC_API_KEY="tu_api_key"
    {run}
    ```

    ## Nota docente

    Recorre primero `inicio/main.{"py" if language == "python" else "ts"}` y deja que el estudiante complete los TODOs.
    Después compara contra `final/main.{"py" if language == "python" else "ts"}` para discutir decisiones de diseño,
    manejo de errores y seguridad.
    '''


def build_root_files() -> None:
    write("README.md", '''
    # Curso de Claude API

    Repositorio para el curso **Construyendo aplicaciones con Claude API**.

    - 18 clases.
    - 4 proyectos.
    - Ruta principal en Python.
    - Ruta alternativa en TypeScript con ejemplos equivalentes.
    - Cada clase incluye carpeta `inicio` y `final` para enseñar con checkpoints claros.

    ## Estructura

    ```text
    python/
      clase-01/
        inicio/
        final/
      ...
    typescript/
      clase-01/
        inicio/
        final/
      ...
    ```

    Además, el repositorio publica ramas remotas por clase:

    - `clase-XX-inicio`
    - `clase-XX-final`

    ## Configuración común

    ```bash
    cp .env.example .env
    export ANTHROPIC_API_KEY="tu_api_key"
    ```

    Nunca subas tu API key al repositorio. Usa variables de entorno en local, GitHub Actions, Railway o tu plataforma de deploy.

    Modelo usado en los ejemplos del guión:

    ```text
    claude-sonnet-4-6
    ```

    Revisa la documentación de Anthropic antes de grabar, porque los nombres de modelos pueden cambiar con el tiempo.

    ## Python

    La carpeta `python/` es la ruta principal del curso. Úsala si quieres seguir las clases exactamente como están planteadas en el temario.

    ### Requerimientos

    - Python 3.11 o superior.
    - `pip` y `venv`.
    - Una API key de Anthropic configurada como `ANTHROPIC_API_KEY`.
    - Conocimiento intermedio de Python: funciones, clases, errores, archivos y consumo de APIs.

    ### Instalar dependencias

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"
    ```

    ### Ejecutar una clase

    Cada clase tiene un punto de partida y una solución:

    ```bash
    # Punto de partida para resolver en vivo
    python python/clase-01/inicio/main.py

    # Solución final de la clase
    python python/clase-01/final/main.py
    ```

    Validación rápida:

    ```bash
    python -m compileall python
    ```

    ## TypeScript

    La carpeta `typescript/` es la ruta alternativa para comparar cómo se implementan los mismos conceptos con Node.js y TypeScript.

    ### Requerimientos

    - Node.js 20 o superior.
    - npm 10 o superior.
    - Una API key de Anthropic configurada como `ANTHROPIC_API_KEY`.
    - Conocimiento básico/intermedio de TypeScript: módulos ES, async/await, tipos y manejo de errores.

    ### Instalar dependencias

    ```bash
    cd typescript
    npm install
    ```

    ### Ejecutar una clase

    Los scripts siguen el patrón `clase:XX:inicio` y `clase:XX:final`:

    ```bash
    # Punto de partida para resolver en vivo
    npm run clase:01:inicio

    # Solución final de la clase
    npm run clase:01:final
    ```

    Validación rápida:

    ```bash
    npm run typecheck
    ```

    ## Cómo elegir entre Python y TypeScript

    - Usa **Python** para seguir el curso principal, los proyectos base y la versión que se despliega con FastAPI.
    - Usa **TypeScript** cuando quieras mostrar la alternativa equivalente para estudiantes que trabajan con Node.js.
    - Ambas rutas usan la misma API key y cubren los mismos conceptos por clase.
    - Puedes comparar `python/clase-XX/final/main.py` contra `typescript/clase-XX/final/main.ts` para explicar diferencias de SDK, tipos y estilo.

    ## Mapa del curso

    | Clase | Tema |
    | --- | --- |
    | 01 | Quickstart: tu primera llamada a Claude API |
    | 02 | Conversaciones multi-turn: el array de messages |
    | 03 | Estrategias de gestión de contexto y tokens |
    | 04 | Streaming de respuestas en tiempo real |
    | 05 | Proyecto: chatbot con interfaz de terminal |
    | 06 | Inputs multimedia: imágenes y documentos PDF |
    | 07 | Outputs estructurados con JSON mode |
    | 08 | Prompt engineering para extracción de datos |
    | 09 | Proyecto: extractor de facturas en PDF |
    | 10 | Tool use: cómo Claude llama funciones externas |
    | 11 | Definir herramientas y manejar tool_result |
    | 12 | Loop agentico: razonar → actuar → observar |
    | 13 | Manejo de errores y seguridad en agentes |
    | 14 | Proyecto: agente de búsqueda y resumen web |
    | 15 | Prompt caching: reduce costos |
    | 16 | Batch API para miles de requests |
    | 17 | Rate limits, reintentos y observabilidad |
    | 18 | Proyecto final: FastAPI + Railway |
    ''')
    write(".env.example", '''
    # Copia este archivo a .env o exporta la variable en tu terminal.
    # No subas API keys reales al repositorio.
    ANTHROPIC_API_KEY=tu_api_key_de_anthropic

    # Clase 18 / Railway puede usar PORT automáticamente.
    PORT=8000
    ''')
    write(".gitignore", '''
    .env
    .venv/
    __pycache__/
    *.pyc
    node_modules/
    dist/
    chat_history.json
    history.json
    output.json
    *.egg-info/
    *.log
    .DS_Store
    ''')
    write("pyproject.toml", '''
    [project]
    name = "curso-de-claude-api"
    version = "0.1.0"
    description = "Ejemplos en Python para el curso de Claude API"
    requires-python = ">=3.11"
    dependencies = [
      "anthropic>=0.54.0",
      "fastapi>=0.115.0",
      "pydantic>=2.7.0",
      "python-dotenv>=1.0.1",
      "uvicorn[standard]>=0.30.0",
    ]

    [project.optional-dependencies]
    dev = [
      "ruff>=0.11.0",
      "mypy>=1.10.0",
    ]

    [tool.ruff]
    line-length = 110
    target-version = "py311"
    ''')
    write("python/README.md", '''
    # Ruta Python

    Python es la ruta principal del curso. Cada clase tiene:

    - `inicio/main.py`: ejercicio guiado con TODOs.
    - `final/main.py`: implementación completa y comentada.

    ## Validación

    ```bash
    python -m compileall python
    ```

    ## Ejecutar una clase

    ```bash
    export ANTHROPIC_API_KEY="tu_api_key"
    python python/clase-01/final/main.py
    ```
    ''')

    scripts = {
        f"clase:{number:02d}:inicio": f"tsx clase-{number:02d}/inicio/main.ts"
        for number, _, _ in CLASSES
    }
    scripts.update({
        f"clase:{number:02d}:final": f"tsx clase-{number:02d}/final/main.ts"
        for number, _, _ in CLASSES
    })
    script_lines = ",\n".join(f'    "{key}": "{value}"' for key, value in sorted(scripts.items()))
    write("typescript/package.json", f'''
    {{
      "name": "curso-de-claude-api-typescript",
      "version": "0.1.0",
      "private": true,
      "type": "module",
      "scripts": {{
        "typecheck": "tsc --noEmit",
    {script_lines}
      }},
      "dependencies": {{
        "@anthropic-ai/sdk": "^0.54.0",
        "dotenv": "^16.4.7",
        "fastify": "^5.3.3",
        "zod": "^3.25.0"
      }},
      "devDependencies": {{
        "@types/node": "^22.10.0",
        "tsx": "^4.19.0",
        "typescript": "^5.8.0"
      }}
    }}
    ''')
    write("typescript/tsconfig.json", '''
    {
      "compilerOptions": {
        "target": "ES2022",
        "module": "NodeNext",
        "moduleResolution": "NodeNext",
        "strict": true,
        "skipLibCheck": true,
        "noEmit": true,
        "types": ["node"]
      },
      "include": ["clase-*/**/*.ts"]
    }
    ''')
    write("typescript/README.md", '''
    # Ruta TypeScript

    Esta carpeta replica los conceptos de la ruta Python para estudiantes que prefieren Node.js.

    ## Instalar

    ```bash
    npm install
    ```

    ## Ejecutar una clase

    ```bash
    export ANTHROPIC_API_KEY="tu_api_key"
    npm run clase:01:final
    ```

    ## Validar tipos

    ```bash
    npm run typecheck
    ```
    ''')


def build_classes() -> None:
    for number, title, objective in CLASSES:
        slug = f"clase-{number:02d}"
        write(f"python/{slug}/README.md", class_readme("python", number, title, objective))
        write(f"python/{slug}/inicio/main.py", py_starter(number, title))
        write(f"python/{slug}/final/main.py", PY_FINALS[number])

        for relative_path, content in PY_EXTRA_FILES.items():
            if relative_path.startswith(f"python/{slug}/"):
                write(relative_path, content)

        write(f"typescript/{slug}/README.md", class_readme("typescript", number, title, objective))
        write(f"typescript/{slug}/inicio/main.ts", ts_starter(number, title))
        write(f"typescript/{slug}/final/main.ts", TS_FINALS[number])

        for relative_path, content in TS_EXTRA_FILES.items():
            if relative_path.startswith(f"typescript/{slug}/"):
                write(relative_path, content)


def main() -> None:
    build_root_files()
    build_classes()
    print(f"Generated course files in {ROOT}")


if __name__ == "__main__":
    main()
