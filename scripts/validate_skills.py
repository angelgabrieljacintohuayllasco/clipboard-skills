#!/usr/bin/env python3
"""Valida que cada carpeta de skills/ cumpla el formato SKILL.md que leen
Claude Code y otros agentes compatibles con Agent Skills.

Reglas:
  - skills/<nombre>/SKILL.md existe
  - frontmatter YAML con `name` y `description`
  - `name` == nombre de la carpeta, minúsculas, letras/números/guiones, <= 64 chars
  - `description` no vacía, <= 260 chars; suma total <= 9000 (presupuesto del listado)
  - sin rutas personales (C:/Users/<x>, /home/<x>) ni correos

Uso: python scripts/validate_skills.py [ruta_a_skills]
Sale con código 1 si algo falla. Pensado para CI y para correr antes de commitear.
"""
import os
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "skills")
ROOT = os.path.abspath(ROOT)

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
PERSONAL_RE = re.compile(r"([A-Z]:[\/]Users[\/]|/home/[a-z]+/|/Users/[a-z]+/|[\w.+-]+@[\w-]+\.[a-z]{2,})", re.I)

# Claude Code reparte un presupuesto fijo de caracteres entre las descripciones de
# todas las skills instaladas. Si se pasa, las últimas del listado quedan sin
# descripción y el modelo nunca las elige. Descripciones cortas = auto-invocación.
MAX_DESC = 260
MAX_TOTAL_DESC = 9000

errors = []
count = 0
total_desc = 0

for entry in sorted(os.listdir(ROOT)):
    folder = os.path.join(ROOT, entry)
    if not os.path.isdir(folder) or entry.startswith("."):
        continue
    count += 1
    skill_md = os.path.join(folder, "SKILL.md")
    if not os.path.isfile(skill_md):
        errors.append(f"{entry}: falta SKILL.md")
        continue
    text = open(skill_md, encoding="utf-8").read()
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not m:
        errors.append(f"{entry}: SKILL.md sin frontmatter YAML (--- ... ---)")
        continue
    fm = m.group(1)
    name = re.search(r"^name:\s*(.+?)\s*$", fm, re.M)
    desc = re.search(r"^description:\s*(.+?)\s*$", fm, re.M)
    if not name:
        errors.append(f"{entry}: frontmatter sin `name`")
    else:
        n = name.group(1).strip().strip("'\"")
        if n != entry:
            errors.append(f"{entry}: name `{n}` no coincide con la carpeta")
        if not NAME_RE.match(n) or len(n) > 64:
            errors.append(f"{entry}: name inválido (minúsculas, guiones, <=64)")
    if not desc:
        errors.append(f"{entry}: frontmatter sin `description`")
    else:
        d = desc.group(1).strip().strip("'\"")
        if len(d) > MAX_DESC:
            errors.append(f"{entry}: description de {len(d)} chars (máx {MAX_DESC}); larga = truncada o fuera del listado = no se auto-invoca")
        total_desc += len(d)
        if len(d) < 40:
            errors.append(f"{entry}: description muy corta ({len(d)} chars); no va a disparar")
    for root, _, files in os.walk(folder):
        for f in files:
            if not f.endswith((".md", ".py", ".sh", ".ps1", ".txt", ".json")):
                continue
            p = os.path.join(root, f)
            body = open(p, encoding="utf-8", errors="replace").read()
            for hit in PERSONAL_RE.finditer(body):
                errors.append(f"{os.path.relpath(p, ROOT)}: dato personal/ruta local `{hit.group(0)}`")

if total_desc > MAX_TOTAL_DESC:
    errors.append(f"suma de descriptions = {total_desc} chars (máx {MAX_TOTAL_DESC}); el listado de skills se trunca")

if errors:
    print(f"FALLA — {len(errors)} problema(s) en {count} skills:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print(f"OK — {count} skills válidas en {ROOT} (descriptions: {total_desc} chars)")
