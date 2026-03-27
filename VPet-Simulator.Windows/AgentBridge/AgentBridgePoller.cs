using System;
using System.Diagnostics;
using System.Net;
using System.Net.Http;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Threading;

namespace VPet_Simulator.Windows.AgentBridge
{
    internal sealed class AgentBridgePoller : IDisposable
    {
        private static readonly JsonSerializerOptions JsonOptions = new()
        {
            PropertyNameCaseInsensitive = true
        };

        private readonly MainWindow mainWindow;
        private readonly AgentBridgeConfig config;
        private readonly HttpClient httpClient;
        private CancellationTokenSource cancellationTokenSource;
        private Task pollingTask;
        private int started;

        public AgentBridgePoller(MainWindow mainWindow, AgentBridgeConfig config)
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
                // Ignore shutdown exceptions for the temporary POC bridge.
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

            await mainWindow.Dispatcher.InvokeAsync(() =>
            {
                switch (bridgeEvent.Type.Trim().ToLowerInvariant())
                {
                    case "bubble.show":
                        ShowBubble(bridgeEvent);
                        break;
                    case "emotion.set":
                        ApplyExpressionEvent(bridgeEvent);
                        break;
                    case "motion.play":
                        PlayMotion(bridgeEvent);
                        break;
                    case "mode.switch":
                        SwitchMode(bridgeEvent);
                        break;
                }
            }, DispatcherPriority.Normal, cancellationToken);
        }

        private void ShowBubble(AgentBridgeEvent bridgeEvent)
        {
            if (string.IsNullOrWhiteSpace(bridgeEvent.Text) || mainWindow.Main == null)
            {
                return;
            }

            if (!string.IsNullOrWhiteSpace(bridgeEvent.Motion))
            {
                PlayMotion(bridgeEvent);
            }

            var graphName = ResolveGraphName(bridgeEvent);
            mainWindow.Main.Say(bridgeEvent.Text, graphName, force: true);
        }

        private void PlayMotion(AgentBridgeEvent bridgeEvent)
        {
            var motionName = string.IsNullOrWhiteSpace(bridgeEvent.Motion)
                ? bridgeEvent.Name
                : bridgeEvent.Motion;

            var motionKey = motionName?.Trim().ToLowerInvariant();
            if (string.IsNullOrWhiteSpace(motionKey))
            {
                return;
            }

            switch (motionKey)
            {
                case "pinch":
                    mainWindow.DisplayPinch();
                    return;
                case "thinking":
                    DisplayGraphLoop("think");
                    return;
            }

            var action = motionKey switch
            {
                "idle" => "DisplayIdel",
                "move" => "DisplayMove",
                "normal" => "DisplayToNomal",
                "touch_head" => "DisplayTouchHead",
                "touch_body" => "DisplayTouchBody",
                "sleep" => "DisplaySleep",
                "raised" => "DisplayRaised",
                "state_one" => "DisplayIdel_StateONE",
                _ => null
            };

            if (action == null)
            {
                return;
            }

            mainWindow.RunAction(action);
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
                    mainWindow.RunAction("DisplayToNomal");
                    break;
            }
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
                // Inference: VPet lacks a verified built-in "shy" graph name in source hooks,
                // so the first bridge iteration approximates shy with the pinch face expression.
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

            if (mainWindow.Main.DisplayType.Name == graphName && mainWindow.Main.DisplayType.Animat != Core.GraphInfo.AnimatType.C_End)
            {
                return;
            }

            if (HasGraph(graphName, Core.GraphInfo.AnimatType.A_Start))
            {
                mainWindow.Main.Display(graphName, Core.GraphInfo.AnimatType.A_Start, mainWindow.Main.DisplayBLoopingForce);
                return;
            }

            if (HasGraph(graphName, Core.GraphInfo.AnimatType.B_Loop))
            {
                mainWindow.Main.Display(graphName, Core.GraphInfo.AnimatType.B_Loop, mainWindow.Main.DisplayBLoopingForce);
                return;
            }

            if (HasGraph(graphName, Core.GraphInfo.AnimatType.Single))
            {
                mainWindow.Main.Display(graphName, Core.GraphInfo.AnimatType.Single, mainWindow.Main.DisplayToNomal);
            }
        }

        private bool HasGraph(string graphName, Core.GraphInfo.AnimatType animatType)
        {
            return (mainWindow.Core?.Graph?.FindGraphs(graphName, animatType, mainWindow.Core.Save.Mode)?.Count ?? 0) > 0;
        }
    }
}
