"""Clase 15 - inicio: Frontend + hub de proyectos con FastAPI.

Punto de partida que combina dos cosas:
1. Lo último de la clase 14 (Batch API) como referencia para continuidad.
2. El esqueleto del hub web que completaremos en vivo durante la clase.

Ejecuta el frontend con:
    uvicorn --app-dir python/clase-15/inicio main:app --reload
"""

import os

from anthropic import Anthropic
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

MODEL = "claude-sonnet-4-6"


# =========================================================================
# Parte 1 - Lo último de la clase 14: Batch API (referencia de continuidad)
# =========================================================================
def demo_batch() -> None:
    """Crear un batch, consultar estado y leer resultados (solución clase 14)."""
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


# =========================================================================
# Parte 2 - Nuevo: esqueleto del hub frontend (a completar durante la clase)
# =========================================================================
app = FastAPI(title="Claude API Hub")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)


INDEX_HTML = """
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Claude API Hub</title>
  </head>
  <body>
    <main>
      <h1>Claude API Hub</h1>
      <p>TODO: diseña un frontend para llamar /api/chat, /api/extract y /api/agent.</p>
    </main>
  </body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index() -> HTMLResponse:
    return HTMLResponse(INDEX_HTML)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/chat")
def chat(payload: ChatRequest) -> dict[str, str]:
    # TODO 1: lee ANTHROPIC_API_KEY y crea el cliente de Anthropic.
    # TODO 2: envía payload.message a Claude.
    # TODO 3: devuelve {"reply": "..."} para que el frontend lo pinte.
    return {"reply": f"TODO: conectar Claude para: {payload.message}"}


# TODO 4: agrega /api/extract para el proyecto de JSON estructurado (clase 07).
# TODO 5: agrega /api/agent para el proyecto de tool use + calculadora (clase 11).
# TODO 6: conecta los formularios del frontend con fetch().
