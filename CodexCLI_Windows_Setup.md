# VPet 仓库的 Codex CLI Windows 环境安装指南

本文档面向以下使用方式：

- 在 Windows 上开发
- 使用 VS Code 和 Codex CLI
- 不打算深入阅读 C# 代码
- 主要由 AI 改代码，你负责运行、看结果、反馈报错

这套方案的目标不是把本机配成完整的 Visual Studio 桌面开发环境，而是配成一个足够让 Codex CLI 持续修改、编译、运行、验证这个仓库的最小环境。

## 1. 先说结论

这个仓库不是只装 `.NET Runtime` 就够了，至少要安装 `.NET 8 SDK`。

原因：

- `Runtime` 只能运行程序，不能执行 `dotnet restore`、`dotnet build`
- Codex CLI 改完代码后，必须能在本机立即编译验证
- 本仓库主项目是 `net8.0-windows` 的 WPF 桌面程序

仓库里的主项目配置可以直接看到这些信息：

- `VPet-Simulator.Windows` 目标框架是 `net8.0-windows`
- 启用了 `UseWPF`
- 启用了 `UseWindowsForms`
- 主要开发平台是 `x64`

## 2. 最小安装清单

建议至少安装以下内容：

1. `.NET 8 SDK x64`
2. `Git for Windows`
3. `Visual Studio Code`
4. `PowerShell 7`
5. Windows 开发者模式，或者管理员权限

说明：

- `.NET 8 SDK` 是必须项
- `Git` 用来管理仓库和让 Codex CLI 在本地协作
- `VS Code` 主要用于查看文件、终端和扩展
- `PowerShell 7` 不是绝对必须，但脚本体验更稳定
- 这个仓库使用 `mklink` 创建符号链接，如果不开启开发者模式，通常需要管理员权限

## 3. 推荐安装方式

如果你已经安装了 `winget`，建议直接用下面的命令。

在管理员 PowerShell 中执行：

```powershell
winget install --id Microsoft.DotNet.SDK.8 --exact
winget install --id Git.Git --exact
winget install --id Microsoft.VisualStudioCode --exact
winget install --id Microsoft.PowerShell --exact
```

如果你不想用 `winget`，也可以分别从官网安装：

- `.NET 8 SDK`
- `Git for Windows`
- `Visual Studio Code`
- `PowerShell 7`

安装完成后，关闭并重新打开终端。

## 4. VS Code 建议扩展

最少建议安装这些扩展：

1. `C#`
2. `C# Dev Kit`
3. `PowerShell`

说明：

- 你不需要精通 C#，但这些扩展能让项目加载、跳转、报错提示更正常
- `C# Dev Kit` 对解决方案和项目识别更友好
- `PowerShell` 扩展便于执行脚本

## 5. 打开 Windows 开发者模式

为了减少 `mklink` 带来的权限问题，建议开启 Windows 开发者模式。

路径通常是：

`设置 -> 系统 -> 开发者选项 -> 开发人员模式`

如果你不想开启，也可以在需要时用“管理员身份运行 PowerShell / CMD”。

## 6. 安装后自检

重新打开终端后，执行下面的命令检查环境：

```powershell
git --version
dotnet --info
code --version
$PSVersionTable.PSVersion
```

如果 `dotnet --info` 报错，说明 `.NET 8 SDK` 还没有正确安装，或者没有进 `PATH`。

## 7. 仓库相关说明

这个仓库的桌面主程序是：

- `VPet-Simulator.Windows/VPet-Simulator.Windows.csproj`

项目特征：

- WPF 桌面应用
- 目标框架：`.NET 8`
- 平台：`x64` 和 `x86`
- 实际开发时建议优先使用 `x64`

仓库原本的文档主要按 Visual Studio 使用方式编写，但命令行开发也是可以做的。

## 8. 第一次构建

在仓库根目录执行：

```powershell
dotnet restore .\VPet.sln
dotnet build .\VPet-Simulator.Windows\VPet-Simulator.Windows.csproj -c Debug -p:Platform=x64
```

