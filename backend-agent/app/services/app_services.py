from dataclasses import dataclass

from ..core.config import Settings
from ..memory.in_memory import InMemoryStore
from .behavior_policy_engine import BehaviorPolicyEngine
from .chat_orchestrator import ChatOrchestrator
from .dev_sequence_orchestrator import DevSequenceOrchestrator
from .event_bus import EventBus
from .llm_service import LlmService
from .memory_service import MemoryService
from .vpet_state_store import VPetStateStore


@dataclass
class AppServices:
    settings: Settings
    event_bus: EventBus
    memory_service: MemoryService
    llm_service: LlmService
    behavior_policy_engine: BehaviorPolicyEngine
    dev_sequence_orchestrator: DevSequenceOrchestrator
    chat_orchestrator: ChatOrchestrator
    vpet_state_store: VPetStateStore


def create_app_services(settings: Settings) -> AppServices:
    event_bus = EventBus()
    memory_service = MemoryService(store=InMemoryStore())
    llm_service = LlmService(settings)
    behavior_policy_engine = BehaviorPolicyEngine()
    dev_sequence_orchestrator = DevSequenceOrchestrator(
        event_bus=event_bus,
        behavior_policy_engine=behavior_policy_engine,
    )
    vpet_state_store = VPetStateStore()
    chat_orchestrator = ChatOrchestrator(
        settings=settings,
        llm_service=llm_service,
        memory_service=memory_service,
    )
    return AppServices(
        settings=settings,
        event_bus=event_bus,
        memory_service=memory_service,
        llm_service=llm_service,
        behavior_policy_engine=behavior_policy_engine,
        dev_sequence_orchestrator=dev_sequence_orchestrator,
        chat_orchestrator=chat_orchestrator,
        vpet_state_store=vpet_state_store,
    )
