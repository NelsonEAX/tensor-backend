import uuid

from sqlalchemy import select, null, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import app_settings
from app.crud.crud_base import CRUDBase
from app.models.models import Tag, UserTags, ChatTags, Category
from app.shemas.category import (
    TagCreate,
    TagUpdate,
    UserTagsCreate,
    UserTagsUpdate,
    ChatTagsCreate,
    ChatTagsUpdate,
    CategoryCreate,
    CategoryUpdate
)


class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    async def exist_create(self, db: AsyncSession, *, tags: list[TagCreate]) -> list[Tag]:
        tags_title = [tag.title for tag in tags]
        q = select(self.model).where(self.model.title.in_(tags_title))
        result = await db.execute(q)
        curr = list(result.scalars())
        curr_titles = [c.title for c in curr]
        tags = [tag for tag in tags if tag.title not in curr_titles]

        for tag in tags:
            tag_obj = await self.create(db, obj_in=tag)
            curr.append(tag_obj)

        return curr

    async def get_multi(
            self,
            db: AsyncSession,
            *,
            offset: int = 0,
            limit: int = 1000
    ) -> list[Tag]:

        q = select(Tag)\
            .join(Category, and_(Category.id == Tag.category_id,
                                 Category.id != app_settings.USER_CATEGORY))\
            .filter(Category.deleted_at == null())\
            .order_by(Category.order)\
            .order_by(Tag.display)

        result = await db.execute(q)
        curr = list(result.scalars())
        return curr


class CRUDUserTags(CRUDBase[UserTags, UserTagsCreate, UserTagsUpdate]):
    async def get_by_user(self, db: AsyncSession, user_id: uuid.UUID | int) -> list[UserTags]:
        q = select(self.model).where(self.model.user_id == user_id)
        result = await db.execute(q)
        curr = list(result.scalars())
        return curr

    async def get_by_parameters(
            self, db: AsyncSession, *, user_id: uuid.UUID | int, tag_id: uuid.UUID | int
    ) -> UserTags:
        q = select(self.model).where(self.model.user_id == user_id, self.model.tag_id == tag_id)
        result = await db.execute(q)
        curr = result.scalar()
        return curr


class CRUDChatTags(CRUDBase[ChatTags, ChatTagsCreate, ChatTagsUpdate]):
    async def get_by_parameters(
            self, db: AsyncSession, *, chat_id: uuid.UUID | int, tag_id: uuid.UUID | int
    ) -> ChatTags:
        q = select(self.model).where(self.model.chat_id == chat_id, self.model.tag_id == tag_id)
        result = await db.execute(q)
        curr = result.scalar()
        return curr


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass


crud_tag = CRUDTag(Tag)
crud_user_tags = CRUDUserTags(UserTags)
crud_chat_tags = CRUDChatTags(ChatTags)
crud_category = CRUDCategory(Category)
