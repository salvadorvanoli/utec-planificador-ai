#!/usr/bin/env pwsh
# =============================================================================
# SCRIPT: scripts/status.ps1
# =============================================================================
# Muestra el estado del AI Agent
# =============================================================================

$ErrorActionPreference = "Stop"

# Cambiar al directorio raíz del proyecto
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Estado del AI Agent                    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[Contenedores]" -ForegroundColor Blue
docker-compose ps

Write-Host ""
Write-Host "[Health Checks]" -ForegroundColor Blue

# Check AI Agent
Write-Host "  AI Agent API..." -NoNewline
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 3 -UseBasicParsing -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        $healthData = $response.Content | ConvertFrom-Json
        if ($healthData.status -eq "healthy") {
            Write-Host " OK" -ForegroundColor Green
        }
        else {
            Write-Host " WARN (Status: $($healthData.status))" -ForegroundColor Yellow
        }
    }
    else {
        Write-Host " WARN (HTTP: $($response.StatusCode))" -ForegroundColor Yellow
    }
}
catch {
    Write-Host " NO RESPONDE" -ForegroundColor Red
}

# Check Docker health status
Write-Host "  Docker Health..." -NoNewline
try {
    $healthStatus = docker inspect --format='{{.State.Health.Status}}' utec-planificador-ai-agent 2>$null
    if ($LASTEXITCODE -eq 0) {
        switch ($healthStatus) {
            "healthy" { Write-Host " OK" -ForegroundColor Green }
            "unhealthy" { Write-Host " UNHEALTHY" -ForegroundColor Red }
            "starting" { Write-Host " STARTING..." -ForegroundColor Yellow }
            default { Write-Host " UNKNOWN" -ForegroundColor Yellow }
        }
    }
    else {
        Write-Host " NO DISPONIBLE" -ForegroundColor Red
    }
}
catch {
    Write-Host " ERROR" -ForegroundColor Red
}

Write-Host ""
Write-Host "[Endpoints]" -ForegroundColor Blue
Write-Host "  API:          http://localhost:8000" -ForegroundColor White
Write-Host "  Health:       http://localhost:8000/health" -ForegroundColor White
Write-Host "  Docs:         http://localhost:8000/docs" -ForegroundColor White
Write-Host "  ReDoc:        http://localhost:8000/redoc" -ForegroundColor White

Write-Host ""
Write-Host "[Uso de Recursos]" -ForegroundColor Blue
try {
    $stats = docker stats --no-stream --format "table {{.Name}}`t{{.CPUPerc}}`t{{.MemUsage}}`t{{.NetIO}}" | Select-String "ai-agent"
    if ($stats) {
        Write-Host $stats -ForegroundColor White
    }
    else {
        Write-Host "  Contenedor no encontrado" -ForegroundColor Red
    }
}
catch {
    Write-Host "  No disponible" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[Integración con Backend]" -ForegroundColor Blue
Write-Host "  Backend debe configurar:" -ForegroundColor Yellow
Write-Host "    AI_AGENT_BASE_URL=http://host.docker.internal:8000" -ForegroundColor Gray
Write-Host ""
