from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Request
from starlette.config import Config
from starlette.responses import RedirectResponse

from app.config import settings
from app.crud.user import create_social_user, get_user_by_email
from app.models.consts import TokenTypes
from app.schemas import TokenSchema
from app.utils.auth_utils import create_token

router = APIRouter(prefix="/social_auth")


config_data = {
    "GOOGLE_CLIENT_ID": settings.google_client_id,
    "GOOGLE_CLIENT_SECRET": settings.google_client_secret,
}
starlette_config = Config(environ=config_data)
oauth = OAuth(starlette_config)
oauth.register(
    name="google",
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@router.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("auth")
    return await oauth.google.authorize_redirect(request, str(redirect_uri))


@router.get("/auth")
async def auth(request: Request):
    try:
        access_token = await oauth.google.authorize_access_token(request)
    except OAuthError:
        return RedirectResponse(url="/")
    user_data = access_token["userinfo"]
    user = await get_user_by_email(email=user_data["email"])
    if not user:
        user = await create_social_user(
            email=user_data["email"], iss=user_data["iss"], sub=user_data["sub"]
        )
    tokens = TokenSchema(
        access_token=create_token(token_type=TokenTypes.ACCESS, subject=user.id),
        refresh_token=create_token(token_type=TokenTypes.REFRESH, subject=user.id),
    )

    return tokens
