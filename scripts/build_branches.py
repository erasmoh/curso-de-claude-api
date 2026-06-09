#!/usr/bin/env python3
"""Reconstruye las ramas por clase (modelo estilo Platzi).

Cada clase publica dos ramas aisladas:

- ``clase-XX-inicio``: punto de partida (solo la carpeta ``inicio`` de esa clase).
- ``clase-XX-final``: solución (solo la carpeta ``final`` de esa clase).

A diferencia de ``main`` (que contiene las 18 clases), cada rama contiene
únicamente el contenido de **una** clase, en ambos lenguajes (Python y
TypeScript), más los archivos de configuración compartidos.

El contenido se extrae de un ref fuente (por defecto ``origin/main``) usando
git plumbing, así que el script NO toca tu working tree ni archivos locales
como ``.env.local`` o ``.venv``.

Uso:

    python scripts/build_branches.py            # construye ramas locales
    SOURCE_REF=main python scripts/build_branches.py
    python scripts/build_branches.py --push     # construye y hace force-push

Nota: el ref/rama actualmente en checkout no puede actualizarse. Haz
``git switch --detach`` antes de correrlo si estás parado en una rama de clase.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from generate_course import CLASSES  # noqa: E402  (reutiliza títulos/objetivos)

SOURCE = os.environ.get("SOURCE_REF", "origin/main")
VARIANTS = ("inicio", "final")

# Archivos de configuración idénticos en todas las ramas.
SHARED_FILES = (
    ".env.example",
    ".gitignore",
    "pyproject.toml",
    "python/README.md",
    "typescript/README.md",
    "typescript/package.json",
    "typescript/package-lock.json",
    "typescript/tsconfig.json",
)

ROOT = Path(
    subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
)


def git(*args: str, input_bytes: bytes | None = None, env: dict | None = None) -> bytes:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        input=input_bytes,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} falló:\n{result.stderr.decode('utf-8', 'replace')}"
        )
    return result.stdout


def show(path: str) -> bytes:
    """Contenido del archivo `path` en el ref fuente."""
    return git("show", f"{SOURCE}:{path}")


def hash_object(content: bytes) -> str:
    return git("hash-object", "-w", "--stdin", input_bytes=content).decode().strip()


_SHARED_CACHE: dict[str, str] = {}


def shared_blob(path: str) -> str:
    if path not in _SHARED_CACHE:
        _SHARED_CACHE[path] = hash_object(show(path))
    return _SHARED_CACHE[path]


def branch_readme(number: int, title: str, objective: str, variant: str) -> bytes:
    nn = f"{number:02d}"
    if variant == "inicio":
        descripcion = "Punto de partida con TODOs para resolver en vivo durante la clase."
    else:
        descripcion = "Solución completa y comentada de la clase."
    text = f"""# Curso de Claude API — Clase {nn}: {title}

Esta rama es el checkpoint **{variant}** de la clase {nn}.

{descripcion}

## Contenido de esta rama

- `python/clase-{nn}/{variant}/main.py` — versión Python (ruta principal).
- `typescript/clase-{nn}/{variant}/main.ts` — versión TypeScript (ruta alternativa).

## Cómo ejecutar

```bash
cp .env.example .env
export ANTHROPIC_API_KEY="tu_api_key"

# Python
python python/clase-{nn}/{variant}/main.py

# TypeScript
cd typescript && npm install && npm run clase:{nn}:{variant}
```

## Navegación del curso

- `clase-XX-inicio`: punto de partida de cada clase.
- `clase-XX-final`: solución de cada clase.
- `main`: curso completo (todas las clases) y el generador.

> Objetivo de la clase: {objective}
"""
    return text.encode("utf-8")


def build_branch(number: int, title: str, objective: str, variant: str) -> tuple[str, str]:
    nn = f"{number:02d}"
    slug = f"clase-{nn}"
    branch = f"{slug}-{variant}"

    index_file = ROOT / ".git" / f"tmp-index-{branch}"
    if index_file.exists():
        index_file.unlink()
    env = dict(os.environ, GIT_INDEX_FILE=str(index_file))

    entries: list[tuple[str, str]] = [(p, shared_blob(p)) for p in SHARED_FILES]
    entries.append((f"python/{slug}/README.md", hash_object(show(f"python/{slug}/README.md"))))
    entries.append((f"typescript/{slug}/README.md", hash_object(show(f"typescript/{slug}/README.md"))))
    entries.append((f"python/{slug}/{variant}/main.py", hash_object(show(f"python/{slug}/{variant}/main.py"))))
    entries.append((f"typescript/{slug}/{variant}/main.ts", hash_object(show(f"typescript/{slug}/{variant}/main.ts"))))
    entries.append(("README.md", hash_object(branch_readme(number, title, objective, variant))))

    for path, sha in entries:
        git("update-index", "--add", "--cacheinfo", f"100644,{sha},{path}", env=env)

    tree = git("write-tree", env=env).decode().strip()
    commit = git("commit-tree", tree, "-m", f"Clase {nn} - {variant}: {title}").decode().strip()
    git("branch", "-f", branch, commit)

    index_file.unlink(missing_ok=True)
    return branch, commit


def main() -> None:
    push = "--push" in sys.argv[1:]
    built: list[str] = []
    for number, title, objective in CLASSES:
        for variant in VARIANTS:
            branch, commit = build_branch(number, title, objective, variant)
            built.append(branch)
            print(f"  {branch:<18} -> {commit[:10]}")

    print(f"\nConstruidas {len(built)} ramas locales desde {SOURCE}.")

    if push:
        print("\nForce-push a origin...")
        git("push", "--force-with-lease", "origin", *built)
        print("Push completado.")
    else:
        print("Para publicar: python scripts/build_branches.py --push")


if __name__ == "__main__":
    main()
