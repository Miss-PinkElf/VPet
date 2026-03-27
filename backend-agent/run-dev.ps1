$ErrorActionPreference = "Stop"
$ScriptRoot = $PSScriptRoot
$VenvPython = Join-Path $ScriptRoot ".venv\Scripts\python.exe"

if (Test-Path $VenvPython) {
    $pythonCmd = $VenvPython
} else {
    $pythonCmd = "python"
}

$hostValue = if ($env:PET_BACKEND_HOST) { $env:PET_BACKEND_HOST } else { "127.0.0.1" }
$portValue = if ($env:PET_BACKEND_PORT) { $env:PET_BACKEND_PORT } else { "18787" }

Set-Location $ScriptRoot
& $pythonCmd -m uvicorn app.main:app --host $hostValue --port $portValue --reload
