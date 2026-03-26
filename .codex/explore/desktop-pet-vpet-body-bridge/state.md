# 当前状态

## 当前阶段
阶段 1：桥接协议和实现顺序冻结

## 已确认的事实
- 动作入口首选 `MainWindow.RunAction(string action)`。
- 说话入口首选 `Main.Say(...)`。
- 窗口控制入口首选 `MW.Core.Controller.MoveWindows(...)`。
- 长期实现应优先挂在 `MainPlugin` 生命周期中。

## 当前推荐事件
- `bubble.show`
- `motion.play`
- `mode.switch`
- `window.move`

## 下一步
- 让 AI 直接开始写第一版桥接 POC。
- 第一版只做 `say / idle / move`。

## 最小活跃上下文摘要
专项目标不是解耦整个 VPet，而是先把外部事件桥做通。
