# Ruta Python

Python es la ruta principal del curso. Cada clase tiene:

- `inicio/main.py`: ejercicio guiado con TODOs.
- `final/main.py`: implementación completa y comentada.

> Todos los comandos de abajo se ejecutan **desde la carpeta de la clase** que quieras
> trabajar (por ejemplo `python/clase-01`). Como `requirements.txt` y `pyproject.toml`
> viven en la raíz del repo, se referencian con `../../`.

## Requisitos

- Python 3.11 o superior.

## Instalación

```bash
# Sitúate en la carpeta de la clase que quieras trabajar
cd python/clase-01

# 1. Crear y activar un entorno virtual (una vez por clase)
python -m venv .venv
source .venv/bin/activate          # En Windows: .venv\Scripts\activate

# 2. Instalar dependencias (requirements.txt está en la raíz del repo)
pip install -r ../../requirements.txt
```

Dependencias principales: `anthropic`, `fastapi`, `pydantic`, `python-dotenv` y `uvicorn[standard]`.

> Alternativa: las dependencias también están declaradas en `pyproject.toml`, así que
> puedes instalar el proyecto como paquete editable con `pip install -e ../..`
> (o `pip install -e "../..[dev]"` para incluir las herramientas `ruff` y `mypy`).

## Configurar la API key

```bash
cp ../../.env.example .env         # luego edita .env con tu clave real
# o expórtala directamente en la terminal:
export ANTHROPIC_API_KEY="tu_api_key"
```

## Validación

```bash
# Compila la clase actual para detectar errores de sintaxis
python -m compileall final inicio
```

## Ejecutar una clase

```bash
# Solución completa
python final/main.py

# Ejercicio guiado (inicio)
python inicio/main.py
```

## Ejecutar la clase 16 (frontend + FastAPI)

La clase 16 es una app web servida con FastAPI, así que se levanta con `uvicorn`:

```bash
# (estando dentro de python/clase-16)
uvicorn --app-dir final main:app --reload
```

Abre http://127.0.0.1:8000 para probar el chatbot, el extractor JSON y el agente desde el navegador.
