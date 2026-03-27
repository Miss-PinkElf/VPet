param(
    [switch]$Reload
)

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
$reloadValue = if ($Reload.IsPresent) {
    $true
} elseif ($env:PET_BACKEND_RELOAD) {
    @("1", "true", "yes", "on") -contains $env:PET_BACKEND_RELOAD.ToLowerInvariant()
} else {
    $false
}

Set-Location $ScriptRoot
$uvicornArgs = @(
    "-m", "uvicorn",
    "app.main:app",
    "--host", $hostValue,
    "--port", $portValue
)

if ($reloadValue) {
    $uvicornArgs += "--reload"
}

& $pythonCmd @uvicornArgs
