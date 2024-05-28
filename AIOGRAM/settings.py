from dotenv import load_dotenv
import os

from pydantic_settings import BaseSettings

# файл .env в том же каталоге, что и скрипт
load_dotenv()


class Setting(BaseSettings):
    print(os.getenv("TOKEN"))
    TOKEN1: str = os.getenv("TOKEN1")
    TOKEN2: str = os.getenv("TOKEN2")
    ADMIN_ID: str = os.getenv("ADMIN_ID")


settings = Setting()
