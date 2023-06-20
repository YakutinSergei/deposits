from aiogram import Router
from aiogram.types import Message

router: Router = Router()



# Хэндлер для сообщений, которые не попали в другие хэндлеры
@router.message()
async def send_answer(message: Message):
    pass