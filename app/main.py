from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.init_db import init_db
from app.routes.auth import router as auth_router
from app.routes.social_auth import router as social_router
from app.routes.task import router as task_router
from app.routes.user import router as user_router
from app.utils.mail_utils import write_creds_to_json

app = FastAPI()

app.include_router(task_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(social_router)

app.add_middleware(SessionMiddleware, secret_key=settings.secret_key)


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()
    await write_creds_to_json()


@app.get("/healthcheck")
def service_healthy():
    return {"status": "ok"}


@app.get("/")
def root():
    return {
        "social_auth": f"{settings.base_url}{social_router.url_path_for('login')}",
        "json_schema": f"{settings.base_url}{app.openapi_url}",
        "swagger": f"{settings.base_url}{app.docs_url}",
        "redoc": f"{settings.base_url}{app.redoc_url}",
    }
