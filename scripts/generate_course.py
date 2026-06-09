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


    MODEL = "claude-3-5-sonnet-latest"


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

    const MODEL = "claude-3-5-sonnet-latest";

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

    MODEL = "claude-3-5-sonnet-latest"


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

    MODEL = "claude-3-5-sonnet-latest"


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
    """Gestión básica de contexto para conversaciones largas."""

    from __future__ import annotations

    import os
    from anthropic import Anthropic

    MODEL = "claude-3-5-sonnet-latest"
    MAX_HISTORY_MESSAGES = 6


    def trim_history(messages: list[dict[str, str]], max_messages: int = MAX_HISTORY_MESSAGES) -> list[dict[str, str]]:
        """Conserva los mensajes más recientes para controlar costo y contexto."""
        if len(messages) <= max_messages:
            return messages
        return messages[-max_messages:]


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        history = [{"role": "user", "content": f"Mensaje antiguo #{index}"} for index in range(10)]
        history.append({"role": "user", "content": "Resume qué decisiones importantes recuerdas."})

        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=250,
            system="Si falta contexto, dilo explícitamente y pide más información.",
            messages=trim_history(history),
        )

        for block in response.content:
            if block.type == "text":
                print(block.text)


    if __name__ == "__main__":
        main()
    ''',
    4: '''
    """Streaming: imprime la respuesta conforme llega desde Claude."""

    import os
    from anthropic import Anthropic

    MODEL = "claude-3-5-sonnet-latest"


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
    """Chatbot de terminal con historial persistente y streaming."""

    from __future__ import annotations

    import json
    import os
    from pathlib import Path
    from anthropic import Anthropic

    MODEL = "claude-3-5-sonnet-latest"
    HISTORY_PATH = Path("chat_history.json")


    def load_history() -> list[dict[str, str]]:
        if not HISTORY_PATH.exists():
            return []
        return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))


    def save_history(messages: list[dict[str, str]]) -> None:
        HISTORY_PATH.write_text(json.dumps(messages, indent=2, ensure_ascii=False), encoding="utf-8")


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        client = Anthropic(api_key=api_key)
        messages = load_history()
        print("Chatbot listo. Escribe 'salir' para terminar.")

        while True:
            user_text = input("\\nTú: ").strip()
            if user_text.lower() == "salir":
                break

            messages.append({"role": "user", "content": user_text})
            assistant_text = ""
            print("Claude: ", end="", flush=True)
            with client.messages.stream(model=MODEL, max_tokens=600, messages=messages[-12:]) as stream:
                for text in stream.text_stream:
                    assistant_text += text
                    print(text, end="", flush=True)
            print()

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

    MODEL = "claude-3-5-sonnet-latest"


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
    """JSON estructurado con prompt estricto y validación Pydantic."""

    from __future__ import annotations

    import json
    import os
    from anthropic import Anthropic
    from pydantic import BaseModel, Field

    MODEL = "claude-3-5-sonnet-latest"


    class TaskSummary(BaseModel):
        title: str = Field(description="Título corto de la tarea.")
        priority: str = Field(description="low, medium o high.")
        next_step: str = Field(description="Siguiente acción concreta.")


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=300,
            system="Responde únicamente JSON válido, sin Markdown ni texto extra.",
            messages=[{"role": "user", "content": "Convierte esta idea en tarea: lanzar chatbot con memoria."}],
        )

        raw_text = "".join(block.text for block in response.content if block.type == "text")
        parsed = TaskSummary.model_validate(json.loads(raw_text))
        print(parsed.model_dump_json(indent=2))


    if __name__ == "__main__":
        main()
    ''',
    8: '''
    """Prompt engineering para extraer datos de documentos ambiguos."""

    import os
    from anthropic import Anthropic

    MODEL = "claude-3-5-sonnet-latest"

    EXTRACTION_PROMPT = """
    Extrae datos del texto usando estas reglas:
    - Si un campo no aparece, usa null.
    - No inventes fechas, totales ni nombres.
    - Devuelve JSON válido con provider, date, total y currency.
    - Si el documento es ambiguo, agrega una lista warnings.
    """


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        document_text = "Factura ACME emitida el 2026-05-01. Total: USD 129.90"
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=350,
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
    """Extractor de factura PDF con salida JSON validada."""

    from __future__ import annotations

    import base64
    import json
    import os
    from pathlib import Path
    from anthropic import Anthropic
    from pydantic import BaseModel

    MODEL = "claude-3-5-sonnet-latest"


    class InvoiceItem(BaseModel):
        description: str
        quantity: float
        unit_price: float


    class Invoice(BaseModel):
        provider: str | None
        date: str | None
        total: float | None
        currency: str | None
        items: list[InvoiceItem]


    def extract_invoice(pdf_path: Path) -> Invoice:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        pdf_data = base64.b64encode(pdf_path.read_bytes()).decode("utf-8")
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=900,
            system="Extrae factura como JSON válido. No agregues Markdown.",
            messages=[{"role": "user", "content": [
                {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": pdf_data}},
                {"type": "text", "text": "Campos: provider, date, total, currency, items[]."},
            ]}],
        )
        raw_text = "".join(block.text for block in response.content if block.type == "text")
        return Invoice.model_validate(json.loads(raw_text))


    if __name__ == "__main__":
        invoice = extract_invoice(Path("invoice.pdf"))
        print(invoice.model_dump_json(indent=2))
    ''',
    10: '''
    """Tool use: Claude solicita una función externa mediante tool_use."""

    import os
    from anthropic import Anthropic

    MODEL = "claude-3-5-sonnet-latest"

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
    """Ejecutar una herramienta local y responder con tool_result."""

    from __future__ import annotations

    import os
    from anthropic import Anthropic

    MODEL = "claude-3-5-sonnet-latest"


    def get_weather(city: str) -> str:
        """Herramienta fake para clase: reemplázala por una API real."""
        return f"Clima en {city}: 24°C, parcialmente nublado."


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        client = Anthropic(api_key=api_key)
        messages = [{"role": "user", "content": "Dime el clima de Bogotá y dame una recomendación."}]
        first = client.messages.create(
            model=MODEL,
            max_tokens=400,
            tools=[{"name": "get_weather", "description": "Clima por ciudad.", "input_schema": {
                "type": "object", "properties": {"city": {"type": "string"}}, "required": ["city"]}}],
            messages=messages,
        )

        messages.append({"role": "assistant", "content": first.content})
        for block in first.content:
            if block.type == "tool_use":
                result = get_weather(str(block.input["city"]))
                messages.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": block.id, "content": result}]})

        final = client.messages.create(model=MODEL, max_tokens=400, messages=messages)
        for block in final.content:
            if block.type == "text":
                print(block.text)


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

    MODEL = "claude-3-5-sonnet-latest"
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
    """Seguridad mínima para agentes con herramientas."""

    from __future__ import annotations

    from urllib.parse import urlparse

    ALLOWED_DOMAINS = {"docs.anthropic.com", "www.anthropic.com"}


    def validate_url(url: str) -> str:
        """Acepta solo HTTPS y dominios permitidos para reducir SSRF y abuso."""
        parsed = urlparse(url)
        if parsed.scheme != "https":
            raise ValueError("Solo se permite HTTPS.")
        if parsed.netloc not in ALLOWED_DOMAINS:
            raise ValueError(f"Dominio no permitido: {parsed.netloc}")
        return url


    def main() -> None:
        safe_url = validate_url("https://docs.anthropic.com/en/api/messages")
        print(f"URL validada para la herramienta fetch: {safe_url}")
        print("En el agente real, combina esta validación con MAX_STEPS y timeouts.")


    if __name__ == "__main__":
        main()
    ''',
    14: '''
    """Agente de búsqueda y resumen web con herramientas simuladas."""

    from __future__ import annotations

    import os
    from anthropic import Anthropic

    MODEL = "claude-3-5-sonnet-latest"


    def search_web(query: str) -> str:
        """Stub didáctico: cambia esto por Tavily, Brave, SerpAPI u otro proveedor."""
        return "1. Anthropic Docs - https://docs.anthropic.com/en/api/messages\\n2. Claude Tool Use - https://docs.anthropic.com/en/docs/tool-use"


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        client = Anthropic(api_key=api_key)
        query = "Cómo funciona tool use en Claude API"
        search_results = search_web(query)
        response = client.messages.create(
            model=MODEL,
            max_tokens=700,
            system="Resume con bullets y cita fuentes por URL.",
            messages=[{"role": "user", "content": f"Pregunta: {query}\\nFuentes encontradas:\\n{search_results}"}],
        )
        print("".join(block.text for block in response.content if block.type == "text"))


    if __name__ == "__main__":
        main()
    ''',
    15: '''
    """Prompt caching: marca instrucciones largas y reutilizables."""

    import os
    from anthropic import Anthropic

    MODEL = "claude-3-5-sonnet-latest"


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
    """Batch API: preparar muchas solicitudes asincrónicas."""

    import os
    from anthropic import Anthropic

    MODEL = "claude-3-5-sonnet-latest"


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        client = Anthropic(api_key=api_key)
        batch = client.messages.batches.create(requests=[
            {
                "custom_id": "resumen-001",
                "params": {
                    "model": MODEL,
                    "max_tokens": 120,
                    "messages": [{"role": "user", "content": "Resume qué es Claude API."}],
                },
            }
        ])
        print(f"Batch creado: {batch.id} con estado {batch.processing_status}")


    if __name__ == "__main__":
        main()
    ''',
    17: '''
    """Reintentos con backoff y logs estructurados para producción."""

    from __future__ import annotations

    import json
    import os
    import time
    from anthropic import Anthropic, RateLimitError

    MODEL = "claude-3-5-sonnet-latest"


    def log_event(event: str, **fields: object) -> None:
        print(json.dumps({"event": event, **fields}, ensure_ascii=False))


    def main() -> None:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("Define ANTHROPIC_API_KEY.")

        client = Anthropic(api_key=api_key)
        for attempt in range(1, 4):
            try:
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=200,
                    messages=[{"role": "user", "content": "Dame un tip de observabilidad."}],
                )
                log_event("claude_response", attempt=attempt, usage=response.usage.model_dump())
                print("".join(block.text for block in response.content if block.type == "text"))
                return
            except RateLimitError:
                wait_seconds = 2 ** attempt
                log_event("rate_limited", attempt=attempt, wait_seconds=wait_seconds)
                time.sleep(wait_seconds)

        raise RuntimeError("No se pudo completar la request después de 3 intentos.")


    if __name__ == "__main__":
        main()
    ''',
    18: '''
    """API REST con FastAPI lista para desplegar en Railway."""

    import os
    from anthropic import Anthropic
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel

    MODEL = "claude-3-5-sonnet-latest"
    app = FastAPI(title="Curso Claude API")


    class ChatRequest(BaseModel):
        message: str


    class ChatResponse(BaseModel):
        answer: str


    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}


    @app.post("/chat", response_model=ChatResponse)
    def chat(payload: ChatRequest) -> ChatResponse:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY no configurada.")

        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=MODEL,
            max_tokens=500,
            messages=[{"role": "user", "content": payload.message}],
        )
        answer = "".join(block.text for block in response.content if block.type == "text")
        return ChatResponse(answer=answer)
    ''',
}


TS_FINALS = {
    1: '''
    import Anthropic from "@anthropic-ai/sdk";

    export {};

    const MODEL = "claude-3-5-sonnet-latest";

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

    const MODEL = "claude-3-5-sonnet-latest";

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

    const MODEL = "claude-3-5-sonnet-latest";
    const MAX_HISTORY_MESSAGES = 6;

    function trimHistory(messages: MessageParam[]): MessageParam[] {
      return messages.length <= MAX_HISTORY_MESSAGES ? messages : messages.slice(-MAX_HISTORY_MESSAGES);
    }

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const history: MessageParam[] = Array.from({ length: 10 }, (_, index) => ({
      role: "user",
      content: `Mensaje antiguo #${index}`,
    }));
    history.push({ role: "user", content: "Resume qué decisiones importantes recuerdas." });

    const client = new Anthropic({ apiKey });
    const response = await client.messages.create({
      model: MODEL,
      max_tokens: 250,
      system: "Si falta contexto, dilo explícitamente y pide más información.",
      messages: trimHistory(history),
    });

    for (const block of response.content) {
      if (block.type === "text") console.log(block.text);
    }
    ''',
    4: '''
    import Anthropic from "@anthropic-ai/sdk";

    export {};

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const client = new Anthropic({ apiKey });
    const stream = client.messages.stream({
      model: "claude-3-5-sonnet-latest",
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

    const MODEL = "claude-3-5-sonnet-latest";
    const HISTORY_PATH = "chat_history.json";

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

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const client = new Anthropic({ apiKey });
    const rl = createInterface({ input, output });
    const messages = await loadHistory();
    console.log("Chatbot listo. Escribe 'salir' para terminar.");

    while (true) {
      const userText = (await rl.question("\\nTú: ")).trim();
      if (userText.toLowerCase() === "salir") break;

      messages.push({ role: "user", content: userText });
      let assistantText = "";
      process.stdout.write("Claude: ");

      const stream = client.messages.stream({ model: MODEL, max_tokens: 600, messages: messages.slice(-12) });
      stream.on("text", (text) => {
        assistantText += text;
        process.stdout.write(text);
      });
      await stream.finalMessage();
      process.stdout.write("\\n");

      messages.push({ role: "assistant", content: assistantText });
      await saveHistory(messages);
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
    ''',
    7: '''
    import Anthropic from "@anthropic-ai/sdk";
    import { z } from "zod";

    export {};

    const TaskSummary = z.object({
      title: z.string(),
      priority: z.enum(["low", "medium", "high"]),
      next_step: z.string(),
    });

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const client = new Anthropic({ apiKey });
    const response = await client.messages.create({
      model: "claude-3-5-sonnet-latest",
      max_tokens: 300,
      system: "Responde únicamente JSON válido, sin Markdown ni texto extra.",
      messages: [{ role: "user", content: "Convierte esta idea en tarea: lanzar chatbot con memoria." }],
    });

    const rawText = response.content.filter((block) => block.type === "text").map((block) => block.text).join("");
    const parsed = TaskSummary.parse(JSON.parse(rawText));
    console.log(JSON.stringify(parsed, null, 2));
    ''',
    8: '''
    import Anthropic from "@anthropic-ai/sdk";

    export {};

    const EXTRACTION_PROMPT = `
    Extrae datos del texto usando estas reglas:
    - Si un campo no aparece, usa null.
    - No inventes fechas, totales ni nombres.
    - Devuelve JSON válido con provider, date, total y currency.
    - Si el documento es ambiguo, agrega una lista warnings.
    `;

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const client = new Anthropic({ apiKey });
    const response = await client.messages.create({
      model: "claude-3-5-sonnet-latest",
      max_tokens: 350,
      system: EXTRACTION_PROMPT,
      messages: [{ role: "user", content: "Factura ACME emitida el 2026-05-01. Total: USD 129.90" }],
    });

    for (const block of response.content) {
      if (block.type === "text") console.log(block.text);
    }
    ''',
    9: '''
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
      model: "claude-3-5-sonnet-latest",
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

    function getWeather(city: string): string {
      return `Clima en ${city}: 24°C, parcialmente nublado.`;
    }

    const tool: ToolUnion = {
      name: "get_weather",
      description: "Clima por ciudad.",
      input_schema: { type: "object", properties: { city: { type: "string" } }, required: ["city"] },
    };

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const client = new Anthropic({ apiKey });
    const messages: MessageParam[] = [{ role: "user", content: "Dime el clima de Bogotá y dame una recomendación." }];
    const first = await client.messages.create({ model: "claude-3-5-sonnet-latest", max_tokens: 400, tools: [tool], messages });

    messages.push({ role: "assistant", content: first.content });
    for (const block of first.content) {
      if (block.type === "tool_use") {
        const input = block.input as Record<string, unknown>;
        const city = typeof input.city === "string" ? input.city : "ciudad desconocida";
        messages.push({ role: "user", content: [{ type: "tool_result", tool_use_id: block.id, content: getWeather(city) }] });
      }
    }

    const final = await client.messages.create({ model: "claude-3-5-sonnet-latest", max_tokens: 400, messages });
    for (const block of final.content) {
      if (block.type === "text") console.log(block.text);
    }
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
      const response = await client.messages.create({ model: "claude-3-5-sonnet-latest", max_tokens: 500, tools: [tool], messages });
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
    ''',
    14: '''
    import Anthropic from "@anthropic-ai/sdk";

    export {};

    function searchWeb(query: string): string {
      return [
        `Consulta: ${query}`,
        "1. Anthropic Docs - https://docs.anthropic.com/en/api/messages",
        "2. Claude Tool Use - https://docs.anthropic.com/en/docs/tool-use",
      ].join("\\n");
    }

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const query = "Cómo funciona tool use en Claude API";
    const client = new Anthropic({ apiKey });
    const response = await client.messages.create({
      model: "claude-3-5-sonnet-latest",
      max_tokens: 700,
      system: "Resume con bullets y cita fuentes por URL.",
      messages: [{ role: "user", content: `Pregunta: ${query}\\nFuentes encontradas:\\n${searchWeb(query)}` }],
    });

    console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
    ''',
    15: '''
    import Anthropic from "@anthropic-ai/sdk";

    export {};

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const longPolicy = "Reglas internas del asistente. ".repeat(400);
    const client = new Anthropic({ apiKey });
    const response = await client.messages.create({
      model: "claude-3-5-sonnet-latest",
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

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const client = new Anthropic({ apiKey });
    const batch = await client.messages.batches.create({
      requests: [{
        custom_id: "resumen-001",
        params: {
          model: "claude-3-5-sonnet-latest",
          max_tokens: 120,
          messages: [{ role: "user", content: "Resume qué es Claude API." }],
        },
      }],
    });

    console.log(`Batch creado: ${batch.id} con estado ${batch.processing_status}`);
    ''',
    17: '''
    import Anthropic, { RateLimitError } from "@anthropic-ai/sdk";

    export {};

    function logEvent(event: string, fields: Record<string, unknown>): void {
      console.log(JSON.stringify({ event, ...fields }));
    }

    const apiKey = process.env.ANTHROPIC_API_KEY;
    if (!apiKey) throw new Error("Define ANTHROPIC_API_KEY.");

    const client = new Anthropic({ apiKey });
    for (let attempt = 1; attempt <= 3; attempt += 1) {
      try {
        const response = await client.messages.create({
          model: "claude-3-5-sonnet-latest",
          max_tokens: 200,
          messages: [{ role: "user", content: "Dame un tip de observabilidad." }],
        });
        logEvent("claude_response", { attempt, usage: response.usage });
        console.log(response.content.filter((block) => block.type === "text").map((block) => block.text).join(""));
        break;
      } catch (error) {
        if (!(error instanceof RateLimitError)) throw error;
        const waitMs = 1000 * 2 ** attempt;
        logEvent("rate_limited", { attempt, waitMs });
        await new Promise((resolve) => setTimeout(resolve, waitMs));
      }
    }
    ''',
    18: '''
    import Anthropic from "@anthropic-ai/sdk";
    import Fastify from "fastify";
    import { z } from "zod";

    export {};

    const ChatRequest = z.object({ message: z.string().min(1) });
    const server = Fastify({ logger: true });

    server.get("/health", async () => ({ status: "ok" }));

    server.post("/chat", async (request, reply) => {
      const apiKey = process.env.ANTHROPIC_API_KEY;
      if (!apiKey) return reply.code(500).send({ error: "ANTHROPIC_API_KEY no configurada." });

      const payload = ChatRequest.parse(request.body);
      const client = new Anthropic({ apiKey });
      const response = await client.messages.create({
        model: "claude-3-5-sonnet-latest",
        max_tokens: 500,
        messages: [{ role: "user", content: payload.message }],
      });
      const answer = response.content.filter((block) => block.type === "text").map((block) => block.text).join("");
      return { answer };
    });

    await server.listen({ port: Number(process.env.PORT ?? 3000), host: "0.0.0.0" });
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

    ## Configuración

    ```bash
    cp .env.example .env
    export ANTHROPIC_API_KEY="tu_api_key"
    ```

    Nunca subas tu API key al repositorio. Usa variables de entorno en local, GitHub Actions, Railway o tu plataforma de deploy.

    ## Python

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"
    python python/clase-01/final/main.py
    ```

    Validación rápida:

    ```bash
    python -m compileall python
    ```

    ## TypeScript

    ```bash
    cd typescript
    npm install
    npm run clase:01:final
    npm run typecheck
    ```

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
    write(".github/workflows/ci.yml", '''
    name: CI

    on:
      pull_request:
      push:
        branches: [main]

    jobs:
      validate:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: "3.12"
          - uses: actions/setup-node@v4
            with:
              node-version: "22"
          - name: Validate Python syntax
            run: python -m compileall python
          - name: Install TypeScript dependencies
            working-directory: typescript
            run: npm install
          - name: Typecheck TypeScript examples
            working-directory: typescript
            run: npm run typecheck
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

        write(f"typescript/{slug}/README.md", class_readme("typescript", number, title, objective))
        write(f"typescript/{slug}/inicio/main.ts", ts_starter(number, title))
        write(f"typescript/{slug}/final/main.ts", TS_FINALS[number])


def main() -> None:
    build_root_files()
    build_classes()
    print(f"Generated course files in {ROOT}")


if __name__ == "__main__":
    main()
