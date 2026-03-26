$ErrorActionPreference = "Stop"

$VenvPath = Join-Path $PSScriptRoot ".venv"
$RequirementsPath = Join-Path $PSScriptRoot "requirements.txt"
$ScriptsPath = Join-Path $VenvPath "Scripts"
$VenvPython = Join-Path $ScriptsPath "python.exe"
$ActivatePs1 = Join-Path $ScriptsPath "Activate.ps1"
$ActivateBat = Join-Path $ScriptsPath "activate.bat"
$ActivateSh = Join-Path $ScriptsPath "activate"

function Get-PythonCommand {
    try {
        $py311 = py -3.11 --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            return @{
                Command = "py"
                Arguments = @("-3.11")
                Version = ($py311 | Out-String).Trim()
            }
        }
    } catch {}

    try {
        $pythonVer = python --version 2>&1
        if ($LASTEXITCODE -eq 0 -and ($pythonVer | Out-String) -match "3\.11") {
            return @{
                Command = "python"
                Arguments = @()
                Version = ($pythonVer | Out-String).Trim()
            }
        }
    } catch {}

    return $null
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Backend 环境初始化脚本 (Python 3.11)" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if (Test-Path $VenvPath) {
    Write-Host "[INFO] 虚拟环境已存在: $VenvPath" -ForegroundColor Yellow
} else {
    Write-Host "[STEP 1] 检查 Python 3.11..." -ForegroundColor Green

    $pythonInfo = Get-PythonCommand
    if (-not $pythonInfo) {
        Write-Host "[ERROR] 未找到 Python 3.11，请先安装。" -ForegroundColor Red
        Write-Host "下载地址: https://www.python.org/downloads/" -ForegroundColor Yellow
        exit 1
    }

    Write-Host "[OK] 使用 Python: $($pythonInfo.Version)" -ForegroundColor Green
    Write-Host "[STEP 2] 创建虚拟环境..." -ForegroundColor Green

    & $pythonInfo.Command @($pythonInfo.Arguments) -m venv $VenvPath
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path $VenvPython)) {
        Write-Host "[ERROR] 创建虚拟环境失败" -ForegroundColor Red
        exit 1
    }

    Write-Host "[OK] 虚拟环境创建成功" -ForegroundColor Green
}

Write-Host "[STEP 3] 检查激活脚本..." -ForegroundColor Green
$missingScripts = @()
if (-not (Test-Path $ActivatePs1)) { $missingScripts += "Activate.ps1" }
if (-not (Test-Path $ActivateBat)) { $missingScripts += "activate.bat" }
if (-not (Test-Path $ActivateSh)) { $missingScripts += "activate" }

if ($missingScripts.Count -gt 0) {
    Write-Host "[WARN] 缺少脚本: $($missingScripts -join ', ')" -ForegroundColor Yellow
} else {
    Write-Host "[OK] 激活脚本已生成" -ForegroundColor Green
    Write-Host "  - Activate.ps1 (PowerShell)" -ForegroundColor Gray
    Write-Host "  - activate.bat (CMD)" -ForegroundColor Gray
    Write-Host "  - activate     (Bash/Git Bash)" -ForegroundColor Gray
}

Write-Host "[STEP 4] 安装依赖..." -ForegroundColor Green

if (-not (Test-Path $VenvPython)) {
    Write-Host "[ERROR] 未找到虚拟环境中的 python.exe: $VenvPython" -ForegroundColor Red
    exit 1
}

& $VenvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Host "[WARN] pip 升级失败，将继续安装 requirements.txt" -ForegroundColor Yellow
}

if (Test-Path $RequirementsPath) {
    & $VenvPython -m pip install -r $RequirementsPath
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[WARN] 部分依赖安装失败，请检查 requirements.txt" -ForegroundColor Yellow
        exit 1
    }

    Write-Host "[OK] 依赖安装完成" -ForegroundColor Green
} else {
    Write-Host "[WARN] requirements.txt 不存在，跳过依赖安装" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  初始化完成" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "手动激活命令:" -ForegroundColor White
Write-Host "  PowerShell: .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
Write-Host "  CMD:        .\.venv\Scripts\activate.bat" -ForegroundColor Yellow
Write-Host "启动后端:     .\run-dev.ps1" -ForegroundColor Yellow
Write-Host ""
