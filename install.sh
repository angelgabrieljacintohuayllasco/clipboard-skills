#!/usr/bin/env bash
# Instala (o actualiza) las skills de este repo en el directorio de skills del agente.
# Uso: ./install.sh [destino] [skill1 skill2 ...]
#   destino por defecto: ~/.claude/skills (Claude Code). Otros agentes: pasa su ruta.
#   sin lista de skills: instala todas.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${1:-$HOME/.claude/skills}"
shift || true
mkdir -p "$DEST"
if [ $# -eq 0 ]; then
  set -- "$HERE"/skills/*/
fi
n=0
for s in "$@"; do
  name="$(basename "${s%/}")"
  src="$HERE/skills/$name"
  [ -d "$src" ] || { echo "no existe: $name" >&2; continue; }
  rm -rf "$DEST/$name"
  cp -r "$src" "$DEST/$name"
  n=$((n+1))
  echo "  + $name"
done
echo "$n skills instaladas en $DEST"
