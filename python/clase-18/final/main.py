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
