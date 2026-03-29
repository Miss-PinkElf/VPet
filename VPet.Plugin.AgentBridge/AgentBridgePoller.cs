using System;
using System.Diagnostics;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Threading;
using VPet_Simulator.Core;
using VPet_Simulator.Windows.Interface;
using static VPet_Simulator.Core.GraphInfo;

namespace VPet.Plugin.AgentBridge
{
    internal sealed class AgentBridgePoller : IDisposable
    {
        private const int DefaultBubbleMotionLeadMilliseconds = 420;
        private const double SmartMoveSmoothDistanceThreshold = 160d;
        private const int SmoothMoveMinimumSteps = 4;
        private const int SmoothMoveMaximumSteps = 10;
        private const int SmoothMoveStepDelayMilliseconds = 45;

        private static readonly JsonSerializerOptions JsonOptions = new()
        {
            PropertyNameCaseInsensitive = true
        };

        private readonly IMainWindow mainWindow;
        private readonly AgentBridgeConfig config;
        private readonly HttpClient httpClient;
        private CancellationTokenSource cancellationTokenSource;
        private Task pollingTask;
        private DateTimeOffset lastStateReportedAt = DateTimeOffset.MinValue;
        private DateTimeOffset? lastAppliedEventAt;
        private string lastAppliedEventType;
        private string lastAppliedEventId;
        private string lastAppliedSequenceName;
        private int? lastAppliedStepIndex;
        private int started;

        public AgentBridgePoller(IMainWindow mainWindow, AgentBridgeConfig config)
        {
            this.mainWindow = mainWindow ?? throw new ArgumentNullException(nameof(mainWindow));
            this.config = config ?? throw new ArgumentNullException(nameof(config));

            httpClient = new HttpClient
            {
                Timeout = TimeSpan.FromMilliseconds(config.RequestTimeoutMilliseconds)
            };
        }

        public void Start()
        {
            if (!config.Enabled || Interlocked.Exchange(ref started, 1) == 1)
            {
                return;
            }

            cancellationTokenSource = new CancellationTokenSource();
            pollingTask = Task.Run(() => PollLoopAsync(cancellationTokenSource.Token));
        }

        public void Dispose()
        {
            if (Interlocked.Exchange(ref started, 0) == 0)
            {
                httpClient.Dispose();
                return;
            }

            try
            {
                cancellationTokenSource?.Cancel();
                pollingTask?.Wait(TimeSpan.FromSeconds(1));
            }
            catch
            {
                // Ignore shutdown exceptions during bridge teardown.
            }
            finally
            {
                cancellationTokenSource?.Dispose();
                httpClient.Dispose();
            }
        }

        private async Task PollLoopAsync(CancellationToken cancellationToken)
        {
            while (!cancellationToken.IsCancellationRequested)
            {
                try
                {
                    var bridgeEvent = await FetchNextEventAsync(cancellationToken);
                    if (bridgeEvent != null)
                    {
                        await DispatchEventAsync(bridgeEvent, cancellationToken);
                        await ReportStateAsync(force: true, cancellationToken);
                    }
                    else
                    {
                        await ReportStateAsync(force: false, cancellationToken);
                    }
                }
                catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
                {
                    break;
                }
                catch (Exception ex)
                {
                    Trace.WriteLine($"[AgentBridge] Poll failed: {ex.Message}");
                }

                try
                {
                    await Task.Delay(config.PollIntervalMilliseconds, cancellationToken);
                }
                catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
                {
                    break;
                }
            }
        }

        private async Task<AgentBridgeEvent> FetchNextEventAsync(CancellationToken cancellationToken)
        {
            using var response = await httpClient.GetAsync(config.PollUrl, cancellationToken);
            if (response.StatusCode == HttpStatusCode.NoContent)
            {
                return null;
            }

            if (!response.IsSuccessStatusCode)
            {
                Trace.WriteLine($"[AgentBridge] Endpoint returned {(int)response.StatusCode} {response.StatusCode}");
                return null;
            }

            var content = await response.Content.ReadAsStringAsync(cancellationToken);
            if (string.IsNullOrWhiteSpace(content))
            {
                return null;
            }

            return JsonSerializer.Deserialize<AgentBridgeEvent>(content, JsonOptions);
        }

