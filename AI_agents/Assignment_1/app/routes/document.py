from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, Form, status
from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.document import DocumentRead
from app.services.document import DocumentService
from app.core.dependencies import get_document_svc
from app.models.document import Document
from app.models.api_response import StandardResponse

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=StandardResponse[dict])
async def upload_document(
    name: str = Form(...),
    file: UploadFile | None = File(default=None),
    text: str | None = Form(default=None),
    db: AsyncSession = Depends(get_db),
    document_svc: DocumentService = Depends(get_document_svc),
):
    """Upload a document to begin Q&A feature

    Args:
        name (str, optional): Name of the document.
        file (UploadFile | None, optional): Media upload class.
        text (str | None, optional): Allows to insert raw text.
        db (AsyncSession, optional): Database instance.
        document_svc (DocumentService, optional): Document service object.

    Raises:
        HTTPException: Media input validation (pdf, text, etc.)
        HTTPException: Format of media uploaded

    Returns:
        Unique Document id of uploaded document
    """
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
            
            return StandardResponse(
                status=201,
                message="PDF uploaded successfully",
                data={"document_id": str(saved.id)}
            )

        # TXT
        if file and file.filename.lower().endswith(".txt"):
            raw_text = (await file.read()).decode("utf-8")
            saved = await document_svc.save_from_text(
                db=db,
                name=name,
                text=raw_text,
            )
            
            return StandardResponse(
                status=201,
                message="Text file uploaded successfully",
                data={"document_id": str(saved.id)}
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
        
        return StandardResponse(
            status=201,
            message="Raw text inserted successfully",
            data={"document_id": str(saved.id)}
        )


@router.get("/", response_model=StandardResponse[List[DocumentRead]])
async def list_documents(
    db: AsyncSession = Depends(get_db),
):
    """List uploaded documents data

    Args:
        db (AsyncSession, optional): Database instance.

    Returns:
        A JSON array of document id and their name.
    """
    result = await db.execute(
        select(Document)
    )
    result_object=result.scalars().all()
    return StandardResponse(
        status=200,
        message="List of documents generated successfully",
        data=result_object
    )

@router.delete("/{document_id}", response_model=StandardResponse)
async def delete_document(
    document_id: UUID,
    db: AsyncSession = Depends(get_db),
    document_svc: DocumentService = Depends(get_document_svc),
):
    """Delete a specific document by id 

    Args:
        document_id (UUID): Unique document id to delete
        db (AsyncSession, optional): Database instance.
        document_svc (DocumentService, optional): Document service class.

    Raises:
        HTTPException: Document exists validation

    Returns:
        A JSON object containing confirmation message and deleted document id
    """
    try:
        await document_svc.delete(db, document_id)
        
        return StandardResponse(
            status=200,
            message="Document deleted successfully",
            data=document_id
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))