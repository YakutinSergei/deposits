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
                                                                        availability INTEGER NOT NULL,
                                                                        stock INTEGER NOT NULL);''')

        await conn.execute('''CREATE TABLE IF NOT EXISTS workers(id BIGSERIAL NOT NULL PRIMARY KEY,
                                                                            user_id INTEGER NOT NULL,
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
                                                VALUES($1, $2, $3, 1000, 0, 0, 0, 0)''',
                                                user_id, login, LEXICON_MINES['natural_gas'])

        mines = ['⛽️Природный газ✅', '☢️Уран❌', '🪨Уголь❌', '🛢Нефть❌', '🟡Золото❌']
        price = [0, 22000, 435000, 3120000, 36000000]
        workers = ['Слесарь', 'Рабочий', 'Специалист', 'Инженер', 'Руководитель']
        workers_price = [100, 480, 2700, 8300, 33000]
        efficiency = [10, 50, 300, 1000, 5000]

        for i in range(len(mines)):
            if i == 0:
                availability = 1
            else:
                availability = 0
            await conn.execute('''INSERT INTO deposits_user(user_id, name, price, availability, stock) 
                                                        VALUES($1, $2, $3, $4, 0)''',
                                                         user_id, mines[i], price[i], availability)
            for j in range(len(workers)):
                await conn.execute('''INSERT INTO workers(user_id, name, price, efficiency, sum, lvl, name_deposit) 
                                                                        VALUES($1, $2, $3, $4, 0, 1, $5)''',
                                   user_id, workers[j], workers_price[j], efficiency[j], mines[i][:-1])
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
        user = await conn.fetchrow(f'SELECT * FROM users WHERE user_id = {user_id}')
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return user
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


#Запрос всех рабочих
async def workers_user(user_id):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        mines = await conn.fetch(f'SELECT * FROM deposits_user WHERE user_id = {user_id}')

        workers_1 = await conn.fetch(f"SELECT * FROM workers WHERE user_id = {user_id} and name_deposit='{mines[0]['name'][:-1]}'")
        workers_2 = await conn.fetch(f"SELECT * FROM workers WHERE user_id = {user_id} and name_deposit='{mines[1]['name'][:-1]}'")
        workers_3 = await conn.fetch(f"SELECT * FROM workers WHERE user_id = {user_id} and name_deposit='{mines[2]['name'][:-1]}'")
        workers_4 = await conn.fetch(f"SELECT * FROM workers WHERE user_id = {user_id} and name_deposit='{mines[3]['name'][:-1]}'")
        workers_5 = await conn.fetch(f"SELECT * FROM workers WHERE user_id = {user_id} and name_deposit='{mines[4]['name'][:-1]}'")
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            return workers_1, workers_2, workers_3, workers_4, workers_5
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

# Пополнение склада
async def mines_stock_up(user_id, name, volume):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        await conn.fetchrow(f'UPDATE deposits_user SET stock=$1 WHERE user_id=$2 and name=$3', volume, user_id, name)
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')

# Обновление full склада
async def user_stock_up(user_id, stock):
    try:
        conn = await asyncpg.connect(user=env('user'),  password=env('password'), database=env('db_name'), host=env('host'))
        await conn.fetchrow(f'UPDATE users SET full_warehouse=$1 WHERE user_id=$2', stock, user_id)
    except Exception as _ex:
        print('[INFO] Error ', _ex)

    finally:
        if conn:
            await conn.close()
            print('[INFO] PostgresSQL closed')