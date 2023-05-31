from fastapi import FastAPI

from src.crud.router import router
from fastapi.middleware.cors import CORSMiddleware

# приложение
app = FastAPI(
    title="CRUD_APP"
)
# маршрутизация
app.include_router(router)

# разрешение на доступ к backend, список доступных запросов

# origins = [
#     "http://localhost:3000",
#     "http://localhost:8080",
#     "http://127.0.0.1:8000",
# ]


origins = ["*"]

# Cors для работы front & back через заголовки связь
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)

# передаем маршруты в приложение с модуля router
app.include_router(router)
