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
                                                                sum_plumber INTEGER NOT NULL,
                                                                sum_working INTEGER NOT NULL,
                                                                sum_specialist INTEGER NOT NULL,
                                                                sum_engineer INTEGER NOT NULL,
                                                                sum_manager INTEGER NOT NULL,
                                                                volume_warehouse INTEGER NOT NULL,
                                                                full_warehouse INTEGER NOT NULL,
                                                                rating INTEGER NOT NULL,
                                                                pg INTEGER NOT NULL);''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS deposits(id BIGSERIAL NOT NULL PRIMARY KEY,
                                                                    name VARCHAR(50)NOT NULL);''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS deposits_user(id BIGSERIAL NOT NULL PRIMARY KEY,
                                                                        name VARCHAR(50)NOT NULL);''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS workers(id BIGSERIAL NOT NULL PRIMARY KEY,
                                                                            name VARCHAR(50)NOT NULL,
                                                                            price INTEGER NOT NULL,
                                                                            efficiency INTEGER NOT NULL);''')

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
        await conn.execute('''INSERT INTO users(user_id, login, name_deposit, sum_plumber, sum_working, sum_specialist, 
                                                sum_engineer, sum_manager, volume_warehouse, full_warehouse, rating, pg) 
                                                VALUES($1, $2, $3, 0, 0, 0, 0, 0, 1000, 0, 0, 0)''',
                                                user_id, login, LEXICON_MINES['natural_gas'])
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')

# Получение данных юзера
async def db_mines(user_id):
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

