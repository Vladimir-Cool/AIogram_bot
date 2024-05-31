from aiogram.filters import BaseFilter
from aiogram.types import Message


class MemberInTextFilter(BaseFilter):

    def __call__(self, message: Message) -> bool:
        entities = message.entities or []
        
