from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Sequence
from uuid import UUID
from sqlalchemy import delete
from app.models.document import Document
from app.models.chunk import Chunk

class DocumentRepository:
    async def create(
        self,
        session: AsyncSession,
        document: Document,
    ) -> Document:
        session.add(document)
        await session.commit()
        await session.refresh(document)
        return document

    async def find_all(
        self,
        session: AsyncSession,
    ) -> Sequence[Document]:
        result = await session.execute(select(Document))
        return result.scalars().all()
    
    async def get_by_id(
        self,
        session: AsyncSession,
        document_id: UUID,
    ) -> Document | None:
        result = await session.execute(
            select(Document).where(Document.id == document_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_ids(
        self,
        session: AsyncSession,
        ids: Sequence[UUID],
    ) -> list[Document]:
        if not ids:
            return []

        result = await session.execute(
            select(Document).where(Document.id.in_(list(ids)))
        )
        return result.scalars().all()
    
    async def delete_by_id(
        self,
        session: AsyncSession,
        document_id: UUID,
    ) -> bool:
        await session.execute(
            delete(Chunk).where(Chunk.document_id == document_id)
        )

        result = await session.execute(
            delete(Document).where(Document.id == document_id)
        )

        return result.rowcount > 0