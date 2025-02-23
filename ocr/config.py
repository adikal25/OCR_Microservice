from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    REDIS_HOST: str = "localhost"  
    REDIS_PORT: int = 6379
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"  
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"  


settings = Settings()
