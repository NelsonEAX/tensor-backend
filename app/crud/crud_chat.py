import uuid

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud_base import CRUDBase
from app.models.models import Message, UserChats, Chat
from app.shemas.chat import (
    MessageCreate,
    MessageUpdate,
    UserChatsCreate,
    UserChatsUpdate,
    ChatCreate,
    ChatUpdate
)


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    async def create_user(
            self, db: AsyncSession, *, user_id: uuid.UUID, obj_in: MessageCreate
    ) -> Message:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data['user_id'] = user_id
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


class CRUDUserChats(CRUDBase[UserChats, UserChatsCreate, UserChatsUpdate]):
    async def get_by_parameters(
            self, db: AsyncSession, *, chat_id: uuid.UUID | int, user_id: uuid.UUID | int
    ) -> UserChats:
        q = select(self.model).where(self.model.chat_id == chat_id, self.model.user_id == user_id)
        result = await db.execute(q)
        curr = result.scalar()
        return curr


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    async def get_chats_by_type(self, db: AsyncSession, chat_type: str, offset: int = 0, limit: int = 0) -> list[Chat]:
        q = select(self.model).where(self.model.type == chat_type) #.offset(offset).limit(limit)
        result = await db.execute(q)
        curr = list(result.scalars())
        return curr


crud_message = CRUDMessage(Message)
crud_user_chats = CRUDUserChats(UserChats)
crud_chat = CRUDChat(Chat)
