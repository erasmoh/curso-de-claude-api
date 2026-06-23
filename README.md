# Curso de Claude API

Repositorio para el curso **Construyendo aplicaciones con Claude API**.

- 15 clases.
- 3 proyectos.
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

## Ramas por clase (estilo Platzi)

Además de las carpetas, cada clase se publica como una **rama aislada**: al hacer
checkout solo verás el contenido de esa clase (Python y TypeScript), no las 17.

- `clase-XX-inicio`: punto de partida para resolver en vivo.
- `clase-XX-final`: solución completa de la clase.

```bash
git fetch origin
git checkout clase-01-inicio   # solo verás python/clase-01 y typescript/clase-01
```

La rama `main` contiene el curso completo (todas las clases) y el generador.
Para reconstruir las ramas desde el contenido de `main`:

```bash
git switch --detach
python scripts/build_branches.py --push
```

## Configuración común

```bash
cp .env.example .env
export ANTHROPIC_API_KEY="tu_api_key"
```

Nunca subas tu API key al repositorio. Usa variables de entorno en local, GitHub Actions, Railway o tu plataforma de deploy.

Modelo usado en los ejemplos del guión:

```text
claude-sonnet-4-6
```

Revisa la documentación de Anthropic antes de grabar, porque los nombres de modelos pueden cambiar con el tiempo.

## Python

La carpeta `python/` es la ruta principal del curso. Úsala si quieres seguir las clases exactamente como están planteadas en el temario.

### Requerimientos

- Python 3.11 o superior.
- `pip` y `venv`.
- Una API key de Anthropic configurada como `ANTHROPIC_API_KEY`.
- Conocimiento intermedio de Python: funciones, clases, errores, archivos y consumo de APIs.

### Instalar dependencias

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Ejecutar una clase

Cada clase tiene un punto de partida y una solución:

```bash
# Punto de partida para resolver en vivo
python python/clase-01/inicio/main.py

# Solución final de la clase
python python/clase-01/final/main.py
```

Validación rápida:

```bash
python -m compileall python
```

## TypeScript

La carpeta `typescript/` es la ruta alternativa para comparar cómo se implementan los mismos conceptos con Node.js y TypeScript.

### Requerimientos

- Node.js 20 o superior.
- npm 10 o superior.
- Una API key de Anthropic configurada como `ANTHROPIC_API_KEY`.
- Conocimiento básico/intermedio de TypeScript: módulos ES, async/await, tipos y manejo de errores.

### Instalar dependencias

```bash
cd typescript
npm install
```

### Ejecutar una clase

Los scripts siguen el patrón `clase:XX:inicio` y `clase:XX:final`:

```bash
# Punto de partida para resolver en vivo
npm run clase:01:inicio

# Solución final de la clase
npm run clase:01:final
```

Validación rápida:

```bash
npm run typecheck
```

## Cómo elegir entre Python y TypeScript

- Usa **Python** para seguir el curso principal, los proyectos base y la versión que se despliega con FastAPI.
- Usa **TypeScript** cuando quieras mostrar la alternativa equivalente para estudiantes que trabajan con Node.js.
- Ambas rutas usan la misma API key y cubren los mismos conceptos por clase.
- Puedes comparar `python/clase-XX/final/main.py` contra `typescript/clase-XX/final/main.ts` para explicar diferencias de SDK, tipos y estilo.

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
| 09 | Tool use: cómo Claude llama funciones externas |
| 10 | Definir herramientas y manejar tool_result |
| 11 | Loop agentico: razonar → actuar → observar |
| 12 | Manejo de errores y seguridad en agentes |
| 13 | Prompt caching: reduce costos |
| 14 | Batch API para miles de requests |
| 15 | Proyecto final: frontend + hub con FastAPI |
