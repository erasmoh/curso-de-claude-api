# Curso de Claude API — Clase 16: Frontend + hub de proyectos con FastAPI

Esta rama es el checkpoint **final** de la clase 16.

Solución completa y comentada de la clase.

## Contenido de esta rama

- `python/clase-16/final/main.py` — versión Python (ruta principal).
- `typescript/clase-16/final/main.ts` — versión TypeScript (ruta alternativa).

## Cómo ejecutar

Configura tu API key (sirve para ambas rutas):

```bash
cp .env.example .env
export ANTHROPIC_API_KEY="tu_api_key"
```

Python (desde la carpeta de la clase; es una app FastAPI, se sirve con `uvicorn`):

```bash
cd python/clase-16
uvicorn --app-dir final main:app --reload
```

TypeScript (desde la raíz del repositorio):

```bash
cd typescript && npm install && npm run clase:16:final
```

## Navegación del curso

- `clase-XX-inicio`: punto de partida de cada clase.
- `clase-XX-final`: solución de cada clase.
- `main`: curso completo (todas las clases) y el generador.

> Objetivo de la clase: Servir un frontend y reunir chatbot, extracción JSON y agente en una sola app.
