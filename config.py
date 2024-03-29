import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    bot_token: str = os.getenv("BOT_TOKEN")
    openai_token: str = os.getenv("OPENAI_TOKEN")
    db_url: str = os.getenv("DB_URL")


settings = Settings()
