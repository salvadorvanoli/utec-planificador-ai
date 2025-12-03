#!/usr/bin/env pwsh
# =============================================================================
# SCRIPT: scripts/logs.ps1
# =============================================================================
# Muestra los logs del AI Agent
# =============================================================================

param(
    [Parameter()]
    [switch]$Follow,
    
    [Parameter()]
    [int]$Tail = 100
)

$ErrorActionPreference = "Stop"

# Cambiar al directorio raíz del proyecto
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Logs del AI Agent                      " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$args = @('logs')
if ($Follow) { $args += '--follow' }
$args += '--tail', $Tail
$args += 'ai-agent'

Write-Host "Mostrando logs del AI Agent" -ForegroundColor Yellow
Write-Host ""

& docker-compose @args

Write-Host ""
Write-Host "Uso:" -ForegroundColor Cyan
Write-Host "  .\scripts\logs.ps1 [-Follow] [-Tail <número>]" -ForegroundColor White
Write-Host ""
Write-Host "Ejemplos:" -ForegroundColor Cyan
Write-Host "  .\scripts\logs.ps1               # Últimos 100 logs" -ForegroundColor Gray
Write-Host "  .\scripts\logs.ps1 -Follow       # Seguir logs en tiempo real" -ForegroundColor Gray
Write-Host "  .\scripts\logs.ps1 -Tail 50      # Últimos 50 logs" -ForegroundColor Gray
Write-Host ""
