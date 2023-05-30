from fastapi import FastAPI

from src.crud.router import router

app = FastAPI(
    title="CRUD_APP"
)

app.include_router(router)
