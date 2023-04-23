from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.init_db import init_db
from app.routes.auth import router as auth_router
from app.routes.social_auth import router as social_router
from app.routes.task import router as task_router
from app.routes.user import router as user_router

app = FastAPI()

app.include_router(task_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(social_router)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


@app.get("/url-list")
def get_all_urls():
    url_list = [{"path": route.path, "name": route.name} for route in app.routes]
    return url_list
