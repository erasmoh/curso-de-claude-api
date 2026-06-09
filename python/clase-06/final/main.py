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
