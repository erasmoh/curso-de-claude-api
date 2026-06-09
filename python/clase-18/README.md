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
