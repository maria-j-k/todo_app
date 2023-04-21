from fastapi import FastAPI

from app.init_db import init_db
from app.routes import router

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}
