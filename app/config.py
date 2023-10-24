from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_PASSWORD: str
    DATABASE_USERNAME: str
    DATABASE_NAME: str
    DATABASE_HOST: str
    DATABASE_PORT: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = '.env'


settings = Settings()
