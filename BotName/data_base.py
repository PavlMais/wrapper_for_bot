import asyncio
import asyncpg
import config


class DataBase(object):

    @classmethod
    async def connect(cls):
        self = DataBase()
        self.pool = await asyncpg.create_pool(config.DB_URL)
        return self

    def conn(func):
        async def decor(self, *args, **kwargs):
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    return await func(self, conn = conn, *args, **kwargs)

        return decor

    
    @conn
    async def create_user(self, conn, user_id):
        await conn.execute('INSERT INTO users (id) VALUES ($1);', user_id)


    @conn
    async def get_msg_id(self, conn, user_id):
        return await conn.fetchrow(f'SELECT msg_id FROM users WHERE id = {user_id}')


    @conn
    async def set_msg_id(self, conn, user_id, msg_id):
        await conn.execute(f'UPDATE users SET msg_id = {msg_id} where id = {user_id};')

    @conn  
    async def user_exist(self, conn, user_id):
        return bool(await conn.fetchrow('SELECT 1 FROM users WHERE id = $1', user_id))

    @conn  
    async def set_user_param(self, conn, user_id, key, value):
        return await conn.fetchrow(
            f'UPDATE users SET {key} = {value} WHERE id = {user_id};'
        )

    # и т.д.




# async def a():
#     db = await DataBase.connect()

#     print(await db.get_user(user_id = 755484))
#     # print(await db.set_user_param(user_id = id_here, key = 'key', value = 'value'))


loop = asyncio.get_event_loop()
db = loop.run_until_complete(DataBase().connect())


