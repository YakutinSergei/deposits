import asyncpg

from environs import Env

from lexicon.lexicon_ru import LEXICON_MINES

#from lexicon.lexicon_ru import LEXICON_CARD_RARE

env = Env()
env.read_env()


async def db_connect():
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        await conn.execute('''CREATE TABLE IF NOT EXISTS users(user_id BIGSERIAL NOT NULL PRIMARY KEY,
                                                                login VARCHAR(50),
                                                                name_deposit VARCHAR(50) NOT NULL,
                                                                volume_warehouse INTEGER NOT NULL,
                                                                full_warehouse INTEGER NOT NULL,
                                                                rating INTEGER NOT NULL,
                                                                pg INTEGER NOT NULL,
                                                                balanc INTEGER NOT NULL);''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS deposits_user(id BIGSERIAL NOT NULL PRIMARY KEY,
                                                                        user_id INTEGER NOT NULL,
                                                                        name VARCHAR(50)NOT NULL,
                                                                        price INTEGER NOT NULL,
                                                                        availability INTEGER NOT NULL);''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS workers(id BIGSERIAL NOT NULL PRIMARY KEY,
                                                                            name VARCHAR(50)NOT NULL,
                                                                            price INTEGER NOT NULL,
                                                                            efficiency INTEGER NOT NULL,
                                                                            sum INTEGER NOT NULL,
                                                                            lvl INTEGER NOT NULL,
                                                                            name_deposit VARCHAR(50)NOT NULL);''')

        await conn.close()

    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')

# Добавление юзера
async def db_users_add(user_id, login):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        await conn.execute('''INSERT INTO users(user_id, login, name_deposit, volume_warehouse, full_warehouse, rating, pg, balanc) 
                                                VALUES($1, $2, $3, 100, 0, 0, 0, 0)''',
                                                user_id, login, LEXICON_MINES['natural_gas'])

        mines = ['⛽️Природный газ✅', '☢️Уран❌', '🪨Уголь❌', '🛢Нефть❌', '🟡Золото❌']
        price = [0, 22000, 435000, 3120000, 36000000]

        for i in range(len(mines)):
            if i == 0:
                availability = 1
            else:
                availability = 0
            await conn.execute('''INSERT INTO deposits_user(user_id, name, price, availability) 
                                                        VALUES($1, $2, $3, $4)''',
                                                         user_id, mines[i], price[i], availability)
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')

# Получение данных юзера
async def db_user(user_id):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        mines = await conn.fetchrow(f'SELECT * FROM users WHERE user_id = {user_id}')
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return mines
            print('[INFO] PostgresSQL closed')

# Список месторождений
async def mines_user(user_id):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        mines = await conn.fetch(f'SELECT * FROM deposits_user WHERE user_id = {user_id}')
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return mines
            print('[INFO] PostgresSQL closed')

#Обновление месторождения
async def name_mines_up(user_id, name):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        await conn.fetchrow(f'UPDATE users SET name_deposit=$1 WHERE user_id=$2', name, user_id)
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')

#Обновление баланса
async def user_balanc_up(user_id, price):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        balanc = await conn.fetchrow(f'SELECT balanc FROM users WHERE user_id = {user_id}')
        await conn.fetchrow(f'UPDATE users SET balanc=$1 WHERE user_id=$2', balanc['balanc'] + price, user_id)
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')

#Покупка месторождения
async def user_price_mines(name, user_id):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        new_name = name[:-1]+'✅'
        await conn.fetchrow(f'UPDATE deposits_user SET name=$1, availability=$4 WHERE user_id=$2 and name=$3', new_name, user_id, name, 1)
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')