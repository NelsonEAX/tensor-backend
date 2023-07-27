import uuid

from pydantic import BaseModel
from datetime import datetime

from app.shemas.category import Tag

from enum import Enum

from app.models.models import MessageType

class ChatType(str, Enum):
    private: str = "private"
    group: str = "group"
    event: str = "event"


class UserRole(str, Enum):
    user: str = "user"
    admin: str = "admin"
    moderator: str = "moderator"


###################
# Message schemas #
###################

class MessageBase(BaseModel):
    type: str
    external: dict | None = None


class MessageCreate(MessageBase):
    chat_id: uuid.UUID


class MessageUpdate(MessageBase):
    pass


class MessageDB(BaseModel):
    id: uuid.UUID
    type: MessageType
    user_id: uuid.UUID
    chat_id: uuid.UUID
    external: dict | None
    created_at: datetime

    class Config:
        orm_mode = True


class Message(MessageDB):
    pass


#####################
# UserChats schemas #
#####################

class UserChatsBase(BaseModel):
    role: UserRole = UserRole.user


class UserChatsCreate(UserChatsBase):
    user_id: uuid.UUID
    chat_id: uuid.UUID


class UserChatsUpdate(UserChatsBase):
    pass


class UserChatsDB(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    chat_id: uuid.UUID
    role: UserRole

    class Config:
        orm_mode = True


class UserChats(UserChatsDB):
    pass


################
# Chat schemas #
################

class ChatBase(BaseModel):
    external: dict | None = None
    parent_id: uuid.UUID | None = None


class ChatCreate(ChatBase):
    type: ChatType = ChatType.private


class ChatUpdate(ChatBase):
    pass


class ChatUsers(BaseModel):
    user_id: uuid.UUID
    role: UserRole


class ChatDB(BaseModel):
    id: uuid.UUID
    type: ChatType
    external: dict
    parent_id: uuid.UUID | None

    # tags: list[Tag]

    class Config:
        orm_mode = True


class Chat(ChatDB):
    pass


class ChatWLastMessage(BaseModel):
    chat: Chat
    last_message: Message | None


class UserChatsWMAC(BaseModel):
    chat: Chat
    date: datetime
    last_message: dict | None
    children: list[Chat] | None


