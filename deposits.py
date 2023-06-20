import asyncio
import logging
from aiogram.types import BotCommand
from environs import Env
from create_bot import bot, dp
from data_base.base import db_connect
from handlers import user_handl, other_handl
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers import apsheduler

env = Env()

# Инициализируем логгер
logger = logging.getLogger(__name__)


async def set_main_menu():
    # Создаем список с командами и их описанием для кнопки menu
    main_menu_commands = [
        BotCommand(command='/profile',
                   description='Профиль'),
        BotCommand(command='/shop',
                   description='Магазин')]

    await bot.set_my_commands(main_menu_commands)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    # Подключаемся к базе данных
    await db_connect()

    # scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    # scheduler.add_job(apsheduler.warehouse_add, trigger='interval', seconds=5, kwargs={'bot':bot})
    # scheduler.start()

    # # Регистриуем роутеры в диспетчере
    dp.include_router(user_handl.router)
    # dp.include_router(admin_handlers.router)
    dp.include_router(other_handl.router)


    # Пропускаем накопившиеся апдейты и запускаем polling
    dp.startup.register(set_main_menu)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
