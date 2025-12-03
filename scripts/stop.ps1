#!/usr/bin/env pwsh
# =============================================================================
# SCRIPT: scripts/stop.ps1
# =============================================================================
# Detiene el AI Agent del Planificador Docente UTEC
# =============================================================================

$ErrorActionPreference = "Stop"

# Cambiar al directorio raíz del proyecto
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Deteniendo AI Agent                    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

docker-compose down

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "[OK] AI Agent detenido correctamente" -ForegroundColor Green
    Write-Host ""
}
else {
    Write-Host ""
    Write-Host "[ERROR] Hubo un problema al detener el AI Agent" -ForegroundColor Red
    Write-Host ""
    exit 1
}
