"""Clase 17 - inicio: Frontend y hub de proyectos con FastAPI.

Punto de partida para convertir los proyectos del curso en una sola app web.
Ejecuta con: uvicorn --app-dir python/clase-17/inicio main:app --reload
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

MODEL = "claude-sonnet-4-6"
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


# TODO 4: agrega /api/extract para el proyecto de JSON estructurado.
# TODO 5: agrega /api/agent para el proyecto de tool use + calculadora.
# TODO 6: conecta los formularios del frontend con fetch().
