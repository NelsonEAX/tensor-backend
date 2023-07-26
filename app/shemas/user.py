import uuid
from typing import Optional, Union

import phonenumbers
from fastapi_users import schemas
from pydantic import BaseModel, EmailStr, Field
from pydantic.validators import strict_str_validator

from app.models.models import UserRole


class PhoneNumber(str):
    """Phone Number Pydantic type, using google's phonenumbers"""

    @classmethod
    def __get_validators__(cls):
        yield strict_str_validator
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        # Remove spaces
        v = v.strip().replace(' ', '')
        try:
            pn = phonenumbers.parse(v, "RU")
        except phonenumbers.phonenumberutil.NumberParseException:
            raise ValueError('value is not a valid phone')

        # Обрубаем возможность передать слишком длинный номер
        if len(str(pn.national_number)) != 10:
            raise ValueError('value is not a valid phone')

        return cls(phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164))


class UserRead(schemas.BaseUser[uuid.UUID]):
    email: Union[EmailStr, PhoneNumber]
    external: dict | None = None


class UserCreate(schemas.BaseUserCreate):
    email: Union[EmailStr, PhoneNumber]
    external: dict | None = None


class UserUpdate(schemas.BaseUserUpdate):
    # Не даем менять базовое поле
    email: Optional[Union[EmailStr, PhoneNumber]] = Field(exclude=True)
    external: dict | None = None


class EmailOrPhone(BaseModel):
    email: Union[EmailStr, PhoneNumber]


class UserWRole(BaseModel):
    user: UserRead
    role: UserRole

