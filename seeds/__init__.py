from datetime import datetime
from typing import Type, Generator

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import UserChats, User, Chat, Base, Category
from seeds.const import password, created_at, today, dt_format, dt_fields, dt_fields2
from seeds.messages import seed_messages
from seeds.tags import categories, seed_category_tags
from seeds.user_chats import users, get_fake_user_item
from seeds.chat_tags import chats, user_chats, get_fake_chat_item
from sqlalchemy import select

from seeds.user_tags import seed_chat_tags, seed_user_tags


async def seed_list(session: AsyncSession, model: Type[Base], items: list | Generator):
    for item in items:
        db_item = await session.get(model, item['id'])
        if db_item:
            if hasattr(db_item, 'external'):
                setattr(db_item, 'external', item['external'])

            if hasattr(db_item, 'deleted_at'):
                setattr(db_item, 'deleted_at',
                        datetime.utcnow() if item.get('deleted', False) else item.get('deleted_at', None))
            session.add(db_item)
        else:
            item = item | dt_fields
            session.add(model(**item))
    await session.commit()


async def seed(session: AsyncSession):
    """
    Заполняем базу тестовыми данными. Эти же данные можно предварительно выгрузить на прод, как демонстрационные
    :param session:
    :return:
    """
    await seed_list(session, User, get_fake_user_item())
    await seed_list(session, Chat, get_fake_chat_item())

    for item in user_chats:
        db_item = (await session.execute(select(UserChats)
                                         .where(UserChats.user_id == item['user_id'])
                                         .where(UserChats.chat_id == item['chat_id']))).scalar()
        if db_item:
            continue

        item = item | dt_fields2
        session.add(UserChats(**item))
    await session.commit()

    await seed_messages(session)

    await seed_list(session, Category, categories)
    await seed_category_tags(session)

    # # Вставка тегов очень длительная операция! С осторожностью
    # await seed_user_tags(session)
    # await seed_chat_tags(session)
