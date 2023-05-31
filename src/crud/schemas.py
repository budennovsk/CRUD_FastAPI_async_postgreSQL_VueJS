import uuid

from pydantic import BaseModel


class CreateUser(BaseModel):
    """Валидация данных"""
    token: uuid.UUID
    name: str
    id: int

    class Config:
        orm_mode = True


class CreateInFront(BaseModel):
    """Валидация данных"""
    name: str

    class Config:
        orm_mode = True


class UpdateInUser(CreateInFront):
    """Валидация данных"""
    id: int
