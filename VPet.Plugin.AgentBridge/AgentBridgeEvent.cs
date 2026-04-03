using System.Text.Json.Serialization;

namespace VPet.Plugin.AgentBridge
{
    internal sealed class AgentBridgeEvent
    {
        public string Type { get; set; }

        public string Text { get; set; }

        public string Name { get; set; }

        public string Motion { get; set; }

        public string Expression { get; set; }

        public string Emotion { get; set; }

        public string Graph { get; set; }

        public string Mode { get; set; }

        [JsonPropertyName("event_id")]
        public string EventId { get; set; }

        [JsonPropertyName("sequence_name")]
        public string SequenceName { get; set; }

        [JsonPropertyName("step_index")]
        public int? StepIndex { get; set; }

        public string Style { get; set; }

        public string Intent { get; set; }

        public string Direction { get; set; }

        public double? Dx { get; set; }

        public double? Dy { get; set; }
    }
}
