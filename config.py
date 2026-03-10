from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str
    JWT_SECRET:str
    JWT_ALGORITHM:str
    REDIS_HOST:str ="local_host"
    REDIS_PORT:int = 6379
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore'
    )

settings = Settings()

# print(settings.model_dump())