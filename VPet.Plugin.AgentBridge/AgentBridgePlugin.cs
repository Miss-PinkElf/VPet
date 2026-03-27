using System.Linq;
using System.Windows;
using VPet_Simulator.Windows.Interface;

namespace VPet.Plugin.AgentBridge
{
    public sealed class AgentBridgePlugin : MainPlugin
    {
        private AgentBridgePoller poller;

        public AgentBridgePlugin(IMainWindow mainwin) : base(mainwin)
        {
        }

        public override string PluginName => "AgentBridge";

        public override void GameLoaded()
        {
            if (poller != null || !ReferenceEquals(GetPrimaryMainWindow(), MW))
            {
                return;
            }

            poller = new AgentBridgePoller(MW, AgentBridgeConfig.LoadFromEnvironment());
            poller.Start();
        }

        public override void EndGame()
        {
            poller?.Dispose();
            poller = null;
        }

        private static IMainWindow GetPrimaryMainWindow()
        {
            return Application.Current?.Windows
                .OfType<Window>()
                .OfType<IMainWindow>()
                .FirstOrDefault();
        }
    }
}
