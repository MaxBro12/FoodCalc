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

    FRONTEND_URL: str
    NCT_AUTH_URL: str

    DISPATCHER_URL: str
    DISPATCHER_CODE: str
    DISPATCHER_APP: str


settings = Settings()
