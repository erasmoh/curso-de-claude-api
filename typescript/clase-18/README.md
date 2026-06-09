# Clase 18: Deploy tu app con Fastify + Railway

**Objetivo:** mostrar la alternativa TypeScript de la API REST final con autenticación básica y variables seguras.

## Estructura

- `inicio/`: punto de partida para resolver durante la clase.
- `final/`: solución con `/health`, `/chat`, header `x-api-key` y `APP_API_KEY`.

## Ejecución local

```bash
export ANTHROPIC_API_KEY="tu_api_key"
export APP_API_KEY="clave_para_tu_app"
npm run clase:18:final
```

## Railway

Configura `ANTHROPIC_API_KEY`, `APP_API_KEY` y `PORT` como variables de entorno.
El comando de inicio puede usar el script de esta clase o un entrypoint dedicado para producción.
