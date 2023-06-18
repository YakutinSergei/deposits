from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from create_bot import bot
from data_base.base import db_users_add, db_mines
from keyboards.user_kb import create_kb_menu

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await db_users_add(message.from_user.id, message.from_user.first_name)
    user = await db_mines(message.from_user.id)
    await message.answer(text='<b><i><u>ПРОФИЛЬ</b></i></u>\n'
                              f'<b><u>Склад: </u></b> {user["volume_warehouse"]}'
                              f'<u>:</u> {user["full_warehouse"]/user["rating"]*100} %\n'
                              f'<b><u>Рейтинг:</u></b> {user["rating"]}', reply_markup=create_kb_menu(user['name_deposit']))