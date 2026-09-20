# Instala (o actualiza) las skills de este repo en el directorio de skills del agente.
# Uso: .\install.ps1 [-Dest <ruta>] [-Skills nombre1,nombre2]
#   -Dest por defecto: $HOME\.claude\skills (Claude Code). Otros agentes: pasa su ruta.
#   sin -Skills: instala todas.
param(
  [string]$Dest = (Join-Path $HOME ".claude\skills"),
  [string[]]$Skills = @()
)
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
New-Item -ItemType Directory -Force -Path $Dest | Out-Null
if ($Skills.Count -eq 0) {
  $Skills = Get-ChildItem -Directory (Join-Path $here "skills") | Select-Object -ExpandProperty Name
}
$n = 0
foreach ($name in $Skills) {
  $src = Join-Path $here "skills\$name"
  if (-not (Test-Path $src)) { Write-Warning "no existe: $name"; continue }
  $dst = Join-Path $Dest $name
  if (Test-Path $dst) { Remove-Item -Recurse -Force $dst }
  Copy-Item -Recurse $src $dst
  $n++
  Write-Host "  + $name"
}
Write-Host "$n skills instaladas en $Dest"
