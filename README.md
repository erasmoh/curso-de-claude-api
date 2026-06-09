# Curso de Claude API

Repositorio para el curso **Construyendo aplicaciones con Claude API**.

- 18 clases.
- 4 proyectos.
- Ruta principal en Python.
- Ruta alternativa en TypeScript con ejemplos equivalentes.
- Cada clase incluye carpeta `inicio` y `final` para enseñar con checkpoints claros.

## Estructura

```text
python/
  clase-01/
    inicio/
    final/
  ...
typescript/
  clase-01/
    inicio/
    final/
  ...
```

Además, el repositorio publica ramas remotas por clase:

- `clase-XX-inicio`
- `clase-XX-final`

## Configuración

```bash
cp .env.example .env
export ANTHROPIC_API_KEY="tu_api_key"
```

Nunca subas tu API key al repositorio. Usa variables de entorno en local, GitHub Actions, Railway o tu plataforma de deploy.

## Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python python/clase-01/final/main.py
```

Validación rápida:

```bash
python -m compileall python
```

## TypeScript

```bash
cd typescript
npm install
npm run clase:01:final
npm run typecheck
```

## Mapa del curso

| Clase | Tema |
| --- | --- |
| 01 | Quickstart: tu primera llamada a Claude API |
| 02 | Conversaciones multi-turn: el array de messages |
| 03 | Estrategias de gestión de contexto y tokens |
| 04 | Streaming de respuestas en tiempo real |
| 05 | Proyecto: chatbot con interfaz de terminal |
| 06 | Inputs multimedia: imágenes y documentos PDF |
| 07 | Outputs estructurados con JSON mode |
| 08 | Prompt engineering para extracción de datos |
| 09 | Proyecto: extractor de facturas en PDF |
| 10 | Tool use: cómo Claude llama funciones externas |
| 11 | Definir herramientas y manejar tool_result |
| 12 | Loop agentico: razonar → actuar → observar |
| 13 | Manejo de errores y seguridad en agentes |
| 14 | Proyecto: agente de búsqueda y resumen web |
| 15 | Prompt caching: reduce costos |
| 16 | Batch API para miles de requests |
| 17 | Rate limits, reintentos y observabilidad |
| 18 | Proyecto final: FastAPI + Railway |
