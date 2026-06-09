# Clase 17: Rate limits, reintentos y observabilidad

**Objetivo:** Aplicar backoff, logs estructurados y métricas de tokens.

## Estructura

- `inicio/`: punto de partida para resolver durante la clase.
- `final/`: solución comentada y lista para comparar.

## Ejecución sugerida

```bash
cp .env.example .env
export ANTHROPIC_API_KEY="tu_api_key"
python python/clase-17/final/main.py
```

## Nota docente

Recorre primero `inicio/main.py` y deja que el estudiante complete los TODOs.
Después compara contra `final/main.py` para discutir decisiones de diseño,
manejo de errores y seguridad.
