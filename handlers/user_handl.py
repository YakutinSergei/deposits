from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from create_bot import bot
from data_base.base import db_users_add, db_user
from handlers import apsheduler
from keyboards.user_kb import create_kb_menu
from lexicon.lexicon_ru import LEXICON_PROFILE

router: Router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    # await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    user = await db_user(message.from_user.id)
    if not user:
        await db_users_add(message.from_user.id, message.from_user.first_name)
        print('создали')
    user = await db_user(message.from_user.id)
    await message.answer(text='<b><i><u>ПРОФИЛЬ</u></i></b>\n'
                              f'<b><u>Баланс: </u></b> {user["balanc"]}{LEXICON_PROFILE["price"]}\n'
                              f'<b><u>Заполненность склада:</u></b> {user["full_warehouse"]/user["volume_warehouse"]*100} %\n'
                              f'<b><u>Рейтинг:</u></b> {user["rating"]}', reply_markup=create_kb_menu(user['name_deposit']))

    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(apsheduler.warehouse_add, trigger='interval', seconds=10, kwargs={'message': message})
    scheduler.start()
