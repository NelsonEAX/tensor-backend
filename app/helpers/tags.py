import uuid
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import app_settings
from app.models.models import User, Tag, UserTags, ChatTags, Chat
import re
import pymorphy2
from sqlalchemy import select, delete

morph = pymorphy2.MorphAnalyzer()


@lru_cache(maxsize=1024, typed=False)
def _normalize_tag(original_tag: str) -> dict:
    tag = original_tag.lower()
    # Удаляем все пробельные символы
    tag = re.sub(r"\s+", "", tag, flags=re.UNICODE)
    morphed = morph.parse(tag)[0]

    if morphed.tag.POS not in (
            'NOUN', 'ADVB', 'NPRO',
            # Глагольные
            'VERB', 'INFN', 'PRTF', 'PRTS',
            # Прилагательные
            'GRND', 'ADJF', 'ADJS', 'COMP',
            # Часи речи, которые никак не преобразуем
            'NUMR', 'PRED', 'PREP', 'CONJ', 'PRCL', 'INTJ'
    ):
        return {
            'original': original_tag,
            'normalized': tag,
            # 'uuid': str(uuid.uuid4()),
        }

    if morphed.tag.POS in ('NOUN', 'ADVB', 'NPRO'):
        normal = morphed.inflect({'sing', 'nomn', 'neut'})
        if normal:
            morphed = normal

    elif morphed.tag.POS in ('VERB', 'INFN', 'PRTF', 'PRTS', 'GRND'):
        normal = morphed.inflect({'INFN', 'sing', 'nomn', 'neut'})
        if normal:
            morphed = normal

    elif morphed.tag.POS in ('ADJF', 'ADJS', 'COMP'):
        normal = morphed.inflect({'ADJF', 'sing', 'nomn', 'neut'})
        if normal:
            morphed = normal

    if morphed:
        morphed = morphed.word

    return {
        'original': original_tag,
        'normalized': morphed,
        # 'uuid': str(uuid.uuid4()),
    }


def _normalize_tags(tags: list[str]) -> list[dict]:
    """"""
    result = []
    for original_tag in tags:
        result.append(_normalize_tag(original_tag))

    print(result)
    return result


async def _find_tag_models(
        normalized_tags: list[dict],
        session: AsyncSession
):
    for item in normalized_tags:
        result = await session.execute(select(Tag).where(Tag.title == item['normalized']))
        tag = result.scalar()

        if tag is None:
            tag = Tag(
                title=item['normalized'],
                category_id=app_settings.USER_CATEGORY,
            )
            session.add(tag)
            await session.commit()

        item['model'] = tag
    print(normalized_tags)


async def helper_update_user_tags(
        tags: list[str],  # list[search_schemas.TagCreate],
        user: User,
        session: AsyncSession
):
    """
    Устанавливаем переданные теги.
    Сначала удаляем все связи объекта, потом накатываем новые
    """

    # Нормализуем теги
    normalized_tags = _normalize_tags(tags)

    # Проверям их наличие в БД, дозаписываем недостающие
    await _find_tag_models(normalized_tags, session)

    # Удаляем существующие связи c Tag для User/Chat
    await session.execute(delete(UserTags).where(UserTags.user_id == user.id))
    await session.commit()

    # Создаем новые связи c Tag для User/Chat
    for item in normalized_tags:
        user_tag = UserTags(
            user_id=user.id,
            tag_id=item['model'].id,
            title=item['original'],
        )
        session.add(user_tag)
        await session.commit()

    return (await session.execute(select(
        UserTags.id, UserTags.user_id, UserTags.tag_id, UserTags.title, Tag.category_id
    ).join(Tag, Tag.id == UserTags.tag_id).where(UserTags.user_id == user.id))).all()


async def helper_update_chat_tags(
        tags: list[str],  # list[search_schemas.TagCreate],
        chat: Chat,
        session: AsyncSession
):
    """
    Устанавливаем переданные теги.
    Сначала удаляем все связи объекта, потом накатываем новые
    """

    # Нормализуем теги
    normalized_tags = _normalize_tags(tags)

    # Проверям их наличие в БД, дозаписываем недостающие
    await _find_tag_models(normalized_tags, session)

    # Удаляем существующие связи c Tag для User/Chat
    await session.execute(delete(ChatTags).where(ChatTags.chat_id == chat.id))
    await session.commit()

    # Создаем новые связи c Tag для User/Chat
    for item in normalized_tags:
        chat_tag = ChatTags(
            chat_id=chat.id,
            tag_id=item['model'].id,
            title=item['original'],
        )
        session.add(chat_tag)
        await session.commit()

    return (await session.execute(select(
        ChatTags.id, ChatTags.chat_id, ChatTags.tag_id, ChatTags.title, Tag.category_id
    ).join(Tag, Tag.id == ChatTags.tag_id).where(ChatTags.chat_id == chat.id))).all()
