# VPet Windows Quickstart Commands

下面的命令按顺序执行即可，覆盖从安装环境到编译运行项目的最短流程。

## 1. 安装必需环境

```powershell
# 安装 .NET 8 SDK x64，项目编译必须依赖它
winget install --id Microsoft.DotNet.SDK.8 --exact

# 如果你还没装 Git，可以执行；已安装可跳过
winget install --id Git.Git --exact

# 如果你还没装 VS Code，可以执行；已安装可跳过
winget install --id Microsoft.VisualStudioCode --exact

# 如果你还没装 PowerShell 7，可以执行；已安装可跳过
winget install --id Microsoft.PowerShell --exact
```

## 2. 检查环境是否安装成功

```powershell
# 检查 Git
git --version

# 检查 .NET SDK；输出里应能看到 8.x SDK
dotnet --info

# 检查 VS Code
code --version

# 检查 PowerShell 版本
$PSVersionTable.PSVersion
```

## 3. 进入项目目录

```powershell
# 切换到仓库根目录
Set-Location E:\Learn\Vs\Code\VPet
```

## 4. 还原依赖并编译主程序

```powershell
# 还原整个解决方案的 NuGet 依赖
dotnet restore .\VPet.sln

# 以 x64 Debug 配置编译桌面主程序
dotnet build .\VPet-Simulator.Windows\VPet-Simulator.Windows.csproj -c Debug -p:Platform=x64
```

## 5. 第一次运行前创建 mod 符号链接

```powershell
# 首次运行前执行；如果没开开发者模式，建议管理员权限运行终端
cmd /c .\VPet-Simulator.Windows\mklink.bat
```

## 6. 启动程序

```powershell
# 直接启动编译后的主程序
.\VPet-Simulator.Windows\bin\x64\Debug\net8.0-windows\VPet-Simulator.Windows.exe
```

## 7. 后续日常开发最常用命令

```powershell
# 改完代码后重新编译
dotnet build .\VPet-Simulator.Windows\VPet-Simulator.Windows.csproj -c Debug -p:Platform=x64

# 再次启动程序
.\VPet-Simulator.Windows\bin\x64\Debug\net8.0-windows\VPet-Simulator.Windows.exe
```

## 8. 常见故障时优先执行

```powershell
# 如果依赖或缓存异常，先重新还原再编译
dotnet restore .\VPet.sln
dotnet build .\VPet-Simulator.Windows\VPet-Simulator.Windows.csproj -c Debug -p:Platform=x64

# 如果启动时报缺少 Core 模组，重新执行符号链接脚本
cmd /c .\VPet-Simulator.Windows\mklink.bat
```
