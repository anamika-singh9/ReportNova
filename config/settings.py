import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    APP_NAME = os.getenv("APP_NAME")
    ENVIRONMENT = os.getenv("ENVIRONMENT")

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    GOOGLE_MODEL = os.getenv("GOOGLE_MODEL")
    TEMPERATURE = os.getenv("TEMPERATURE")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

    DATABASE_URL = os.getenv("DATABASE_URL")

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440)
    )

settings = Settings() 

