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