        private async Task DispatchEventAsync(AgentBridgeEvent bridgeEvent, CancellationToken cancellationToken)
        {
            if (bridgeEvent == null || string.IsNullOrWhiteSpace(bridgeEvent.Type))
            {
                return;
            }

            switch (bridgeEvent.Type.Trim().ToLowerInvariant())
            {
                case "bubble.show":
                    await ShowBubbleAsync(bridgeEvent, cancellationToken);
                    RememberAppliedEvent("bubble.show", bridgeEvent);
                    break;
                case "emotion.set":
                    await mainWindow.Dispatcher.InvokeAsync(() => ApplyExpressionEvent(bridgeEvent), DispatcherPriority.Normal, cancellationToken);
                    RememberAppliedEvent("emotion.set", bridgeEvent);
                    break;
                case "motion.play":
                    await mainWindow.Dispatcher.InvokeAsync(() => PlayMotion(bridgeEvent), DispatcherPriority.Normal, cancellationToken);
                    RememberAppliedEvent("motion.play", bridgeEvent);
                    break;
                case "mode.switch":
                    await mainWindow.Dispatcher.InvokeAsync(() => SwitchMode(bridgeEvent), DispatcherPriority.Normal, cancellationToken);
                    RememberAppliedEvent("mode.switch", bridgeEvent);
                    break;
                case "window.move":
                    await MoveWindowAsync(bridgeEvent, cancellationToken);
                    RememberAppliedEvent("window.move", bridgeEvent);
                    break;
                case "move.intent":
                    await mainWindow.Dispatcher.InvokeAsync(() => MoveFromIntent(bridgeEvent), DispatcherPriority.Normal, cancellationToken);
                    RememberAppliedEvent("move.intent", bridgeEvent);
                    break;
            }
        }

        private void RememberAppliedEvent(string eventType, AgentBridgeEvent bridgeEvent)
        {
            lastAppliedEventType = eventType;
            lastAppliedEventId = bridgeEvent?.EventId;
            lastAppliedSequenceName = bridgeEvent?.SequenceName;
            lastAppliedStepIndex = bridgeEvent?.StepIndex;
            lastAppliedEventAt = DateTimeOffset.UtcNow;
        }

        private async Task ShowBubbleAsync(AgentBridgeEvent bridgeEvent, CancellationToken cancellationToken)
        {
            if (string.IsNullOrWhiteSpace(bridgeEvent.Text) || mainWindow.Main == null)
            {
                return;
            }

            var graphName = ResolveGraphName(bridgeEvent);

            if (TryResolveNativeBubbleMotionGraph(bridgeEvent.Motion, out var nativeMotionGraph))
            {
                await mainWindow.Dispatcher.InvokeAsync(() =>
                {
                    if (mainWindow.Main != null)
                    {
                        mainWindow.Main.DisplayStopForce(() => mainWindow.Main.Say(bridgeEvent.Text, nativeMotionGraph, force: true));
                    }
                }, DispatcherPriority.Normal, cancellationToken);
                return;
            }

            if (!string.IsNullOrWhiteSpace(bridgeEvent.Motion))
            {
                await mainWindow.Dispatcher.InvokeAsync(() => PlayMotion(bridgeEvent), DispatcherPriority.Normal, cancellationToken);

                try
                {
                    await Task.Delay(GetBubbleMotionLeadMilliseconds(bridgeEvent.Motion), cancellationToken);
                }
                catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
                {
                    return;
                }
            }

            await mainWindow.Dispatcher.InvokeAsync(() =>
            {
                if (mainWindow.Main != null)
                {
                    mainWindow.Main.Say(bridgeEvent.Text, graphName, force: true);
                }
            }, DispatcherPriority.Normal, cancellationToken);
        }

