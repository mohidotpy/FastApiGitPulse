from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schema.base_schema import FindBase, AllOptional


class BaseUser(BaseModel):
    email: str
    user_token: str
    name: str


class UserSchema(BaseModel):
    id: int
    email: str
    user_token: str

    class Config:
        orm_mode = True


class CurrentUserSchema(BaseModel):
    id: int
    email: str
    user_token: str

    class Config:
        orm_mode = True


class UpsertUserSchema(BaseUser, metaclass=AllOptional):
    ...


class UserSignInSchema(BaseModel):
    access_token: str
    expiration: datetime
    user_info: UserSchema


class FindUserSchema(FindBase, BaseModel, metaclass=AllOptional):
    email: str
    ...


class UserQuerySchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    page: int = 1
    page_size: Optional[int] = 10
    ordering: str = "id"
