from typing import Literal

from pydantic import BaseModel, Field


class MemoryRecord(BaseModel):
    category: Literal['working', 'event', 'semantic'] = 'working'
    content: str = Field(min_length=1, max_length=4000)


class MemoryRecallItem(BaseModel):
    content: str
    category: str