        private void PlayMotion(AgentBridgeEvent bridgeEvent)
        {
            var motionName = string.IsNullOrWhiteSpace(bridgeEvent.Motion)
                ? bridgeEvent.Name
                : bridgeEvent.Motion;

            var motionKey = motionName?.Trim().ToLowerInvariant();
            if (string.IsNullOrWhiteSpace(motionKey) || mainWindow.Main == null)
            {
                return;
            }

            switch (motionKey)
            {
                case "pinch":
                    PlayPinch();
                    return;
                case "thinking":
                    DisplayGraphLoop("think");
                    return;
                case "idle":
                    mainWindow.Main.DisplayIdel();
                    return;
                case "move":
                    mainWindow.Main.DisplayMove();
                    return;
                case "normal":
                    mainWindow.Main.DisplayToNomal();
                    return;
                case "touch_head":
                    mainWindow.Main.DisplayTouchHead();
                    return;
                case "touch_body":
                    mainWindow.Main.DisplayTouchBody();
                    return;
                case "sleep":
                    mainWindow.Main.DisplaySleep();
                    return;
                case "raised":
                    mainWindow.Main.DisplayRaised();
                    return;
                case "state_one":
                    mainWindow.Main.DisplayIdel_StateONE?.Invoke();
                    return;
            }
        }

        private void ApplyExpressionEvent(AgentBridgeEvent bridgeEvent)
        {
            var graphName = ResolveGraphName(bridgeEvent);
            if (string.IsNullOrWhiteSpace(graphName))
            {
                return;
            }

            DisplayGraphLoop(graphName);
        }

        private void SwitchMode(AgentBridgeEvent bridgeEvent)
        {
            var modeKey = bridgeEvent.Mode?.Trim().ToLowerInvariant();
            switch (modeKey)
            {
                case "thinking":
                    DisplayGraphLoop("think");
                    break;
                case "normal":
                    mainWindow.Main?.DisplayToNomal();
                    break;
            }
        }

        private async Task MoveWindowAsync(AgentBridgeEvent bridgeEvent, CancellationToken cancellationToken)
        {
            var deltaX = bridgeEvent.Dx ?? 0d;
            var deltaY = bridgeEvent.Dy ?? 0d;
            if (Math.Abs(deltaX) < double.Epsilon && Math.Abs(deltaY) < double.Epsilon)
            {
                return;
            }

            var style = ResolveMoveStyle(bridgeEvent.Style, deltaX, deltaY);
            if (style == MoveStyle.Snap)
            {
                await mainWindow.Dispatcher.InvokeAsync(
                    () => mainWindow.Core?.Controller?.MoveWindows(deltaX, deltaY),
                    DispatcherPriority.Normal,
                    cancellationToken);
                return;
            }

            await SmoothMoveWindowAsync(deltaX, deltaY, cancellationToken);
        }

        private async Task SmoothMoveWindowAsync(double deltaX, double deltaY, CancellationToken cancellationToken)
        {
            var distance = Math.Max(Math.Abs(deltaX), Math.Abs(deltaY));
            var steps = Math.Clamp((int)Math.Ceiling(distance / 24d), SmoothMoveMinimumSteps, SmoothMoveMaximumSteps);
            var stepX = deltaX / steps;
            var stepY = deltaY / steps;
            var movedX = 0d;
            var movedY = 0d;

            for (var index = 0; index < steps; index++)
            {
                cancellationToken.ThrowIfCancellationRequested();

                var currentStepX = index == steps - 1 ? deltaX - movedX : stepX;
                var currentStepY = index == steps - 1 ? deltaY - movedY : stepY;
                movedX += currentStepX;
                movedY += currentStepY;

                await mainWindow.Dispatcher.InvokeAsync(
                    () => mainWindow.Core?.Controller?.MoveWindows(currentStepX, currentStepY),
                    DispatcherPriority.Normal,
                    cancellationToken);

                if (index < steps - 1)
                {
                    await Task.Delay(SmoothMoveStepDelayMilliseconds, cancellationToken);
                }
            }
        }

