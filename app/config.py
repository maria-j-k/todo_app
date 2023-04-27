import os

from dotenv import load_dotenv
from pydantic import BaseSettings, MongoDsn, ValidationError

MongoDsn.allowed_schemes.add("mongodb+srv")


class BaseAppSettings(BaseSettings):
    base_url: str = "http://127.0.0.1:8000"
    secret_key_access: str
    secret_key_refresh: str
    secret_key: str
    access_token_expires: int = 60 * 24
    refresh_token_expires: int = 60 * 24 * 7
    email_token_expires: int = 25
    algorithm = "HS256"
    google_client_id: str
    google_client_secret: str

    class Config:
        env_file = ".env"


class DevSettings(BaseAppSettings):
    mongo_url: MongoDsn
    mongo_db_name: str = "to-do"


class TestSettings(BaseAppSettings):
    mongo_url: MongoDsn
    mongo_db_name: str = "test"


def get_settings():
    load_dotenv()
    environment = os.environ.get("ENVIRONMENT")
    return get_config(environment)


def get_config(environment):
    if environment == "dev" or not environment:
        config = DevSettings(mongo_url=os.environ.get("MONGODB_URL"))
        return config
    if environment == "test":
        config = TestSettings(mongo_url=os.environ.get("MONGO_TEST_DB_URL"))
        return config
    if environment == "docker":
        config = DevSettings(mongo_url=os.environ.get("MONGO_DOCKER_URL"))
        return config
    raise ValidationError("Improper environment value")


settings = get_settings()
