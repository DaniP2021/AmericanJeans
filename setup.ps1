# Prepara esta PC para trabajar con el catálogo.
#
#   .\setup.ps1              -> dependencias + modelo chico (4,5 MB)
#   .\setup.ps1 -Completo    -> además el modelo grande (167 MB), mejor calidad de recorte
#
# No toca el sistema: todo queda dentro del proyecto, en .pylibs y .models.

param([switch]$Completo)

$ErrorActionPreference = "Stop"
$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $raiz

function Buscar-Python {
    foreach ($candidato in @("python", "py", "python3")) {
        $cmd = Get-Command $candidato -ErrorAction SilentlyContinue
        if ($cmd) {
            $version = & $cmd.Source -c "import sys; print(sys.version_info[:2])" 2>$null
            if ($LASTEXITCODE -eq 0) { return $cmd.Source }
        }
    }
    return $null
}

$python = Buscar-Python
if (-not $python) {
    Write-Host ""
    Write-Host "No encontré Python." -ForegroundColor Red
    Write-Host "Instalalo desde https://www.python.org/downloads/ marcando 'Add Python to PATH'."
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Host "Preparando el proyecto con $python" -ForegroundColor Cyan
Write-Host ""

$args = @("arquitectura-agente-tienda/qa/bootstrap.py")
if ($Completo) { $args += "--completo" }

& $python @args
exit $LASTEXITCODE
