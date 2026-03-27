param(
    [string]$BackendHost = "127.0.0.1",
    [int]$BackendPort = 18787,
    [switch]$SkipBuild
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendRoot = Join-Path $RepoRoot "backend-agent"
$BackendPython = Join-Path $BackendRoot ".venv\Scripts\python.exe"
$BackendRunScript = Join-Path $BackendRoot "run-dev.ps1"
$BackendSetupScript = Join-Path $BackendRoot "setup.ps1"
$VPetProject = Join-Path $RepoRoot "VPet-Simulator.Windows\VPet-Simulator.Windows.csproj"
$VPetExe = Join-Path $RepoRoot "VPet-Simulator.Windows\bin\x64\Debug\net8.0-windows\VPet-Simulator.Windows.exe"
$VPetModLink = Join-Path $RepoRoot "VPet-Simulator.Windows\bin\x64\Debug\net8.0-windows\mod"
$VPetModTarget = Join-Path $RepoRoot "VPet-Simulator.Windows\mod"
$BackendWindowTitle = "VPet Backend :$BackendPort"
$VPetWindowTitle = "VPet Body :$BackendPort"

function Get-DotnetCommand {
    if (Get-Command dotnet -ErrorAction SilentlyContinue) {
        return "dotnet"
    }

    $fallback = "C:\Program Files\dotnet\dotnet.exe"
    if (Test-Path $fallback) {
        return $fallback
    }

    throw ".NET SDK 未找到。请先安装 .NET 8 SDK。"
}

function Ensure-BackendEnvironment {
    if (Test-Path $BackendPython) {
        Write-Host "[OK] 检测到后端虚拟环境: $BackendPython" -ForegroundColor Green
        return
    }

    Write-Host "[STEP] 未检测到 backend-agent\\.venv，开始初始化后端环境" -ForegroundColor Yellow
    & $BackendSetupScript
    if (-not (Test-Path $BackendPython)) {
        throw "后端虚拟环境初始化失败，未找到 $BackendPython"
    }
}

function Stop-ProcessIfRunning {
    param(
        [string]$Name
    )

    Get-Process -Name $Name -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
}

function Stop-BackendByPort {
    try {
        $owningProcessIds = Get-NetTCPConnection -LocalPort $BackendPort -State Listen -ErrorAction Stop |
            Select-Object -ExpandProperty OwningProcess -Unique
        foreach ($processId in $owningProcessIds) {
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
    } catch {
        $netstatOutput = netstat -ano | Select-String ":$BackendPort\s+.*LISTENING\s+(\d+)$"
        foreach ($line in $netstatOutput) {
            $processId = [int]($line.Matches[0].Groups[1].Value)
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
        }
    }
}

function Restart-ExistingProcesses {
    Write-Host "[STEP] 关闭旧的 VPet / 后端进程" -ForegroundColor Yellow
    Stop-ProcessIfRunning -Name "VPet-Simulator.Windows"
    Stop-BackendByPort
}

function Ensure-VPetModLink {
    if (Test-Path $VPetModLink) {
        return
    }

    Write-Host "[STEP] 创建 VPet mod 符号链接" -ForegroundColor Yellow
    try {
        New-Item -ItemType SymbolicLink -Path $VPetModLink -Target $VPetModTarget -Force | Out-Null
    } catch {
        throw "创建 mod 符号链接失败。请以管理员身份运行终端，或先手动执行 cmd /c .\VPet-Simulator.Windows\mklink.bat"
    }
}

function Build-VPet {
    $dotnet = Get-DotnetCommand
    Write-Host "[STEP] 编译 VPet-Simulator.Windows (Debug x64)" -ForegroundColor Yellow
    & $dotnet build $VPetProject -c Debug -p:Platform=x64
}

function Start-Backend {
    Write-Host "[STEP] 启动后端 FastAPI 服务" -ForegroundColor Yellow
    $backendCommand = @(
        "`$env:PET_BACKEND_HOST='$BackendHost'"
        "`$env:PET_BACKEND_PORT='$BackendPort'"
        "Set-Location '$BackendRoot'"
        "& '$BackendRunScript'"
    ) -join "; "

    Start-Process -FilePath "powershell.exe" -ArgumentList @(
        "-NoExit",
        "-ExecutionPolicy", "Bypass",
        "-Command", $backendCommand
    ) -WindowStyle Normal | Out-Null
}

function Start-VPet {
    Write-Host "[STEP] 启动 VPet" -ForegroundColor Yellow
    $env:VPET_AGENT_BRIDGE_URL = "http://$BackendHost`:$BackendPort/vpet/events/next"
    Start-Process -FilePath $VPetExe -WorkingDirectory (Split-Path -Parent $VPetExe) | Out-Null
}

Set-Location $RepoRoot

Ensure-BackendEnvironment
Restart-ExistingProcesses
if (-not $SkipBuild) {
    Build-VPet
}
Ensure-VPetModLink
Start-Backend
Start-Sleep -Seconds 2
Start-VPet

Write-Host ""
Write-Host "一键启动已执行：" -ForegroundColor Green
Write-Host "后端测试页: http://$BackendHost`:$BackendPort/dev/control" -ForegroundColor Cyan
Write-Host "VPet 事件桥接: http://$BackendHost`:$BackendPort/vpet/events/next" -ForegroundColor Cyan
Write-Host "编译模式: $(if ($SkipBuild) { '跳过编译' } else { '重新编译并启动' })" -ForegroundColor Cyan
Write-Host ""
Write-Host "如果后端窗口报缺依赖，请先单独运行: .\backend-agent\setup.ps1" -ForegroundColor Yellow
