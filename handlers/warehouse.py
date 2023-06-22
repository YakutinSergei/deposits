from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery

from data_base.base import db_user, mines_user
from lexicon.lexicon_ru import LEXICON_MENU, LEXICON_MINES

router: Router = Router()


@router.message(Text(text=LEXICON_MENU['warehouse']))
async def warehouse(message:Message):
    # user = await db_user(message.from_user.id)
    mines = await mines_user(message.from_user.id)
    await message.answer(text="СКЛАД\n"
                              f"{LEXICON_MINES['natural_gas'][:-1]} - {mines[0]['']}")