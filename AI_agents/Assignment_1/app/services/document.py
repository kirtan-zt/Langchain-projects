from uuid import UUID
from typing import Sequence, List, Optional
import io
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pypdf import PdfReader
from langchain_core.documents import Document as LCDocument
from app.models.chunk import Chunk
from app.models.document import Document
from app.repositories.document import DocumentRepository

class DocumentService:
    def __init__(
        self,
        document_repository: DocumentRepository,
        vector_store,
        text_splitter,
    ):
        self.document_repository = document_repository
        self.vector_store = vector_store
        self.text_splitter = text_splitter

    async def get_by_ids(
        self,
        session: AsyncSession,
        document_ids: Sequence[UUID],
    ) -> list[Document]:
        if not document_ids:
            return []

        result = await session.execute(
            select(Document).where(Document.id.in_(document_ids))
        )
        return result.scalars().all()

    async def _save_from_text(
        self,
        db: AsyncSession,
        name: str,
        base_docs: list[LCDocument],
    ) -> Document:

        document = Document(
            name=name,
            content=b"",  
        )

        db.add(document)
        await db.flush()

        all_splits: list[LCDocument] = []
        chunks: list[Chunk] = []

        for base_doc in base_docs:
            splits = self.text_splitter.split_documents([base_doc])

            for idx, split in enumerate(splits):
                split.metadata.update(
                    {
                        "document_id": str(document.id),
                        "file_name": name,
                        "chunk_index": idx,
                        "page_number": base_doc.metadata["page_number"],
                    }
                )

                all_splits.append(split)

                chunks.append(
                    Chunk(
                        document_id=document.id,
                        chunk_index=idx,
                        content=split.page_content,
                    )
                )
        if not all_splits:
            raise ValueError("No text chunks generated")
          
        db.add_all(chunks)
        await self.vector_store.aadd_documents(all_splits)
        await db.commit()
        return document

    async def save_from_pdf(
        self,
        db: AsyncSession,
        name: str,
        pdf_bytes: bytes,
    ) -> Document:
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
        except Exception as e:
            raise ValueError("Failed to read PDF file") from e

        if reader.is_encrypted:
            try:
                reader.decrypt("")  # try empty password
            except Exception:
                raise ValueError("Encrypted PDF is not supported")
            
        base_docs: list[LCDocument] = []
        
        for page_number, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            if not text:
                continue

            base_docs.append(
            LCDocument(
                page_content=text,
                metadata={
                    "file_name": name,
                    "page_number": page_number,
                },
            )
        )

        if not base_docs:
            raise ValueError("No text could be extracted from PDF")

        return await self._save_from_text(
            db=db,
            name=name,
            base_docs=base_docs,
        )

    async def save_from_text(
        self,
        db: AsyncSession,
        name: str,
        text: str,
    ) -> Document:
        if not text.strip():
            raise ValueError("Text content is empty")
        
        base_docs = [
            LCDocument(
                page_content=text,
                metadata={
                    "file_name": name,
                    "page_number": 1,
                },
            )
        ]

        return await self._save_from_text(
            db=db,
            name=name,
            base_docs=base_docs,
        )

    async def search(
        self,
        query: str,
        file_ids: list[UUID],
        k: int = 5,
    ) -> List[LCDocument]:
        if not file_ids:
            return []

        return await self.vector_store.asimilarity_search(
            query=query,
            k=k,
            filter={
                "document_id": {"$in": [str(fid) for fid in file_ids]}
            },
        )

    async def delete(
        self,
        session: AsyncSession,
        document_id: UUID,
    ) -> None:

        # Check existence
        document = await self.document_repository.get_by_id(
            session,
            document_id,
        )
        if not document:
            raise ValueError(f"Document {document_id} not found")

        await session.delete(document)
        await session.commit()