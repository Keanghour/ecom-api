# app\core\config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = 'aTdsPDJA6ZnJxMp6GhpAyQ'  
    DATABASE_URL: str = 'sqlite:///./test.db' 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    # GOOGLE_AUTH_ENABLED=False  


    class Config:
        env_file = ".env"  

# Instantiate the settings object
settings = Settings()

