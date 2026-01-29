from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    #.env
    DEBUG: bool
    PORT: int
    DB_PATH: str

    AUTH_SECRET_KEY: str
    AUTH_ALGORITHM: str
    AUTH_TOKEN_LIFETIME_IN_MIN: int
    AUTH_REFRESH_LIFETIME_IN_DAYS: int

    REDIS_URL: str
    REDIS_EXPIRE: int
    REDIS_POOL_SIZE: int
    REDIS_PREFIX: str

    FRONTEND_URL: str

    BLOCKER_URL: str
    BLOCKER_PREFIX: str

    DISPATCHER_URL: str
    DISPATCHER_CODE: str
    DISPATCHER_APP: str


settings = Settings()
