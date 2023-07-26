import uuid
from typing import Optional

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import app_settings
from app.helpers.tags import helper_update_user_tags
from app.models.db import User, get_async_session
from app.models.models import UserTags, Tag
from app.shemas.user import UserRead, UserCreate, EmailOrPhone, UserUpdate
from app.auth.manager import get_user_manager
from app.crud.crud_user import crud_user
from app.crud.crud_category import crud_tag, crud_user_tags
from app.shemas import category as search_schemas


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=app_settings.JWT_SECRET, lifetime_seconds=app_settings.JWT_LIFETIME)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()
current_active_user = fastapi_users.current_user(active=True)

additional_users_router = APIRouter(prefix="/current", tags=["current"])


@additional_users_router.get("", response_model=UserRead)
async def get_user(user: User = Depends(current_user)):
    return user


@additional_users_router.post("", response_model=UserRead)
async def post_user(
        user_update: UserUpdate, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    updated_user = await crud_user.update(session, db_obj=user, obj_in=user_update)
    return updated_user


@additional_users_router.get("/tags", response_model=list[search_schemas.UserTagsWithCategory])
async def user_tags(
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    tags_obj = (await session.execute(select(
        UserTags.id, UserTags.user_id, UserTags.tag_id, UserTags.title, Tag.category_id
    ).join(Tag, Tag.id == UserTags.tag_id).where(UserTags.user_id == user.id).offset(offset).limit(limit))).all()
    return tags_obj


@additional_users_router.post("/tags", response_model=list[search_schemas.UserTagsWithCategory])
async def update_user_tags(
        tags: list[str],  # list[search_schemas.TagCreate],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await helper_update_user_tags(tags, user, session)


@additional_users_router.delete("", response_model=UserRead)
async def remove_user_by_id(
        user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    await session.delete(user)
    await session.commit()
    return user


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/{id}", response_model=UserRead)
async def get_user_by_id(
        id: uuid.UUID, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    user = (await session.scalars(select(User).filter(User.id == id))).first()
    print(user)
    return user


auth_router = APIRouter()


@auth_router.post("/find", response_model=UserRead, response_model_include={"email", "id"}, )
async def auth_find(
        email: EmailOrPhone,
        session: AsyncSession = Depends(get_async_session)
):
    statement = select(User).where(
        func.lower(User.email) == func.lower(email.email)
    )
    results = await session.execute(statement)
    user = results.unique().scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="USER_NOT_EXISTS")
    return user


def include_auth_router(app: FastAPI) -> None:
    """
    Добавляем в приложение роуты авторизации и регистрации
    """
    app.include_router(
        fastapi_users.get_auth_router(auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth",
        tags=["auth"],
    )

    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )

    # app.include_router(
    #     fastapi_users.get_users_router(UserRead, UserUpdate),
    #     prefix="/users",
    #     tags=["users"],
    # )

    app.include_router(
        auth_router,
        prefix="/auth",
        tags=["auth"]
    )

    app.include_router(
        additional_users_router,
    )

    app.include_router(
        user_router,
    )
