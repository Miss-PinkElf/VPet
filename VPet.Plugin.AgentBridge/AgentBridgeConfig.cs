using System;

namespace VPet.Plugin.AgentBridge
{
    internal sealed class AgentBridgeConfig
    {
        private const string DefaultPollUrl = "http://127.0.0.1:18787/vpet/events/next";
        private const int DefaultPollIntervalMilliseconds = 1000;
        private const int DefaultRequestTimeoutMilliseconds = 3000;

        public bool Enabled { get; init; } = true;

        public string PollUrl { get; init; } = DefaultPollUrl;

        public int PollIntervalMilliseconds { get; init; } = DefaultPollIntervalMilliseconds;

        public int RequestTimeoutMilliseconds { get; init; } = DefaultRequestTimeoutMilliseconds;

        public static AgentBridgeConfig LoadFromEnvironment()
        {
            return new AgentBridgeConfig
            {
                Enabled = ReadBool("VPET_AGENT_BRIDGE_ENABLED", true),
                PollUrl = ReadString("VPET_AGENT_BRIDGE_URL", DefaultPollUrl),
                PollIntervalMilliseconds = ReadInt("VPET_AGENT_BRIDGE_INTERVAL_MS", DefaultPollIntervalMilliseconds),
                RequestTimeoutMilliseconds = ReadInt("VPET_AGENT_BRIDGE_TIMEOUT_MS", DefaultRequestTimeoutMilliseconds)
            };
        }

        private static bool ReadBool(string name, bool fallback)
        {
            var value = Environment.GetEnvironmentVariable(name);
            if (string.IsNullOrWhiteSpace(value))
            {
                return fallback;
            }

            if (bool.TryParse(value, out var result))
            {
                return result;
            }

            return value.Trim() switch
            {
                "1" => true,
                "0" => false,
                _ => fallback
            };
        }

        private static int ReadInt(string name, int fallback)
        {
            var value = Environment.GetEnvironmentVariable(name);
            if (int.TryParse(value, out var result) && result > 0)
            {
                return result;
            }

            return fallback;
        }

        private static string ReadString(string name, string fallback)
        {
            var value = Environment.GetEnvironmentVariable(name);
            return string.IsNullOrWhiteSpace(value) ? fallback : value.Trim();
        }
    }
}
