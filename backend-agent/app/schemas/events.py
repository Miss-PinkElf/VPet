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


PetEvent = Union[
    BubbleShowEvent,
    EmotionSetEvent,
    MotionPlayEvent,
    ModeSwitchEvent,
    MoveIntentEvent,
]


class DevEventRequest(BaseModel):
    type: Literal['bubble.show', 'emotion.set', 'motion.play', 'mode.switch', 'move.intent']
    text: Optional[str] = Field(default=None, max_length=2000)
    duration_ms: int = Field(default=5000, ge=1000, le=20000)
    emotion: Optional[str] = Field(default=None, max_length=80)
    motion: Optional[str] = Field(default=None, max_length=80)
    expression: Optional[str] = Field(default=None, max_length=80)
    graph: Optional[str] = Field(default=None, max_length=80)
    priority: int = Field(default=50, ge=0, le=100)
    mode: Optional[str] = Field(default=None, max_length=80)
    intent: Optional[str] = Field(default=None, max_length=80)


class DevEventResponse(BaseModel):
    status: Literal['ok']
    event: PetEvent
