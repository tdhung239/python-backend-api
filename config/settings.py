import os

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    DATABASE_URL = os.environ["DATABASE_URL"]
    PORT = os.environ["PORT"]
    SMTP_SERVER = os.environ["SMTP_SERVER"]
    SENDER_EMAIL = os.environ["SENDER_EMAIL"]
    PASSWORD = os.environ["PASSWORD"]
    SECRET_KEY = os.environ["SECRET_KEY"]
    ALGORITHM = os.environ["ALGORITHM"]
    ACCESS_TOKEN_EXPIRE_MINUTES = os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"]

    class Config:
        env_file = "..env"


settings = Settings()
