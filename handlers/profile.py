from aiogram import Router
from aiogram.filters import CommandStart, Text
from aiogram.types import Message, CallbackQuery

from create_bot import bot
from data_base.base import db_users_add, db_user, mines_user, name_mines_up, user_balanc_up, user_price_mines, \
    workers_user

from keyboards.user_kb import create_inline_kb, create_kb_menu
from lexicon.lexicon_ru import LEXICON_MINES, LEXICON_PROFILE

router: Router = Router()

#Меню месторождения
@router.message(Text(text=[LEXICON_MINES['natural_gas'], LEXICON_MINES['uranium'], LEXICON_MINES['coal'],
                           LEXICON_MINES['oil'], LEXICON_MINES['gold'], LEXICON_MINES['uranium_open'],
                           LEXICON_MINES['coal_open'], LEXICON_MINES['oil_open'], LEXICON_MINES['gold_open']]))
async def mines_choice(message:Message):
    mines = await mines_user(message.from_user.id)
    await workers_user(message.from_user.id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(text='Выбирите месторождение', chat_id= message.from_user.id,
                           reply_markup=create_inline_kb(1, 'mines_choice_', mines[0]['name'],
                                                                             mines[1]['name'],
                                                                             mines[2]['name'],
                                                                             mines[3]['name'],
                                                                             mines[4]['name']))

#Выбор место рождения
@router.callback_query(Text(startswith='mines_choice_'))
async def mines_selection(callback: CallbackQuery):
    mines = await mines_user(callback.from_user.id)

    if callback.data.split('_')[-1] == mines[0]['name']:
        if mines[0]['availability'] == 1:
            await name_mines_up(callback.from_user.id, mines[0]['name'])
            user = await db_user(callback.from_user.id)
            await callback.message.answer(text=f'Вы перешли на месторождение: {mines[0]["name"]}', reply_markup=create_kb_menu(user['name_deposit']))
        else:
            await bot.edit_message_text(text='❌<b>Данное месторожедние еще не открыто</b>❌\n'
                                             f'Цена: {mines[0]["price"]}{LEXICON_PROFILE["price"]}',
                                  chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                  reply_markup=create_inline_kb(1, f'shop_{callback.data.split("_")[-1]}_', '🔑Открыть', '🔙Отмена'))
    elif callback.data.split('_')[-1] == mines[1]['name']:
        if mines[1]['availability'] == 1:
            await name_mines_up(callback.from_user.id, mines[1]['name'])
            user = await db_user(callback.from_user.id)
            await callback.message.answer(text=f'Вы перешли на месторождение: {mines[1]["name"]}', reply_markup=create_kb_menu(user['name_deposit']))
        else:
            await bot.edit_message_text(text='❌<b>Данное месторожедние еще не открыто</b>❌\n'
                                             f'Цена: {mines[1]["price"]}{LEXICON_PROFILE["price"]}',
                                        chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=create_inline_kb(1, f'shop_{callback.data.split("_")[-1]}_',
                                                                      '🔑Открыть', '🔙Отмена'))
    elif callback.data.split('_')[-1] == mines[2]['name']:
        if mines[2]['availability'] == 1:
            await name_mines_up(callback.from_user.id, mines[2]['name'])
            user = await db_user(callback.from_user.id)
            await callback.message.answer(text=f'Вы перешли на месторождение: {mines[2]["name"]}', reply_markup=create_kb_menu(user['name_deposit']))
        else:
            await bot.edit_message_text(text='❌<b>Данное месторожедние еще не открыто</b>❌\n'
                                             f'Цена: {mines[2]["price"]}{LEXICON_PROFILE["price"]}',
                                        chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=create_inline_kb(1, f'shop_{callback.data.split("_")[-1]}_',
                                                                      '🔑Открыть', '🔙Отмена'))
    elif callback.data.split('_')[-1] == mines[3]['name']:
        if mines[3]['availability'] == 1:
            await name_mines_up(callback.from_user.id, mines[3]['name'])
            user = await db_user(callback.from_user.id)
            await callback.message.answer(text=f'Вы перешли на месторождение: {mines[3]["name"]}', reply_markup=create_kb_menu(user['name_deposit']))
        else:
            await bot.edit_message_text(text='❌<b>Данное месторожедние еще не открыто</b>❌\n'
                                             f'Цена: {mines[3]["price"]}{LEXICON_PROFILE["price"]}',
                                        chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=create_inline_kb(1, f'shop_{callback.data.split("_")[-1]}_',
                                                                      '🔑Открыть', '🔙Отмена'))
    elif callback.data.split('_')[-1] == mines[4]['name']:
        if mines[4]['availability'] == 1:
            await name_mines_up(callback.from_user.id, mines[4]['name'])
            user = await db_user(callback.from_user.id)
            await callback.message.answer(text=f'Вы перешли на месторождение: {mines[4]["name"]}', reply_markup=create_kb_menu(user['name_deposit']))
        else:
            await bot.edit_message_text(text='❌<b>Данное месторожедние еще не открыто</b>❌\n'
                                             f'Цена: {mines[4]["price"]}{LEXICON_PROFILE["price"]}',
                                        chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                        reply_markup=create_inline_kb(1, f'shop_{callback.data.split("_")[-1]}_',
                                                                      '🔑Открыть', '🔙Отмена'))

@router.callback_query(Text(startswith='shop_'))
async def mines_buy(callback: CallbackQuery):
    if callback.data.split('_')[-1] == '🔑Открыть':
        user = await db_user(callback.from_user.id)
        mines = await mines_user(callback.from_user.id)
        if callback.data.split('_')[1] == mines[0]['name']:
            if mines[0]['price'] <= user['balanc']:
                await user_balanc_up(callback.from_user.id, -mines[0]['price'])
                await user_price_mines(callback.data.split('_')[1], callback.from_user.id)
                await callback.message.answer(text=f"✅ Месторождение {mines[0]['name'][:-1]} открыто✅",
                                              reply_markup=create_kb_menu(user['name_deposit']))
            else:
                await callback.message.answer(text='❌Покупка не совершена! Не хватает средств❌')

        elif callback.data.split('_')[1] == mines[1]['name']:
            if mines[1]['price'] <= user['balanc']:
                await user_balanc_up(callback.from_user.id, -mines[1]['price'])
                await user_price_mines(callback.data.split('_')[1], callback.from_user.id)
                await name_mines_up(callback.from_user.id, mines[1]['name'][:-1]+'✅')
                user = await db_user(callback.from_user.id)
                await callback.message.answer(text=f"✅ Месторождение {mines[1]['name'][:-1]} открыто✅",
                                              reply_markup=create_kb_menu(user['name_deposit']))

            else:
                await callback.message.answer(text='❌Покупка не совершена! Не хватает средств❌')

        elif callback.data.split('_')[1] == mines[2]['name']:
            if mines[2]['price'] <= user['balanc']:
                await user_balanc_up(callback.from_user.id, -mines[2]['price'])
                await user_price_mines(callback.data.split('_')[1], callback.from_user.id)
                await name_mines_up(callback.from_user.id, mines[2]['name'][:-1] + '✅')
                user = await db_user(callback.from_user.id)
                await callback.message.answer(text=f"✅ Месторождение {mines[2]['name'][:-1]} открыто✅",
                                              reply_markup=create_kb_menu(user['name_deposit']))

            else:
                await callback.message.answer(text='❌Покупка не совершена! Не хватает средств❌')

        elif callback.data.split('_')[1] == mines[3]['name']:
            if mines[3]['price'] <= user['balanc']:
                await user_balanc_up(callback.from_user.id, -mines[3]['price'])
                await user_price_mines(callback.data.split('_')[1], callback.from_user.id)
                await name_mines_up(callback.from_user.id, mines[3]['name'][:-1] + '✅')
                user = await db_user(callback.from_user.id)
                await callback.message.answer(text=f"✅ Месторождение {mines[3]['name'][:-1]} открыто✅",
                                              reply_markup=create_kb_menu(user['name_deposit']))

            else:
                await callback.message.answer(text='❌Покупка не совершена! Не хватает средств❌')

        elif callback.data.split('_')[1] == mines[4]['name']:
            if mines[4]['price'] <= user['balanc']:
                await user_balanc_up(callback.from_user.id, -mines[4]['price'])
                await user_price_mines(callback.data.split('_')[1], callback.from_user.id)
                await name_mines_up(callback.from_user.id, mines[4]['name'][:-1] + '✅')
                user = await db_user(callback.from_user.id)
                await callback.message.answer(text=f"✅ Месторождение {mines[4]['name'][:-1]} открыто✅",
                                              reply_markup=create_kb_menu(user['name_deposit']))

            else:
                await callback.message.answer(text='❌Покупка не совершена! Не хватает средств❌')

    else:
        mines = await mines_user(callback.from_user.id)
        await bot.edit_message_text(text='Выбирите месторождение', chat_id=callback.from_user.id, message_id=callback.message.message_id,
                                    reply_markup=create_inline_kb(1, 'mines_choice_', mines[0]['name'],
                                                             mines[1]['name'],
                                                             mines[2]['name'],
                                                             mines[3]['name'],
                                                             mines[4]['name']))