        private void MoveFromIntent(AgentBridgeEvent bridgeEvent)
        {
            var controller = mainWindow.Core?.Controller;
            var zoomRatio = controller?.ZoomRatio ?? 0d;
            if (controller == null || zoomRatio <= 0d)
            {
                return;
            }

            var intentKey = bridgeEvent.Intent?.Trim().ToLowerInvariant();
            var (deltaX, deltaY) = intentKey switch
            {
                "dock_left" => (-controller.GetWindowsDistanceLeft() / zoomRatio, 0d),
                "dock_right" => (controller.GetWindowsDistanceRight() / zoomRatio, 0d),
                "dock_top" => (0d, -controller.GetWindowsDistanceUp() / zoomRatio),
                "dock_bottom" => (0d, controller.GetWindowsDistanceDown() / zoomRatio),
                _ => (0d, 0d)
            };

            if (Math.Abs(deltaX) < double.Epsilon && Math.Abs(deltaY) < double.Epsilon)
            {
                Trace.WriteLine($"[AgentBridge] Unsupported move.intent: {bridgeEvent.Intent}");
                return;
            }

            controller.MoveWindows(deltaX, deltaY);
        }

        private MoveStyle ResolveMoveStyle(string requestedStyle, double deltaX, double deltaY)
        {
            var style = requestedStyle?.Trim().ToLowerInvariant();
            if (style == "snap" || style == "teleport")
            {
                return MoveStyle.Snap;
            }

            if (style == "smooth" || style == "walk")
            {
                return MoveStyle.Smooth;
            }

            var distance = Math.Max(Math.Abs(deltaX), Math.Abs(deltaY));
            if (distance > SmartMoveSmoothDistanceThreshold)
            {
                return MoveStyle.Snap;
            }

            return MoveStyle.Smooth;
        }

        private string ResolveGraphName(AgentBridgeEvent bridgeEvent)
        {
            if (!string.IsNullOrWhiteSpace(bridgeEvent.Graph))
            {
                return bridgeEvent.Graph.Trim();
            }

            var expressionKey = !string.IsNullOrWhiteSpace(bridgeEvent.Expression)
                ? bridgeEvent.Expression
                : bridgeEvent.Emotion;

            return expressionKey?.Trim().ToLowerInvariant() switch
            {
                "think" => "think",
                "thinking" => "think",
                "pinch" => "pinch",
                "shy" => "pinch",
                _ => null
            };
        }

        private void DisplayGraphLoop(string graphName)
        {
            if (string.IsNullOrWhiteSpace(graphName) || mainWindow.Main == null)
            {
                return;
            }

            if (mainWindow.Main.DisplayType.Name == graphName && mainWindow.Main.DisplayType.Animat != AnimatType.C_End)
            {
                return;
            }

            if (HasGraph(graphName, AnimatType.A_Start))
            {
                mainWindow.Main.Display(graphName, AnimatType.A_Start, mainWindow.Main.DisplayBLoopingForce);
                return;
            }

            if (HasGraph(graphName, AnimatType.B_Loop))
            {
                mainWindow.Main.Display(graphName, AnimatType.B_Loop, mainWindow.Main.DisplayBLoopingForce);
                return;
            }

            if (HasGraph(graphName, AnimatType.Single))
            {
                mainWindow.Main.Display(graphName, AnimatType.Single, mainWindow.Main.DisplayToNomal);
            }
        }

        private void PlayPinch()
        {
            if (!HasGraph("pinch", AnimatType.A_Start) || mainWindow.Main == null)
            {
                return;
            }

            mainWindow.Main.Display("pinch", AnimatType.A_Start, () =>
                mainWindow.Main.Display("pinch", AnimatType.B_Loop, () => mainWindow.Main.DisplayCEndtoNomal("pinch")));
        }

        private bool HasGraph(string graphName, AnimatType animatType)
        {
            return (mainWindow.Core?.Graph?.FindGraphs(graphName, animatType, mainWindow.Core.Save.Mode)?.Count ?? 0) > 0;
        }

