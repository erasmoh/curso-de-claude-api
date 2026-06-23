# Clase 15: Frontend + hub de proyectos con Fastify

**Objetivo:** mostrar la alternativa TypeScript del hub web: un frontend servido por Fastify y endpoints para chatbot, extracción JSON y agente con herramientas.

## Estructura

- `inicio/`: punto de partida que conserva la solución de la clase 14 (Batch API) como referencia y suma un servidor Fastify mínimo con TODOs.
- `final/`: solución con frontend HTML/CSS/JS embebido y endpoints `/api/chat`, `/api/extract` y `/api/agent`.

## Ejecución local

```bash
export ANTHROPIC_API_KEY="tu_api_key"
npm run clase:15:final
```

Abre `http://127.0.0.1:3000` para probar la versión TypeScript desde el navegador.
