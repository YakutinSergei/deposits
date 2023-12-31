from aiogram.types import Message

from data_base.base import mines_user, workers_user, db_user, mines_stock_up, user_stock_up


async def warehouse_add(message: Message):
    user = await db_user(message.from_user.id)
    mines = await mines_user(message.from_user.id)
    works = await workers_user(message.from_user.id)
    warehouse_volume = mines[0]['stock'] + mines[1]['stock'] + mines[2]['stock'] + mines[3]['stock'] + mines[4]['stock'] #На сколько заполнен
    user_volume = user['volume_warehouse'] #Размер склада
    b = False
    if warehouse_volume < user_volume:
        for i in range(len(works)):
            if not b:
                volume = mines[i]['stock']
                for j in range(len(works[i])):
                    volume += mines[i]['availability']*((works[i][j]['efficiency'] * works[i][j]['sum'])/6)
                    warehouse_volume += mines[i]['availability']*((works[i][j]['efficiency'] * works[i][j]['sum'])/6)
                    if  warehouse_volume >= user_volume:
                        await message.answer(text='Склад переполнен')
                        b = True
                        volume = user_volume - (warehouse_volume - volume)
                        await mines_stock_up(message.from_user.id, mines[i]['name'], volume)
                        await user_stock_up(message.from_user.id, user_volume)
                        break
                await mines_stock_up(message.from_user.id, mines[i]['name'], volume)
                if warehouse_volume >= user_volume:
                    await user_stock_up(message.from_user.id, user_volume)
                else:
                    await user_stock_up(message.from_user.id, warehouse_volume)
            else:
                break