        private bool TryResolveNativeBubbleMotionGraph(string motionName, out string graphName)
        {
            graphName = motionName?.Trim().ToLowerInvariant() switch
            {
                "touch_head" => mainWindow.Core?.Graph?.FindName(GraphType.Touch_Head),
                "touch_body" => mainWindow.Core?.Graph?.FindName(GraphType.Touch_Body),
                "pinch" => "pinch",
                "thinking" => "think",
                _ => null
            };

            return !string.IsNullOrWhiteSpace(graphName) && HasGraph(graphName, AnimatType.A_Start);
        }

        private static int GetBubbleMotionLeadMilliseconds(string motionName)
        {
            return motionName?.Trim().ToLowerInvariant() switch
            {
                "touch_head" => 480,
                "touch_body" => 480,
                "pinch" => 520,
                "thinking" => 280,
                _ => DefaultBubbleMotionLeadMilliseconds
            };
        }

        private async Task ReportStateAsync(bool force, CancellationToken cancellationToken)
        {
            if (string.IsNullOrWhiteSpace(config.StateReportUrl))
            {
                return;
            }

            var now = DateTimeOffset.UtcNow;
            if (!force && now - lastStateReportedAt < TimeSpan.FromMilliseconds(config.StateReportIntervalMilliseconds))
            {
                return;
            }

            AgentBridgeStateSnapshot snapshot;
            try
            {
                snapshot = await mainWindow.Dispatcher.InvokeAsync(
                    CaptureStateSnapshot,
                    DispatcherPriority.Background,
                    cancellationToken);
            }
            catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
            {
                return;
            }

            if (snapshot == null)
            {
                return;
            }

            var content = new StringContent(JsonSerializer.Serialize(snapshot, JsonOptions), Encoding.UTF8, "application/json");

            try
            {
                using var response = await httpClient.PostAsync(config.StateReportUrl, content, cancellationToken);
                if (response.IsSuccessStatusCode)
                {
                    lastStateReportedAt = now;
                    return;
                }

                Trace.WriteLine($"[AgentBridge] State report failed: {(int)response.StatusCode} {response.StatusCode}");
            }
            catch (OperationCanceledException) when (cancellationToken.IsCancellationRequested)
            {
            }
            catch (Exception ex)
            {
                Trace.WriteLine($"[AgentBridge] State report failed: {ex.Message}");
            }
        }

        private AgentBridgeStateSnapshot CaptureStateSnapshot()
        {
            var controller = mainWindow.Core?.Controller;
            var zoomRatio = controller?.ZoomRatio ?? 1d;
            var left = controller?.GetWindowsDistanceLeft() ?? 0d;
            var top = controller?.GetWindowsDistanceUp() ?? 0d;
            var right = controller?.GetWindowsDistanceRight() ?? 0d;
            var bottom = controller?.GetWindowsDistanceDown() ?? 0d;
            var displayType = mainWindow.Main?.DisplayType;

            return new AgentBridgeStateSnapshot
            {
                Timestamp = DateTimeOffset.UtcNow,
                Left = zoomRatio > 0d ? left / zoomRatio : left,
                Top = zoomRatio > 0d ? top / zoomRatio : top,
                Right = zoomRatio > 0d ? right / zoomRatio : right,
                Bottom = zoomRatio > 0d ? bottom / zoomRatio : bottom,
                ZoomRatio = zoomRatio,
                DisplayName = displayType?.Name,
                DisplayType = displayType?.Type.ToString(),
                DisplayAnimat = displayType?.Animat.ToString(),
                Mode = mainWindow.Core?.Save?.Mode.ToString(),
                WorkingState = mainWindow.Main?.State.ToString(),
                WorkName = mainWindow.Main?.NowWork?.Name,
                WorkType = mainWindow.Main?.NowWork?.Type.ToString(),
                BubbleVisible = mainWindow.Main?.MsgBar?.Visibility == System.Windows.Visibility.Visible,
                LastEventType = lastAppliedEventType,
                LastEventId = lastAppliedEventId,
                LastSequenceName = lastAppliedSequenceName,
                LastStepIndex = lastAppliedStepIndex,
                LastEventAt = lastAppliedEventAt
            };
        }

        private enum MoveStyle
        {
            Smooth,
            Snap
        }
    }
}
