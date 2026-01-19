from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import Sequence
from sqlalchemy.orm import selectinload

from app.models.chat import Chat
from app.models.document import Document


class ChatRepository:

    async def create(
        self,
        db: AsyncSession,
        chat: Chat,
        documents: Sequence[Document],
    ) -> Chat:
        chat.files = list(documents)
        db.add(chat)
        await db.flush()
        await db.commit() 
        await db.refresh(chat)
        return chat

    async def find_all(self, db: AsyncSession) -> Sequence[Chat]:
        result = await db.execute(select(Chat))
        return result.scalars().all()

    async def get_by_id(self, db: AsyncSession, chat_id: UUID) -> Chat | None:
        result = await db.execute(
            select(Chat)
            .options(selectinload(Chat.files))  
            .where(Chat.id == chat_id)
        )
        return result.scalar_one_or_none()
