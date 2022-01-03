from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    token_expire_min: int = 30
    jwt_secret_key: str = '' #TODO: for generatin use "openssl rand -hex 32"
    jwt_algorithm: str = 'HS256'

    class Config:
        env_prefix = 'rra'


@lru_cache()
def get_settings() -> Settings:
    return Settings()
