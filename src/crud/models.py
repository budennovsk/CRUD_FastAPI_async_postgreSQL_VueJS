import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# создаем модель, объекты которой будут храниться в бд
Base = declarative_base()


# создаем модель, объекты которой будут храниться в бд
class User(Base):
    """Модель БД """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    token = Column(UUID(as_uuid=True), default=uuid.uuid4)

    def __repr__(self):
        return f'{self.id!r},{self.name!r},{self.token!r}'
