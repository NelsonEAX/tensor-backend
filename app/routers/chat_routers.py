import dataclasses
import uuid
from enum import Enum

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, or_, func, desc, Row
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.exceptions import PermissionDenied, WrongNumberOfUsers
from app.helpers.tags import helper_update_chat_tags, helper_update_user_tags
from app.models.db import get_async_session

from app.crud.crud_user import crud_user
from app.crud.crud_chat import crud_chat, crud_message, crud_user_chats
from app.models.models import User, Chat, ChatTags, UserRole, UserChats, Message, Tag, ChatType
from app.auth import current_user

from app.shemas import user as user_schemas
from app.shemas import chat as chat_schemas
from app.shemas import category as search_schemas
from app.crud.crud_category import crud_chat_tags, crud_tag

chat_router = APIRouter(prefix="/chats", tags=["chats"])
message_router = APIRouter(prefix="/messages", tags=["messages"])


##################
# Chat endpoints #
##################


@chat_router.get("", response_model=list[chat_schemas.ChatWLastMessage])
async def user_chats(
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chats_obj = (await session.scalars(
        select(Chat).join(UserChats).filter(UserChats.user_id == user.id, Chat.deleted_at.is_(None)).
        offset(offset).limit(limit)
    )).all()
    chats_res = []

    for chat_obj in chats_obj:
        last_message = (await session.scalars(
            select(Message).join(Chat).filter(Message.chat_id == chat_obj.id).order_by(desc(Message.created_at))
        )).first()

        chats_res.append({"chat": chat_obj, "last_message": last_message})

    return chats_res

    # sub = select(func.max(Message.created_at)).where(Message.chat_id == Chat.id).correlate().scalar_subquery()
    # chats_obj = (await session.execute(
    #     select(Chat, Message).join(UserChats).outerjoin(Message, Message.chat_id == Chat.id).
    #     where(UserChats.user_id == user.id, Message.created_at == sub)
    # )).all()
    #
    # chats_messages = [{"chat": chat_obj, "last_message": message_obj} for chat_obj, message_obj in chats_obj]
    #
    # return chats_messages


@chat_router.get("/{chat_id}/inner", response_model=list[chat_schemas.Chat])
async def get_chat_inner(
        chat_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_inner = (await session.scalars(
        select(Chat).where(or_(Chat.parent_id == chat_id, Chat.id == chat_id)).offset(offset).limit(limit))).all()

    return chat_inner


@dataclasses.dataclass
class RecomendedObj:
    obj_name: str
    obj_id: uuid.UUID
    percent: float


class RecType(str, Enum):
    # для пользователей и чатов
    related: str = "related"
    # для событий
    absolute: str = "absolute"


# метод для возвращения нового объекта с процентом совместимости
def get_rec_objects_list(some_dict: dict, object_name: str, cur_user_tags_ids_set: set, rec_type: RecType):
    recs_list = []
    # проходимся по словарю и для каждого пользователя считаем процент совместимости
    for object_id, tags_list in some_dict.items():
        tags_ids_set = set(tag.id for tag in tags_list)
        if rec_type == RecType.related:
            max_tag_count = max(len(cur_user_tags_ids_set), len(tags_ids_set))
        else:
            max_tag_count = len(tags_ids_set)
        intersections = len(cur_user_tags_ids_set.intersection(tags_ids_set))
        percent = intersections / max_tag_count
        percent = round(percent*100)
        recs_list.append(
            RecomendedObj(
                obj_name=object_name,
                obj_id=object_id,
                percent=percent)
        )
    return recs_list


@chat_router.get("/recomended/userschats", response_model=list[user_schemas.UserRead | chat_schemas.Chat])
async def get_recomendations(
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    ### Получаем групповые и приватные ЧАТЫ ###
    all_user_chats = (await db.scalars(user.chats.statement)).all()

    # получаем все личные чаты пользователя
    cur_user_private_chats = []

    # получаем все групповые чаты пользователя
    cur_user_group_chats = []

    # сортируем чаты на приватные и групповые
    for i in all_user_chats:
        if i.type == "private":
            cur_user_private_chats.append(i)
        if i.type == "group":
            cur_user_group_chats.append(i)

    # получаем id собеседников, с которыми текущий пользователь общался лично, чтобы убрать этих юзеров из рекомендаций
    companions_id = []
    for private_chat in cur_user_private_chats:
        private_chat_users = (await db.scalars(private_chat.users.statement)).all()
        for private_chat_user in private_chat_users:
            if private_chat_user.id != user.id:
                companions_id.append(private_chat_user.id)

    ###Тут работаем с пользователями###
    # получаем теги текущего пользователя
    user_tags = (await db.scalars(user.tags.statement)).all()
    # получаем всех пользователей
    all_users = await crud_user.get_multi(db=db, offset=offset,
                                          limit=limit)
    all_users_tags_dict = {}
    ###Сортировка пользователей###
    # теги, складываем в словарь по пользователю
    for other_user in all_users:
        # чтобы в рекомендации случайно не попал сам пользователь и те, с кем он общался
        if other_user.id != user.id and other_user.id not in companions_id:
            others_tags = (await db.scalars(other_user.tags.statement)).all()

            # чтобы не попадали пользователи с 0 тегов
            if len(others_tags) >= 1:
                all_users_tags_dict[other_user.id] = others_tags

    set_cur_user_tags_ids_to_compare = set(tag.id for tag in user_tags)

    new_recomended_users: list[RecomendedObj] = get_rec_objects_list(
        some_dict=all_users_tags_dict,
        object_name="user",
        cur_user_tags_ids_set=set_cur_user_tags_ids_to_compare,
        rec_type=RecType.related
    )

    ### Работа с группами ###
    all_groups_tags_dict = {}
    # достаём id групп текущего пользователя
    cur_user_group_chats_ids = [group.id for group in cur_user_group_chats]
    # получаем вообще все группы
    all_groups = await crud_chat.get_chats_by_type(db=db, chat_type="group", offset=offset, limit=limit)

    # исключаем из всех групп группы пользователя и записываем в словарь
    for group in all_groups:
        if group.id not in cur_user_group_chats_ids:
            # получаем теги группы
            group_tags = (await db.scalars(group.tags.statement)).all()

            # выкидываем из списка чаты у которых нет тегов
            if len(group_tags) >= 1:
                all_groups_tags_dict[group.id] = group_tags

    # получаем список групп с процентом совместимости к текущему пользователю
    new_recomended_groups: list[RecomendedObj] = get_rec_objects_list(
        some_dict=all_groups_tags_dict,
        object_name="group",
        cur_user_tags_ids_set=set_cur_user_tags_ids_to_compare,
        rec_type=RecType.related
    )

    # объединяем две полученные кучки
    union_list = new_recomended_users + new_recomended_groups
    union_list.sort(key=lambda some_obj: some_obj.percent, reverse=True)

    # получаем итоговый список
    result_list = []
    for obj in union_list:
        if obj.obj_name == "user":
            us = await crud_user.get(db=db, model_id=obj.obj_id)
            json_view = jsonable_encoder(us)
            json_view['external']['percent'] = obj.percent
            result_list.append(json_view)
        if obj.obj_name == "group":
            us = await crud_chat.get(db=db, model_id=obj.obj_id)
            json_view = jsonable_encoder(us)
            json_view['external']['percent'] = obj.percent
            result_list.append(json_view)
    return result_list


@chat_router.get("/recomended/events", response_model=list[chat_schemas.Chat])
async def get_recomended_events(
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user), db: AsyncSession = Depends(get_async_session)):
    # получаем теги текущего пользователя
    user_tags = (await db.scalars(user.tags.statement)).all()

    all_events_tags_dict = {}
    all_events = await crud_chat.get_chats_by_type(db=db, chat_type="event", offset=offset, limit=limit)

    # получаем список id чатов в которых пользовать присутствует
    cur_user_chats = (await db.scalars(user.chats.statement)).all()
    cur_user_chats_ids = [cur_us_chat.id for cur_us_chat in cur_user_chats]

    # теги, складываем в словарь по событию
    for event in all_events:
        if event.id not in cur_user_chats_ids:
            event_tags = (await db.scalars(event.tags.statement)).all()

            # выкидываем из списка чаты у которых нет тегов
            if len(event_tags) >= 1:
                all_events_tags_dict[event.id] = event_tags

    set_cur_user_tags_ids_to_compare = set(tag.id for tag in user_tags)

    new_recomended_events: list[RecomendedObj] = get_rec_objects_list(
        some_dict=all_events_tags_dict,
        object_name="event",
        cur_user_tags_ids_set=set_cur_user_tags_ids_to_compare,
        rec_type=RecType.absolute
    )

    # сортируем по проценту
    new_recomended_events.sort(key=lambda x: x.percent, reverse=True)

    # формируем список событий по их id
    result_list = [await crud_chat.get(db=db, model_id=i.obj_id) for i in new_recomended_events]
    return result_list


# временный метод для обновления тегов пользователей
@chat_router.post("/tags/{user_id}", response_model=list[search_schemas.UserTags], deprecated=True)
async def update_user_tags(
        tags: list[str],  # list[search_schemas.TagCreate],
        user_id: uuid.UUID,
        session: AsyncSession = Depends(get_async_session)
):
    user = await crud_user.get(db=session, model_id=user_id)
    return await helper_update_user_tags(tags, user, session)


@chat_router.get("/{chat_id}", response_model=chat_schemas.Chat)
async def chat(
        chat_id: uuid.UUID,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    return chat_obj


@chat_router.get("/{chat_id}/messages", response_model=list[chat_schemas.Message])
async def chat_messages(
        chat_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    messages_obj = (await session.scalars(chat_obj.messages.statement.offset(offset).limit(limit))).all()
    return messages_obj


@chat_router.get("/{chat_id}/users", response_model=list[user_schemas.UserWRole])
async def chat_users(
        chat_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    users_obj = (await session.execute(
        select(User, UserChats.role).join(UserChats).
        filter(UserChats.chat_id == chat_id, UserChats.deleted_at.is_(None)).offset(offset).limit(limit)
    )).all()
    users_obj = [{"user": user, "role": role} for user, role in users_obj]
    return users_obj


@chat_router.get("/{chat_id}/tags", response_model=list[search_schemas.ChatTagsWithCategory])
async def chat_tags(
        chat_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    # TODO: Проверка, что запрашиваются теги для доступного чата/группы
    tags_obj = (await session.execute(select(
        ChatTags.id, ChatTags.chat_id, ChatTags.tag_id, ChatTags.title, Tag.category_id
    ).join(Tag, Tag.id == ChatTags.tag_id).where(ChatTags.chat_id == chat_id).offset(offset).limit(limit))).all()
    return tags_obj


@chat_router.post("", response_model=chat_schemas.Chat)
async def create_chat(
        chat: chat_schemas.ChatCreate,
        users_id: list[uuid.UUID],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.create(session, obj_in=chat)

    if chat.type == ChatType.private.value:
        if len(users_id) != 2:
            raise WrongNumberOfUsers()

        alias1 = aliased(UserChats)
        alias2 = aliased(UserChats)

        chat = (await session.execute(
            select(Chat).join(alias1, Chat.id == alias1.chat_id).where(alias1.user_id == users_id[0]).
            join(alias2, Chat.id == alias2.chat_id).where(alias2.user_id == users_id[1])
        )).first()

        print(chat)

        if chat:
            return chat[0]
        else:
            for user_id in users_id:
                user_chats_obj = chat_schemas.UserChatsCreate(user_id=user_id, chat_id=chat_obj.id,
                                                              role=UserRole.admin.value)
                await crud_user_chats.create(session, obj_in=user_chats_obj)

            return chat_obj

    for user_id in users_id:
        user_chats_obj = chat_schemas.UserChatsCreate(user_id=user_id, chat_id=chat_obj.id, role=UserRole.admin.value)
        await crud_user_chats.create(session, obj_in=user_chats_obj)

    return chat_obj


@chat_router.post("/{chat_id}/tags", response_model=list[search_schemas.ChatTags] | dict)
@chat_router.post("/{chat_id}/tags", response_model=list[search_schemas.ChatTagsWithCategory])
async def update_chat_tags(
        tags: list[str],  # list[search_schemas.TagCreate],
        chat_id: uuid.UUID,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    # TODO: Проверка, что устанавливаются теги для доступного (по правам) чата/группы

    user_chats_obj = await crud_user_chats.get_by_parameters(session, chat_id=chat_id, user_id=user.id)

    if not user_chats_obj or user_chats_obj.role not in (UserRole.admin.value, UserRole.moderator.value):
        raise PermissionDenied()

    chat_obj = await crud_chat.get(session, model_id=chat_id)  # сдвинуть влево
    return await helper_update_chat_tags(tags, chat_obj, session)


@chat_router.put("/{chat_id}", response_model=chat_schemas.Chat | dict)
async def update_chat(
        chat_id: uuid.UUID,
        chat: chat_schemas.ChatUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    user_chats_obj = await crud_user_chats.get_by_parameters(session, chat_id=chat_id, user_id=user.id)

    if not user_chats_obj or user_chats_obj.role not in (UserRole.admin.value, UserRole.moderator.value):
        raise PermissionDenied()

    chat_obj = await crud_chat.get(session, model_id=chat_id)
    updated_chat_obj = await crud_chat.update(session, db_obj=chat_obj, obj_in=chat)
    return updated_chat_obj


@chat_router.put("/{chat_id}/users")
async def add_chat_users(
        chat_id: uuid.UUID,
        users: list[chat_schemas.ChatUsers],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    for user in users:
        user_chats_obj = chat_schemas.UserChatsCreate(user_id=user.user_id, chat_id=chat_id, role=user.role)
        await crud_user_chats.create(session, obj_in=user_chats_obj)


@chat_router.put("/{chat_id}/users/role", response_model=None | dict)
async def update_chat_users_role(
        chat_id: uuid.UUID,
        users: list[chat_schemas.ChatUsers],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    user_chats_obj = await crud_user_chats.get_by_parameters(session, chat_id=chat_id, user_id=user.id)

    if not user_chats_obj or user_chats_obj.role not in (UserRole.admin.value):
        raise PermissionDenied()

    for user in users:
        user_chats_obj = crud_user_chats.get_by_parameters(session, chat_id=chat_id, user_id=user.user_id)
        setattr(user_chats_obj, "role", user.role)
        await crud_user_chats.update(session, obj_in=user_chats_obj)


@chat_router.delete("/{chat_id}", response_model=chat_schemas.Chat | dict)
async def delete_chat(
        chat_id: uuid.UUID, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    user_chats_obj = await crud_user_chats.get_by_parameters(session, chat_id=chat_id, user_id=user.id)

    if not user_chats_obj or user_chats_obj.role not in (UserRole.admin.value):
        raise PermissionDenied()

    deleted_chat_obj = await crud_chat.delete(session, model_id=chat_id)
    return deleted_chat_obj



# 92628958-6e50-45c8-aa5c-603622ac7ed8
@chat_router.delete("/{chat_id}/user", response_model=None | dict)
async def delete_chat_user(
        chat_id: uuid.UUID,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    user_chats_obj = await crud_user_chats.get_by_parameters(session, chat_id=chat_id, user_id=user.id)
    deleted_user_chats_obj = await crud_user_chats.delete(session, model_id=user_chats_obj.id)



@chat_router.delete("/{chat_id}/users", response_model=None | dict)
async def delete_chat_users(
        chat_id: uuid.UUID,
        users_id: list[uuid.UUID],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    user_chats_obj = await crud_user_chats.get_by_parameters(session, chat_id=chat_id, user_id=user.id)

    if not user_chats_obj or user_chats_obj.role not in (UserRole.admin.value, UserRole.moderator.value):
        raise PermissionDenied()

    for user_id in users_id:
        user_chats_obj = await crud_user_chats.get_by_parameters(session, chat_id=chat_id, user_id=user_id)
        deleted_user_chats_obj = await crud_user_chats.delete(session, model_id=user_chats_obj.id)


#####################
# Message endpoints #
#####################


# @message_router.get("", response_model=list[chat_schemas.Message])
# async def user_messages(
#         offset: int = 0,
#         limit: int = 100,
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     messages_obj = (await session.scalars(user.messages.statement.offset(offset).limit(limit))).all()
#     return messages_obj
#
#
# @message_router.get("/{message_id}", response_model=chat_schemas.Message)
# async def message(
#         message_id: uuid.UUID,
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     message_obj = await crud_message.get(session, model_id=message_id)
#     return message_obj
#
#
# @message_router.get("/{message_id}/user", response_model=user_schemas.UserRead)
# async def message_user(
#         message_id: uuid.UUID,
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     message_obj = await crud_message.get(session, model_id=message_id)
#     return message_obj.user
#
#
# @message_router.get("/{message_id}/chat", response_model=chat_schemas.Chat)
# async def message_chat(
#         message_id: uuid.UUID,
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     message_obj = await crud_message.get(session, model_id=message_id)
#     return message_obj.chat
#
#
# @message_router.post("", response_model=chat_schemas.Message)
# async def create_message(
#         message: chat_schemas.MessageCreate,
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     message_obj = await crud_message.create_user(session, user_id=user.id, obj_in=message)
#     return message_obj
#
#
# @message_router.put("", response_model=chat_schemas.Message)
# async def update_message(
#         message_id: uuid.UUID,
#         message: chat_schemas.MessageUpdate,
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     message_obj = await crud_message.get(session, model_id=message_id)
#     updated_message_obj = await crud_message.update(session, db_obj=message_obj, obj_in=message)
#     return updated_message_obj
#
#
@message_router.delete("", response_model=chat_schemas.Message)
async def delete_message(
        message_id: uuid.UUID,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    message_obj = await crud_message.get(session, model_id=message_id)
    deleted_message_obj = await crud_message.remove(session, model_id=message_obj.id)
    return deleted_message_obj



    # chats_obj = (await session.scalars(
    #     select(Chat).join(UserChats).filter(UserChats.user_id == user.id, Chat.parent_id.is_(None))
    # )).all()
    # chats_res = []
    #
    # for chat_obj in chats_obj:
    #     last_message = (await session.scalars(
    #         select(Message).join(Chat).filter(Message.chat_id == chat_obj.id).order_by(desc(Message.created_at))
    #     )).first()
    #
    #     chats_res.append({"chat": chat_obj, "last_message": last_message})  # child

    # await session.execute()
