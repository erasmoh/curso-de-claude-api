# Clase 16: Frontend + hub de proyectos con FastAPI

**Objetivo:** convertir los proyectos clave del curso en una sola aplicación web: un frontend servido por FastAPI y tres endpoints para chatbot, extracción JSON y agente con herramientas.

## Estructura

- `inicio/`: punto de partida que conserva la solución de la clase 14 (Batch API) como referencia y suma una app FastAPI mínima con `/health`, `/` y TODOs para completar los endpoints.
- `final/`: solución con frontend HTML/CSS/JS embebido y endpoints `/api/chat`, `/api/extract` y `/api/agent`.

## Ejecución local

```bash
# Desde la carpeta de la clase
cd python/clase-16
export ANTHROPIC_API_KEY="tu_api_key"
uvicorn --app-dir final main:app --reload
```

Abre `http://127.0.0.1:8000` para probar los tres proyectos desde el navegador.

## Guion sugerido

1. Mostrar el frontend estático servido por FastAPI.
2. Conectar el formulario del chatbot con `fetch('/api/chat')`.
3. Reutilizar el extractor de facturas de la clase 07 en `/api/extract`.
4. Reutilizar el agente con calculadora de la clase 11 en `/api/agent`.
5. Explicar por qué el frontend nunca debe llamar a Claude API directamente con la API key.
