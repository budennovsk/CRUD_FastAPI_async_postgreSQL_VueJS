import uuid
from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy import update, delete
from src.crud.models import User
from src.crud.schemas import CreateUser
from src.database import get_async_session

app = FastAPI(
    title="CRUD_App"
)


@app.post('/create', status_code=status.HTTP_201_CREATED)
async def create_user(name: str, session: AsyncSession = Depends(get_async_session)):
    stmt = select(User).where(User.name == name)
    result = await session.execute(stmt)
    if result.scalars().first() is None:
        stmt = User(name=name)
        session.add(stmt)
        await session.commit()
    else:
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": datetime.strftime(datetime.utcnow(), "%Y-%m-%dT%H:%M:%S.%fZ"),
            "details": 'Такое пользователь уже существует'
        })


@app.get('/get_item', response_model=List[CreateUser], status_code=status.HTTP_200_OK)
async def get_user(name: str, session: AsyncSession = Depends(get_async_session)):
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


@app.put('/update')
async def update_user(name: str, id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = update(User).where(User.id == id) \
        .values(name=name, token=uuid.uuid4())
    await session.execute(stmt)
    await session.commit()


@app.delete('/delete')
async def delete_user(name: str, id: int, session: AsyncSession = Depends(get_async_session)):
    stmt = delete(User).where(User.id == id, User.name == name)
    await session.execute(stmt)
    await session.commit()


@app.get('/get_item_all', response_model=List[CreateUser], status_code=status.HTTP_200_OK)
async def get_user_all(session: AsyncSession = Depends(get_async_session)):
    query = select(User)
    result = await session.execute(query)
    return [CreateUser(id=i.id, name=i.name, token=i.token) for i in result.scalars().all()]
