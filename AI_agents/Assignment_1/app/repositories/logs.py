from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import Sequence, Optional, List
from app.models.logs import Message, SenderType


class MessageRepository:

    async def create(
        self,
        db: AsyncSession,
        chat_id: UUID,
        content: str,
        sender_type: SenderType,
        sources: Optional[List[str]] = None,
        confidence: Optional[float] = None,
    ) -> Message:
        msg = Message(
            chat_id=chat_id,
            content=content,
            sender_type=sender_type,
            sources=sources,
            confidence=confidence
        )
        db.add(msg)
        await db.flush()
        return msg

    async def save_many(
        self,
        db: AsyncSession,
        messages: Sequence[Message],
    ):
        db.add_all(messages)
        await db.flush()

    async def find_by_chat_id(
        self,
        db: AsyncSession,
        chat_id: UUID,
    ) -> Sequence[Message]:
        result = await db.execute(
            select(Message).where(Message.chat_id == chat_id)
        )
        return result.scalars().all()
    
    async def find_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100,
    ) -> Sequence[Message]:
        result = await db.execute(
            select(Message)
            .offset(skip)
            .limit(limit)
            .order_by(Message.created_at.desc())
        )
        return result.scalars().all()
