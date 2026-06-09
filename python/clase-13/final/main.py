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
