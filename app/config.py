from pydantic import BaseSettings, MongoDsn

MongoDsn.allowed_schemes.add("mongodb+srv")


class Settings(BaseSettings):
    mongodb_url: MongoDsn
    secret_key_access: str
    secret_key_refresh: str
    secret_key: str
    access_token_expires: int = 60 * 24
    refresh_token_expires: int = 60 * 24 * 7
    email_token_expires: int = 20  # TODO make 15
    algorithm = "HS256"
    google_client_id: str
    google_client_secret: str

    class Config:
        env_file = ".env"


settings = Settings()
