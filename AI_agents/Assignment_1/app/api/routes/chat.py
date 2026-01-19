from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.chat import ChatCreate, ChatRead, ChatResponse
from app.schemas.logs import MessageCreate, MessageRead
from app.services.chat import ChatService
from app.core.dependencies import get_chat_svc
import logging

logger = logging.getLogger(__name__)

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


@router.post("/{chat_id}/messages", response_model=ChatResponse)
async def send_message(
    chat_id: UUID,
    payload: MessageCreate,
    db: AsyncSession = Depends(get_db),
    chat_svc: ChatService = Depends(get_chat_svc),
):
    try:
        message = await chat_svc.send_message(
            session=db,
            chat_id=chat_id,
            message_create=payload,
        )
        
        if not message:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to generate AI response",
            )

        return ChatResponse(
            answer=message.content,
            references=message.sources,
            confidence=message.confidence,
        )

    except ValueError as e:
        logger.warning(f"Chat validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except HTTPException:
        raise

    except Exception as e:
        # Unexpected errors (LLM, DB, vector store, etc.)
        logger.exception("Unexpected error while generating chat response")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your request",
        )


@router.get("/{chat_id}/messages", response_model=List[MessageRead])
async def get_messages(
    chat_id: UUID,
    db: AsyncSession = Depends(get_db),
    chat_svc: ChatService = Depends(get_chat_svc),
):
    return await chat_svc.find_messages(db, chat_id)
