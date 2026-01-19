from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form, status
from typing import List
from fastapi.responses import JSONResponse
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.document import DocumentRead
from app.services.document import DocumentService
from app.core.dependencies import get_document_svc
from app.models.document import Document

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=dict)
async def upload_document(
    name: str = Form(...),
    file: UploadFile | None = File(default=None),
    text: str | None = Form(default=None),
    db: AsyncSession = Depends(get_db),
    document_svc: DocumentService = Depends(get_document_svc),
):
    if not file and not text:
        raise HTTPException(
            status_code=400,
            detail="Either a file or raw text must be provided",
        )

    # File upload
    if file:
        filename = file.filename.lower()

        # PDF
        if filename.endswith(".pdf"):
            saved = await document_svc.save_from_pdf(
                db=db,
                name=name,
                pdf_bytes=await file.read(),
            )
            return JSONResponse(
                content={"document_id": str(saved.id)},
                status_code=status.HTTP_200_OK,
            )

        # TXT
        if file and file.filename.lower().endswith(".txt"):
            raw_text = (await file.read()).decode("utf-8")
            saved = await document_svc.save_from_text(
                db=db,
                name=name,
                text=raw_text,
            )
            return JSONResponse(
                content={"document_id": str(saved.id)},
                status_code=status.HTTP_200_OK,
            )

        raise HTTPException(
            status_code=400,
            detail="Supported formats: PDF, TXT, or raw text",
        )

    # Raw text
    if text:
        saved = await document_svc.save_from_text(
            db=db,
            name=name,
            text=text,
        )
        return JSONResponse(
            content={"document_id": str(saved.id)},
            status_code=status.HTTP_200_OK,
        )


@router.get("/", response_model=List[DocumentRead])
async def list_documents(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Document)
    )
    return result.scalars().all()

@router.delete("/{document_id}")
async def delete_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
    document_svc: DocumentService = Depends(get_document_svc),
):
    try:
        await document_svc.delete(db, document_id)
        return {
            "status": "deleted",
            "document_id": document_id,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))