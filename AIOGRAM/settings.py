from environs import Env
from dataclasses import dataclass
from dotenv import load_dotenv
import os

from pydantic_settings import BaseSettings

# @dataclass
# class Bots:
#     bot_token: str
#     admin_id: int
#
# @dataclass
# class Settings:
#     bots: Bots
#
#
# def get_settings(path: str):
#     env = Env()
#     env.read_env(path)
#
#     return Settings(
#         bots=Bots(
#             bot_token=env.str("TOKEN"),
#             admin_id=env.int("ADMIN_ID")
#         )
#     )

# settings = get_settings("input")
# print(settings)

# НОВЫЕ настройки

load_dotenv()


class Setting(BaseSettings):
    print(os.getenv("TOKEN"))
    TOKEN: str = os.getenv("TOKEN")
    ADMIN_ID: str = os.getenv("ADMIN_ID")


settings = Setting()
