import uuid
from datetime import datetime
from typing import List

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import update, delete
from src.crud.models import User
from src.crud.schemas import CreateUser, CreateInFront, UpdateInUser
from src.database import get_async_session

# точка входа маршрутов
router = APIRouter(
    prefix="/api",
    tags=["Create and Delete"]
)


@router.get('/get_item_all', response_model=List[CreateUser], status_code=status.HTTP_200_OK)
async def get_user_all(session: AsyncSession = Depends(get_async_session)):
    """ Получение всех пользователей"""
    query = select(User)
    result = await session.execute(query)
    return [CreateUser(id=i.id, name=i.name, token=i.token) for i in result.scalars().all()]


@router.get('/get_item', response_model=List[CreateUser], status_code=status.HTTP_200_OK)
async def get_user(name: str, session: AsyncSession = Depends(get_async_session)):
    """ Получение пользователя по имени"""
    try:
        query = select(User).where(User.name == name)
        result = await session.execute(query)
        return [CreateUser(id=i.id, name=i.name, token=i.token) for i in result.scalars().all()]

    except Exception:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": None
        })


@router.put('/update', status_code=status.HTTP_202_ACCEPTED)
async def update_user(req: UpdateInUser, session: AsyncSession = Depends(get_async_session)):
    """ Изменение пользователя """
    name, id = req.dict().values()
    stmt = update(User).where(User.id == id) \
        .values(name=name, token=uuid.uuid4())
    await session.execute(stmt)
    await session.commit()
    return "Update Successfully"


@router.delete('/delete/{id}', status_code=status.HTTP_202_ACCEPTED)
async def delete_user(id: int, session: AsyncSession = Depends(get_async_session)):
    """ Удаление пользователя """
    stmt = delete(User).where(User.id == id)
    await session.execute(stmt)
    await session.commit()
    return "Delete Successfully"


@router.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(name: CreateInFront, session: AsyncSession = Depends(get_async_session)):
    """ Создание пользователя """
    name_serializers = name.dict()['name']
    stmt = select(User).where(User.name == name_serializers)
    result = await session.execute(stmt)
    if result.scalars().first() is None:
        stmt = User(name=name_serializers)
        session.add(stmt)
        await session.commit()
        return "Added Successfully"
    else:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%S.%fZ"),
            "details": 'Такое пользователь уже существует'
        })
