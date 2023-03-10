from typing import List, Optional
from pydantic import BaseModel

class EventHeader(BaseModel):
    UserId: str
    CameraId: int
    Created: str
    Path: str
    IsRequiredObjectDetection: bool

class EventBody(BaseModel):
    Label: str
    Left: int
    Top: int
    Right: int
    Bottom: int

class Event(BaseModel):
    EventHeader: EventHeader
    EventBodies: Optional[List[EventBody]]