说明：

- `restore` 会下载 NuGet 依赖
- `build` 会编译桌面主程序
- 如果这是第一次执行，可能需要等待一会

如果 `restore` 失败，先检查：

1. 网络是否可用
2. `dotnet --info` 是否正常
3. 是否被代理、公司网络或防火墙拦截

## 9. 第一次运行前必须做的事

这个仓库运行时依赖 `mod` 目录的符号链接。

仓库已经自带了脚本：

- `VPet-Simulator.Windows/mklink.bat`

第一次运行前，建议执行：

```powershell
cmd /c .\VPet-Simulator.Windows\mklink.bat
```

注意：

- 如果没有开启开发者模式，最好用管理员身份运行终端
- 脚本里有一些指向外部插件仓库的链接命令，报错并不一定影响主程序启动
- 最重要的是把主程序输出目录里的 `mod` 链接到仓库内的 `mod`

## 10. 启动程序

构建完成后，可直接运行：

```powershell
.\VPet-Simulator.Windows\bin\x64\Debug\net8.0-windows\VPet-Simulator.Windows.exe
```

也可以用：

```powershell
Start-Process .\VPet-Simulator.Windows\bin\x64\Debug\net8.0-windows\VPet-Simulator.Windows.exe
```

如果程序启动时报“缺少模组 Core”之类的错误，优先检查 `mklink.bat` 是否已经成功执行。

## 11. 适合你的工作流

如果你打算让 AI 主要负责写代码，你只负责运行和反馈，建议固定使用下面的流程：

1. 告诉 AI 你要改什么
2. 让 AI 直接修改仓库
3. 在本机运行构建命令
4. 启动程序验证效果
5. 把报错文本、截图、现象反馈给 AI

这种方式下，你不需要读懂大部分 C# 代码，但你需要提供高质量反馈。

## 12. 你最需要反馈给 AI 的内容

每次验证后，尽量反馈以下信息：

1. 你执行了哪个命令
2. 完整报错文本
3. 预期行为是什么
4. 实际行为是什么
5. 有没有截图或录屏

例如：

```text
我执行了：
dotnet build .\VPet-Simulator.Windows\VPet-Simulator.Windows.csproj -c Debug -p:Platform=x64

报错是：
xxx

我的预期是：
点击设置按钮后弹出设置窗口

实际结果是：
按钮无反应
```

这种反馈比“不能用”“报错了”有效很多。

## 13. 常见问题

### Q1: 我能不能只装 Runtime？

不能。

你要让 Codex CLI 修改后立即本地编译验证，必须安装 `.NET 8 SDK`。

### Q2: 我一定要装 Visual Studio 吗？

不一定。

如果你主要采用“AI 写代码 + 你本地验证”的方式，`VS Code + .NET 8 SDK` 就够用了。

### Q3: 为什么要管理员权限？

因为仓库使用了 `mklink` 创建符号链接。不开启 Windows 开发者模式时，通常需要管理员权限。

### Q4: 为什么优先用 x64？

仓库原文档就是按 `x64` 启动主程序写的，而且主项目也明确区分了 `x64/x86`。实际本地开发时，优先统一用 `x64` 更省事。

## 14. 最小命令清单

以后你最常用的命令，通常就是这些：

```powershell
dotnet restore .\VPet.sln
dotnet build .\VPet-Simulator.Windows\VPet-Simulator.Windows.csproj -c Debug -p:Platform=x64
cmd /c .\VPet-Simulator.Windows\mklink.bat
.\VPet-Simulator.Windows\bin\x64\Debug\net8.0-windows\VPet-Simulator.Windows.exe
```

## 15. 下一步建议

把环境装好后，下一步最值得做的是补两个脚本：

1. `dev-build.ps1`
2. `dev-run.ps1`

这样以后你只需要执行脚本，把结果发给 AI，就能持续迭代。

如果需要，我可以继续直接帮你把这两个脚本也加到仓库里。
