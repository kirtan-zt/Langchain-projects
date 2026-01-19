from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_message_repo
from app.core.db import get_db
from app.schemas.logs import MessageRead
from app.repositories.logs import MessageRepository

router = APIRouter(prefix="/logs", tags=["logs"])

message_repo = MessageRepository()

@router.get("/", response_model=List[MessageRead])
async def read_logs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    message_repo: MessageRepository = Depends(get_message_repo),
):
    messages = await message_repo.find_all(db, skip=skip, limit=limit)
    return messages