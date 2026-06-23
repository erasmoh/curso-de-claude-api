# Curso de Claude API — Clase 12: Manejo de errores y seguridad en agentes

Esta rama es el checkpoint **inicio** de la clase 12.

Punto de partida con TODOs para resolver en vivo durante la clase.

## Contenido de esta rama

- `python/clase-12/inicio/main.py` — versión Python (ruta principal).
- `typescript/clase-12/inicio/main.ts` — versión TypeScript (ruta alternativa).

## Cómo ejecutar

```bash
cp .env.example .env
export ANTHROPIC_API_KEY="tu_api_key"

# Python
python python/clase-12/inicio/main.py

# TypeScript
cd typescript && npm install && npm run clase:12:inicio
```

## Navegación del curso

- `clase-XX-inicio`: punto de partida de cada clase.
- `clase-XX-final`: solución de cada clase.
- `main`: curso completo (todas las clases) y el generador.

> Objetivo de la clase: Limitar pasos, validar inputs y evitar loops peligrosos.
