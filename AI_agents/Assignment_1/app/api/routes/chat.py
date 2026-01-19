from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.chat import ChatCreate, ChatRead
from app.schemas.logs import MessageCreate, MessageRead
from app.services.chat import ChatService
from app.core.dependencies import get_chat_svc

router = APIRouter(prefix="/chats", tags=["chats"])


@router.post("/", response_model=ChatRead)
async def create_chat(
    chat_create: ChatCreate,
    db: AsyncSession = Depends(get_db),
    chat_svc: ChatService = Depends(get_chat_svc),
):
    chat = await chat_svc.create_chat(db, chat_create)
    return chat


@router.get("/", response_model=List[ChatRead])
async def get_chats(
    db: AsyncSession = Depends(get_db),
    chat_svc: ChatService = Depends(get_chat_svc),
):
    return await chat_svc.find_all_chats(db)


@router.post("/{chat_id}/messages", response_model=MessageRead)
async def send_message(
    chat_id: UUID,
    message_create: MessageCreate,
    db: AsyncSession = Depends(get_db),
    chat_svc: ChatService = Depends(get_chat_svc),
):
    try:
        return await chat_svc.send_message(db, chat_id, message_create)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{chat_id}/messages", response_model=List[MessageRead])
async def get_messages(
    chat_id: UUID,
    db: AsyncSession = Depends(get_db),
    chat_svc: ChatService = Depends(get_chat_svc),
):
    return await chat_svc.find_messages(db, chat_id)
