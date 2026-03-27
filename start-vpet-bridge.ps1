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
$VPetSetting = Join-Path $RepoRoot "VPet-Simulator.Windows\bin\x64\Debug\net8.0-windows\Setting.lps"
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

function Get-BackendListeningProcessIds {
    $processIds = @()

    try {
        $processIds += @(Get-NetTCPConnection -LocalPort $BackendPort -State Listen -ErrorAction Stop |
            Select-Object -ExpandProperty OwningProcess -Unique)
    } catch {
    }

    $netstatOutput = netstat -ano | Select-String ":$BackendPort\s+.*LISTENING\s+(\d+)$"
    foreach ($line in $netstatOutput) {
        $processIds += [int]($line.Matches[0].Groups[1].Value)
    }

    return $processIds | Select-Object -Unique
}

function Get-BackendCandidateProcessIds {
    $candidateIds = New-Object 'System.Collections.Generic.HashSet[int]'

    foreach ($processId in (Get-BackendListeningProcessIds)) {
        $null = $candidateIds.Add([int]$processId)
    }

    Get-CimInstance Win32_Process |
        Where-Object {
            $_.CommandLine -and (
                ($_.CommandLine -like "*$BackendRunScript*") -or
                ($_.CommandLine -like "*app.main:app*" -and $_.CommandLine -like "*--port $BackendPort*")
            )
        } |
        ForEach-Object {
            $null = $candidateIds.Add([int]$_.ProcessId)
        }

    return @($candidateIds)
}

function Stop-ProcessTree {
    param(
        [int]$ProcessId,
        [System.Collections.Generic.HashSet[int]]$Visited
    )

    if (-not $Visited.Add($ProcessId)) {
        return
    }

    $children = @(Get-CimInstance Win32_Process -Filter "ParentProcessId = $ProcessId" -ErrorAction SilentlyContinue |
        Select-Object -ExpandProperty ProcessId)
    foreach ($childId in $children) {
        Stop-ProcessTree -ProcessId $childId -Visited $Visited
    }

    Stop-Process -Id $ProcessId -Force -ErrorAction SilentlyContinue
}

function Wait-BackendPortReleased {
    param(
        [int]$TimeoutSeconds = 12
    )

    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    while ((Get-Date) -lt $deadline) {
        if ((Get-BackendListeningProcessIds).Count -eq 0) {
            return
        }
        Start-Sleep -Milliseconds 300
    }

    $remaining = (Get-BackendListeningProcessIds) -join ", "
    throw "后端端口 $BackendPort 仍被占用，残留进程: $remaining"
}

function Stop-BackendByPort {
    $visited = New-Object 'System.Collections.Generic.HashSet[int]'
    foreach ($processId in (Get-BackendCandidateProcessIds)) {
        Stop-ProcessTree -ProcessId $processId -Visited $visited
    }
    Wait-BackendPortReleased
}

function Wait-BackendReady {
    param(
        [int]$TimeoutSeconds = 20
    )

    $scenariosUrl = "http://$BackendHost`:$BackendPort/api/dev/scenarios"
    $controlUrl = "http://$BackendHost`:$BackendPort/dev/control"
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)

    while ((Get-Date) -lt $deadline) {
        try {
            $scenarioResponse = Invoke-WebRequest -UseBasicParsing -Uri $scenariosUrl -TimeoutSec 3
            $controlResponse = Invoke-WebRequest -UseBasicParsing -Uri $controlUrl -TimeoutSec 3
            if ($scenarioResponse.StatusCode -eq 200 -and $controlResponse.Content -match 'sequence-editor') {
                return
            }
        } catch {
        }

        Start-Sleep -Milliseconds 500
    }

    throw "后端未在限定时间内通过 sequence/scenario 联调页校验：$scenariosUrl"
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

function Ensure-AgentBridgeModEnabled {
    if (-not (Test-Path $VPetSetting)) {
        return
    }

    $content = Get-Content -Raw $VPetSetting
    if ($content -match '(?im)^onmod:.*\|agentbridge:\|') {
        return
    }

    Write-Host "[STEP] 确保 Setting.lps 已启用 agentbridge mod" -ForegroundColor Yellow
    if ($content -match '(?im)^onmod:.*$') {
        $updated = [System.Text.RegularExpressions.Regex]::Replace(
            $content,
            '(?im)^onmod:.*$',
            {
                param($match)
                $line = $match.Value.TrimEnd()
                if ($line.EndsWith('|')) {
                    return "$line" + "agentbridge:|"
                }
                return "$line" + "|agentbridge:|"
            },
            1
        )
    }
    else {
        $separator = if ($content.EndsWith("`r`n") -or $content.EndsWith("`n")) { "" } else { "`r`n" }
        $updated = "$content$separator" + "onmod:|agentbridge:|`r`n"
    }

    Set-Content -LiteralPath $VPetSetting -Value $updated -Encoding UTF8NoBOM
}

function Build-VPet {
    $dotnet = Get-DotnetCommand
    Write-Host "[STEP] 编译 VPet-Simulator.Windows (Debug x64)" -ForegroundColor Yellow
    & $dotnet build $VPetProject -c Debug -p:Platform=x64
}

function Start-Backend {
    Write-Host "[STEP] 启动后端 FastAPI 服务" -ForegroundColor Yellow
    $backendCommand = @(
        "`$host.UI.RawUI.WindowTitle = '$BackendWindowTitle'"
        "`$env:PET_BACKEND_HOST='$BackendHost'"
        "`$env:PET_BACKEND_PORT='$BackendPort'"
        "`$env:PET_BACKEND_RELOAD='0'"
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
Ensure-AgentBridgeModEnabled
Start-Backend
Wait-BackendReady
Start-VPet

Write-Host ""
Write-Host "一键启动已执行：" -ForegroundColor Green
Write-Host "后端测试页: http://$BackendHost`:$BackendPort/dev/control" -ForegroundColor Cyan
Write-Host "VPet 事件桥接: http://$BackendHost`:$BackendPort/vpet/events/next" -ForegroundColor Cyan
Write-Host "编译模式: $(if ($SkipBuild) { '跳过编译' } else { '重新编译并启动' })" -ForegroundColor Cyan
Write-Host ""
Write-Host "如果后端窗口报缺依赖，请先单独运行: .\backend-agent\setup.ps1" -ForegroundColor Yellow
