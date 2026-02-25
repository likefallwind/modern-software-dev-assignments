from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from .. import db
from ..schemas import (
    ActionItemResponse,
    ExtractRequest,
    ExtractResponse,
    MarkDoneRequest,
)
from ..services.extract import extract_action_items, extract_action_items_llm

router = APIRouter(prefix="/action-items", tags=["action-items"])


@router.post("/extract", response_model=ExtractResponse, status_code=status.HTTP_201_CREATED)
def extract(payload: ExtractRequest) -> ExtractResponse:
    if not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="text is required",
        )

    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(payload.text)
        if note_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save note",
            )

    items = extract_action_items(payload.text)
    ids = db.insert_action_items(items, note_id=note_id)
    action_item_rows = db.get_action_items_by_ids(ids)

    action_items = [
        ActionItemResponse(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in action_item_rows
    ]

    return ExtractResponse(note_id=note_id, items=action_items)


@router.post("/extract-llm", response_model=ExtractResponse, status_code=status.HTTP_201_CREATED)
def extract_llm(payload: ExtractRequest) -> ExtractResponse:
    if not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="text is required",
        )

    note_id: Optional[int] = None
    if payload.save_note:
        note_id = db.insert_note(payload.text)
        if note_id is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save note",
            )

    items = extract_action_items_llm(payload.text)
    ids = db.insert_action_items(items, note_id=note_id)
    action_item_rows = db.get_action_items_by_ids(ids)

    action_items = [
        ActionItemResponse(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in action_item_rows
    ]

    return ExtractResponse(note_id=note_id, items=action_items)


@router.get("", response_model=List[ActionItemResponse])
def list_all(note_id: Optional[int] = None) -> List[ActionItemResponse]:
    rows = db.list_action_items(note_id=note_id)
    return [
        ActionItemResponse(
            id=r["id"],
            note_id=r["note_id"],
            text=r["text"],
            done=bool(r["done"]),
            created_at=r["created_at"],
        )
        for r in rows
    ]


@router.post("/{action_item_id}/done", response_model=ActionItemResponse)
def mark_done(action_item_id: int, payload: MarkDoneRequest) -> ActionItemResponse:
    db.mark_action_item_done(action_item_id, payload.done)

    rows = db.list_action_items()
    for r in rows:
        if r["id"] == action_item_id:
            return ActionItemResponse(
                id=r["id"],
                note_id=r["note_id"],
                text=r["text"],
                done=payload.done,
                created_at=r["created_at"],
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="action item not found",
    )
