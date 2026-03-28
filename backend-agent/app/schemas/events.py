from datetime import datetime, timezone
from typing import Literal, Optional, Union

from pydantic import BaseModel, Field


class BasePetEvent(BaseModel):
    source: str = Field(default='backend')


class BubbleShowEvent(BasePetEvent):
    type: Literal['bubble.show'] = 'bubble.show'
    text: str = Field(min_length=1, max_length=2000)
    duration_ms: int = Field(default=5000, ge=1000, le=20000)
    motion: Optional[str] = Field(default=None, max_length=80)
    expression: Optional[str] = Field(default=None, max_length=80)
    graph: Optional[str] = Field(default=None, max_length=80)


class EmotionSetEvent(BasePetEvent):
    type: Literal['emotion.set'] = 'emotion.set'
    emotion: str = Field(min_length=1, max_length=80)
    graph: Optional[str] = Field(default=None, max_length=80)


class MotionPlayEvent(BasePetEvent):
    type: Literal['motion.play'] = 'motion.play'
    motion: str = Field(min_length=1, max_length=80)
    priority: int = Field(default=50, ge=0, le=100)


class ModeSwitchEvent(BasePetEvent):
    type: Literal['mode.switch'] = 'mode.switch'
    mode: str = Field(min_length=1, max_length=80)


class MoveIntentEvent(BasePetEvent):
    type: Literal['move.intent'] = 'move.intent'
    intent: str = Field(min_length=1, max_length=80)


class WindowMoveEvent(BasePetEvent):
    type: Literal['window.move'] = 'window.move'
    dx: float = Field(default=0)
    dy: float = Field(default=0)
    style: Optional[str] = Field(default=None, max_length=40)


PetEvent = Union[
    BubbleShowEvent,
    EmotionSetEvent,
    MotionPlayEvent,
    ModeSwitchEvent,
    MoveIntentEvent,
    WindowMoveEvent,
]


class DevEventRequest(BaseModel):
    type: Literal['bubble.show', 'emotion.set', 'motion.play', 'mode.switch', 'move.intent', 'window.move']
    text: Optional[str] = Field(default=None, max_length=2000)
    duration_ms: int = Field(default=5000, ge=1000, le=20000)
    emotion: Optional[str] = Field(default=None, max_length=80)
    motion: Optional[str] = Field(default=None, max_length=80)
    expression: Optional[str] = Field(default=None, max_length=80)
    graph: Optional[str] = Field(default=None, max_length=80)
    priority: int = Field(default=50, ge=0, le=100)
    mode: Optional[str] = Field(default=None, max_length=80)
    intent: Optional[str] = Field(default=None, max_length=80)
    dx: float = Field(default=0)
    dy: float = Field(default=0)
    style: Optional[str] = Field(default=None, max_length=40)


class DevEventResponse(BaseModel):
    status: Literal['ok']
    event: PetEvent


class DevSequenceStepRequest(BaseModel):
    delay_ms: int = Field(default=0, ge=0, le=20000)
    event: DevEventRequest
    wait_for: Optional[Literal['event_applied', 'move_complete', 'motion_complete']] = None
    wait_timeout_ms: int = Field(default=6000, ge=200, le=30000)
    settle_ms: int = Field(default=0, ge=0, le=5000)


class DevSequenceRequest(BaseModel):
    name: Optional[str] = Field(default=None, max_length=120)
    source: str = Field(default='dev-sequence', max_length=120)
    steps: list[DevSequenceStepRequest] = Field(min_length=1, max_length=20)


class DevSequenceDispatchResponse(BaseModel):
    status: Literal['accepted']
    sequence_name: str
    step_count: int = Field(ge=1)
    source: str = Field(max_length=120)


class DevScenarioSummary(BaseModel):
    scenario_id: str = Field(min_length=1, max_length=120)
    title: str = Field(min_length=1, max_length=120)
    description: str = Field(min_length=1, max_length=240)
    step_count: int = Field(ge=1)


class DevScenarioListResponse(BaseModel):
    status: Literal['ok']
    scenarios: list[DevScenarioSummary]


class VPetStateSnapshot(BaseModel):
    source: str = Field(default='vpet-plugin')
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    left: float
    top: float
    right: float = Field(default=0)
    bottom: float = Field(default=0)
    zoom_ratio: float = Field(gt=0)
    display_name: Optional[str] = Field(default=None, max_length=120)
    display_type: Optional[str] = Field(default=None, max_length=120)
    display_animat: Optional[str] = Field(default=None, max_length=120)
    mode: Optional[str] = Field(default=None, max_length=80)
    working_state: Optional[str] = Field(default=None, max_length=80)
    work_name: Optional[str] = Field(default=None, max_length=120)
    work_type: Optional[str] = Field(default=None, max_length=80)
    bubble_visible: bool = False
    last_event_type: Optional[str] = Field(default=None, max_length=80)
    last_event_at: Optional[datetime] = None


class VPetStateResponse(BaseModel):
    status: Literal['ok']
    state: Optional[VPetStateSnapshot] = None
