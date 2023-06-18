from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message

from create_bot import bot
from data_base.base import db_users_add, db_mines
from keyboards.user_kb import create_kb_menu
from lexicon.lexicon_ru import LEXICON_MINES
router: Router = Router()

@router.message(Text(text=[LEXICON_MINES['natural_gas'], LEXICON_MINES['uranium'], LEXICON_MINES['coal'],
                           LEXICON_MINES['oil'], LEXICON_MINES['gold']]))
async def mines(message: Message):
    await message.answer(te)