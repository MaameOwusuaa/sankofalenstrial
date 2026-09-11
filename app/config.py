from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator

class Settings(BaseSettings):
    app_name: str = 'SankofaLens'
    environment: str = 'development'
    debug: bool = True
    secret_key: str = 'CHANGE_ME'
    access_token_expire_minutes: int = 60
    database_url: str
    openai_api_key: str | None = None
    openai_model: str | None = None
    frontend_origin: str = 'http://127.0.0.1:8000'
    map_tile_url: str = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=False, extra='ignore')

    @field_validator('secret_key')
    @classmethod
    def validate_secret(cls, v: str) -> str:
        if v == 'CHANGE_ME' and __import__('os').getenv('ENVIRONMENT', 'development') == 'production':
            raise ValueError('SECRET_KEY must be changed in production')
        return v
settings = Settings()
