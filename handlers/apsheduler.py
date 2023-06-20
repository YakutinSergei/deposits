from aiogram import Bot
from aiogram.types import Message




async def warehouse_add(bot: Bot, message: Message):
    await bot.send_message(message.from_user.id, f'прошло время')
