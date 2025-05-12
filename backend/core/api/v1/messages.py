from fastapi import APIRouter, HTTPException, Depends
from typing import List
from services.messages_service import MessagesService
from db.models import StreamerMessage
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/messages", tags=["Messages"])

class MessageResponse(BaseModel):
    id: int
    content: str
    source: str
    timestamp: datetime

    class Config:
        orm_mode = True

@router.get("/", response_model=List[MessageResponse])
def get_messages(limit: int = 10, source: str = None):
    messages = MessagesService.get_messages(limit, source)
    return messages