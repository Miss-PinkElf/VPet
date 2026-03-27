using System;
using System.Text.Json.Serialization;

namespace VPet.Plugin.AgentBridge
{
    internal sealed class AgentBridgeStateSnapshot
    {
        [JsonPropertyName("source")]
        public string Source { get; set; } = "vpet-plugin";

        [JsonPropertyName("timestamp")]
        public DateTimeOffset Timestamp { get; set; } = DateTimeOffset.UtcNow;

        [JsonPropertyName("left")]
        public double Left { get; set; }

        [JsonPropertyName("top")]
        public double Top { get; set; }

        [JsonPropertyName("zoom_ratio")]
        public double ZoomRatio { get; set; }

        [JsonPropertyName("display_name")]
        public string DisplayName { get; set; }

        [JsonPropertyName("display_type")]
        public string DisplayType { get; set; }

        [JsonPropertyName("mode")]
        public string Mode { get; set; }

        [JsonPropertyName("last_event_type")]
        public string LastEventType { get; set; }
    }
}
