from dataclasses import dataclass
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.chat import ChatCreate
from app.models.chat import Chat
from app.models.logs import Message
from app.repositories.chat import ChatRepository
from app.repositories.document import DocumentRepository
from app.repositories.logs import MessageRepository
from app.services.ai import AIService
from app.services.document import DocumentService
from app.schemas.logs import MessageCreate
from app.models.logs import SenderType

@dataclass
class ChatService:
    """Business logic for chat model"""
    chat_repository: ChatRepository
    message_repository: MessageRepository
    ai_svc: AIService
    document_svc: DocumentService

    async def create_chat(
    self,
    session: AsyncSession,
    chat_create: ChatCreate,
) -> Chat:
        """Method to create chat id

        Args:
            session (AsyncSession): Database instance
            chat_create (ChatCreate): Request model to store chat id

        Returns:
            Chat: Dictionary that maps to Chat database 
        """
        documents = []

        if chat_create.document_ids:
            documents = await self.document_svc.get_by_ids(
            session,
            chat_create.document_ids,
            )

        chat = Chat(name="New Chat")
        return await self.chat_repository.create(
        db=session,
        chat=chat,
        documents=documents,
        )

    async def find_all_chats(
        self,
        session: AsyncSession,
    ) -> list[Chat]:
        """Lists all chat ids from the database.

        Args:
            session (AsyncSession): Database instance.

        Returns:
            list[Chat]: A JSON array of chat objects
        """
        return await self.chat_repository.find_all(session)

    async def send_message(
        self,
        session: AsyncSession,
        chat_id: UUID,
        message_create: MessageCreate,
    ) -> Message:
        """Method to send prompt to LLM from the user.

        Args:
            session (AsyncSession): Database instance.
            chat_id (UUID): Unique chat id
            message_create (MessageCreate): Request model object

        Raises:
            ValueError: Chat id validation check

        Returns:
            Message: LLM response for the given question
        """
        
        chat = await self.chat_repository.get_by_id(session, chat_id)
        if chat is None:
            raise ValueError(f"Chat {chat_id} not found")
        
        # Save user message
        user_msg = Message(
            chat_id=chat_id,
            content=message_create.content,
            sender_type=SenderType.HUMAN,
        )
        session.add(user_msg)

        # Retrieve context from documents
        context_docs = await self.document_svc.search(
            query=message_create.content,
            file_ids=[doc.id for doc in chat.files],
        )

        # Generate AI response
        rag_result = await self.ai_svc.generate_rag_answer(
            question=message_create.content,
            documents=context_docs,
        )

        # Save AI message
        ai_msg = Message(
            chat_id=chat_id,
            sender_type=SenderType.AI,
            content=rag_result.answer,
            sources=rag_result.sources,
            confidence=rag_result.confidence,
        )
        session.add(ai_msg)
        await session.commit()
        await session.refresh(ai_msg)

        return ai_msg
    
    async def find_messages(
        self,
        session: AsyncSession,
        chat_id: UUID,
    ) -> list[Message]:
        """Lists all messages in the conversation.

        Args:
            session (AsyncSession): Database instance.
            chat_id (UUID): Unique chat id

        Returns:
            list[Message]: A JSON array of message objects.
        """
        return await self.message_repository.find_by_chat_id(session, chat_id)