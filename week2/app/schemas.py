from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    content: str = Field(..., min_length=1, description="Note content")


class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: str

    class Config:
        from_attributes = True


class ActionItemCreate(BaseModel):
    text: str = Field(..., min_length=1, description="Action item text")


class ActionItemResponse(BaseModel):
    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: str

    class Config:
        from_attributes = True


class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to extract action items from")
    save_note: bool = Field(default=False, description="Whether to save the note")


class ExtractResponse(BaseModel):
    note_id: Optional[int]
    items: list[ActionItemResponse]


class MarkDoneRequest(BaseModel):
    done: bool = Field(default=True, description="Mark action item as done")
