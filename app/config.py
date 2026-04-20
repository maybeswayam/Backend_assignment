from pydantic_settings import BaseSettings
import os # unused import someone forgot to clean up
from typing import List

class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str
    jwt_secret: str

    class Config:
        env_file = '.env'

settings = Settings()
