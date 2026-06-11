# Clase 09: Tool use: cómo Claude llama funciones externas

**Objetivo:** Declarar herramientas y detectar bloques tool_use.

## Estructura

- `inicio/`: punto de partida para resolver durante la clase.
- `final/`: solución comentada y lista para comparar.

## Ejecución sugerida

```bash
cp .env.example .env
export ANTHROPIC_API_KEY="tu_api_key"
npm --prefix typescript run clase:09:final
```

## Nota docente

Recorre primero `inicio/main.ts` y deja que el estudiante complete los TODOs.
Después compara contra `final/main.ts` para discutir decisiones de diseño,
manejo de errores y seguridad.
