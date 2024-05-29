import re
from typing import List

from aiogram.filters import BaseFilter
from aiogram.types import Message


class WordFilter(BaseFilter):
    """Фильтр для поиска слов из списка в текстве"""
    def __init__(self, search_list: List[str]):
        self.search_list = search_list

    async def __call__(self, message: Message) -> bool:
        for search_str in self.search_list:
            if re.search(search_str, message.text, re.IGNORECASE):
                return True
        return False
