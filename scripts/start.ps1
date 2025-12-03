#!/usr/bin/env pwsh
# =============================================================================
# SCRIPT: scripts/start.ps1
# =============================================================================
# Inicia el AI Agent del Planificador Docente UTEC
# Microservicio de IA con FastAPI + OpenAI
# 
# Uso:
#   .\scripts\start.ps1              # Inicia en modo desarrollo
#   .\scripts\start.ps1 -Production  # Inicia en modo producción
# =============================================================================

param(
    [switch]$Production = $false
)

$ErrorActionPreference = "Stop"

# Cambiar al directorio raíz del proyecto
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Iniciando AI Agent - Planificador UTEC" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Docker
try {
    docker --version | Out-Null
    Write-Host "[OK] Docker disponible" -ForegroundColor Green
}
catch {
    Write-Host "[ERROR] Docker no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Instala Docker desde: https://docs.docker.com/get-docker/" -ForegroundColor Yellow
    exit 1
}

# Verificar/Crear red compartida
$sharedNetworkName = "utec-shared-network"
try {
    $networkExists = docker network ls --format "{{.Name}}" | Select-String -Pattern "^$sharedNetworkName$" -Quiet
    
    if (-not $networkExists) {
        Write-Host "[INFO] Creando red compartida: $sharedNetworkName" -ForegroundColor Yellow
        docker network create $sharedNetworkName | Out-Null
        Write-Host "[OK] Red compartida creada" -ForegroundColor Green
    }
    else {
        Write-Host "[OK] Red compartida disponible: $sharedNetworkName" -ForegroundColor Green
    }
}
catch {
    Write-Host "[ADVERTENCIA] No se pudo verificar/crear la red compartida" -ForegroundColor Yellow
}

# Verificar .env
if (-not (Test-Path ".env")) {
    Write-Host "[ADVERTENCIA] Archivo .env no encontrado" -ForegroundColor Yellow
    
    if (Test-Path ".env.example") {
        Write-Host "[INFO] Creando .env desde .env.example..." -ForegroundColor Yellow
        Copy-Item ".env.example" ".env"
        Write-Host "[OK] Archivo .env creado" -ForegroundColor Green
        Write-Host "[ACCION REQUERIDA] Edita el archivo .env con tu OPENAI_KEY" -ForegroundColor Yellow
        Write-Host "Ejecuta: code .env" -ForegroundColor Cyan
        Write-Host ""
    }
    else {
        Write-Host "[ERROR] Tampoco existe .env.example" -ForegroundColor Red
        exit 1
    }
}
else {
    Write-Host "[OK] Archivo .env encontrado" -ForegroundColor Green
}

# Verificar OPENAI_KEY
$envContent = Get-Content ".env" -Raw
if ($envContent -match "OPENAI_KEY=your-openai-api-key-here" -or $envContent -notmatch "OPENAI_KEY=sk-") {
    Write-Host "[ERROR] OPENAI_KEY no está configurada correctamente en .env" -ForegroundColor Red
    Write-Host "Por favor, edita .env y agrega tu API Key de OpenAI" -ForegroundColor Yellow
    Write-Host "Obtén tu API Key en: https://platform.openai.com/api-keys" -ForegroundColor Cyan
    exit 1
}

Write-Host ""

# Determinar modo de ejecución
if ($Production) {
    Write-Host "[INFO] Iniciando en modo PRODUCCIÓN" -ForegroundColor Cyan
    Write-Host "[INFO] Configuración: 4 workers, resource limits" -ForegroundColor Yellow
    Write-Host "[PASO 1/3] Iniciando servicios..." -ForegroundColor Blue
    docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
}
else {
    Write-Host "[INFO] Iniciando en modo DESARROLLO" -ForegroundColor Yellow
    Write-Host "[INFO] Configuración: Hot-reload habilitado, logs DEBUG" -ForegroundColor Yellow
    Write-Host "[INFO] Para modo producción, usa: .\scripts\start.ps1 -Production" -ForegroundColor Gray
    Write-Host "[PASO 1/3] Iniciando servicios..." -ForegroundColor Blue
    docker-compose up -d --build
}

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[ERROR] Falló el inicio del servicio" -ForegroundColor Red
    exit 1
}

Write-Host "[OK] Contenedor iniciado" -ForegroundColor Green
Write-Host ""

Write-Host "[PASO 2/3] Esperando que el AI Agent esté listo..." -ForegroundColor Blue

$maxAttempts = 40
$attempt = 0
$agentReady = $false

while ($attempt -lt $maxAttempts) {
    $attempt++
    
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 2 -UseBasicParsing -ErrorAction Stop
        if ($response.StatusCode -eq 200) {
            $agentReady = $true
            break
        }
    }
    catch {
        # Ignorar errores de conexión
    }
    
    if ($attempt -eq 1 -or $attempt % 5 -eq 0) {
        Write-Host "  Intento $attempt/$maxAttempts..." -ForegroundColor Gray
    }
    Start-Sleep -Seconds 2
}

Write-Host ""

if ($agentReady) {
    Write-Host "========================================" -ForegroundColor Green
    Write-Host " AI AGENT INICIADO CORRECTAMENTE       " -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Servicios disponibles:" -ForegroundColor Cyan
    Write-Host "  API:          http://localhost:8000" -ForegroundColor White
    Write-Host "  Health:       http://localhost:8000/health" -ForegroundColor White
    Write-Host "  Docs:         http://localhost:8000/docs" -ForegroundColor White
    Write-Host "  ReDoc:        http://localhost:8000/redoc" -ForegroundColor White
    Write-Host ""
    Write-Host "Endpoints principales:" -ForegroundColor Cyan
    Write-Host "  Chat:         POST /agent/chat/message" -ForegroundColor White
    Write-Host "  Suggestions:  POST /agent/suggestions" -ForegroundColor White
    Write-Host "  Report:       POST /agent/report/generate" -ForegroundColor White
    Write-Host ""
    Write-Host "Comandos útiles:" -ForegroundColor Cyan
    Write-Host "  Ver logs:     .\scripts\logs.ps1" -ForegroundColor White
    Write-Host "  Ver estado:   .\scripts\status.ps1" -ForegroundColor White
    Write-Host "  Detener:      .\scripts\stop.ps1" -ForegroundColor White
    Write-Host ""
    
    if ($Production) {
        Write-Host "Modo: PRODUCCIÓN (4 workers)" -ForegroundColor Green
    }
    else {
        Write-Host "Modo: DESARROLLO (hot-reload)" -ForegroundColor Yellow
    }
    
    Write-Host ""
}
else {
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host " AI AGENT INICIADO CON ADVERTENCIAS    " -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "El servicio está tardando en iniciar. Esto puede ser normal." -ForegroundColor Yellow
    Write-Host "Verifica el estado con: .\scripts\logs.ps1 -Follow" -ForegroundColor Cyan
    Write-Host ""
}
