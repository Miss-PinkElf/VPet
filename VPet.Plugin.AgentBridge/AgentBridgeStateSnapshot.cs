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

        [JsonPropertyName("right")]
        public double Right { get; set; }

        [JsonPropertyName("bottom")]
        public double Bottom { get; set; }

        [JsonPropertyName("zoom_ratio")]
        public double ZoomRatio { get; set; }

        [JsonPropertyName("display_name")]
        public string DisplayName { get; set; }

        [JsonPropertyName("display_type")]
        public string DisplayType { get; set; }

        [JsonPropertyName("display_animat")]
        public string DisplayAnimat { get; set; }

        [JsonPropertyName("mode")]
        public string Mode { get; set; }

        [JsonPropertyName("working_state")]
        public string WorkingState { get; set; }

        [JsonPropertyName("work_name")]
        public string WorkName { get; set; }

        [JsonPropertyName("work_type")]
        public string WorkType { get; set; }

        [JsonPropertyName("bubble_visible")]
        public bool BubbleVisible { get; set; }

        [JsonPropertyName("last_event_type")]
        public string LastEventType { get; set; }

        [JsonPropertyName("last_event_id")]
        public string LastEventId { get; set; }

        [JsonPropertyName("last_sequence_name")]
        public string LastSequenceName { get; set; }

        [JsonPropertyName("last_step_index")]
        public int? LastStepIndex { get; set; }

        [JsonPropertyName("last_event_at")]
        public DateTimeOffset? LastEventAt { get; set; }
    }
}
