import asyncpg
from asyncpg import Pool, Connection

from data.config import PG_PASS, host, PG_USER


class DatabaseUsersPG:

    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(user=PG_USER,
                                         password=PG_PASS,
                                         host=host,
                                         )
        return cls(pool)

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await  connection.fetch(command, *args)
                elif fetchval:
                    result = await  connection.fetchval(command, *args)
                elif fetchrow:
                    result = await  connection.fetchrow(command, *args)
                elif execute:
                    result = await  connection.execute(command, *args)
                return result

    async def create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS UsersPGDB(
                id SERIAL PRIMARY KEY,
                id_user BIGINT NOT NULL UNIQUE,
                ser_name varchar(255) NOT NULL
                  );
               
                 """
        await self.execute(sql, execute=True)
        print("""
_____________________________________
CREATE TABLE UserPGDB -> successfully
_____________________________________""")

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    async def select_all_sets(self):
        sql = """
        SELECT * FROM UsersPGDB
        """
        print("""
_____________________________________
SELECT * FROM UsersPGDB
_____________________________________
                """)
        return await self.execute(sql, fetch=True)

    async def select_one_set(self, id:int):
        sql = """
        SELECT * FROM UsersPGDB WHERE id=$1
        """
        print("""
_____________________________________
SELECT * FROM UsersPGDB WHERE id=$1
_____________________________________
        """)
        return await self.execute(sql, id, fetchrow=True)

    async def count(self):
        print("""
_____________________________________
SELECT COUNT(*) FROM UsersPGDB
_____________________________________
                """)
        return await self.execute("SELECT COUNT(*) FROM UsersPGDB;", fetchval=True)

    async def delete_one_set(self, id: int):
        await self.execute("""DELETE FROM UsersPGDB WHERE id=$1""", id, execute=True)

    async def add_set(self, id_user, ser_name):
        sql = """
               INSERT INTO UsersPGDB(id_user, ser_name) VALUES ($1, $2) 
               """
        print("""
________________________________________________________
INSERT INTO UsersPGDB(id_user, ser_name) -> successfully
________________________________________________________""")
        return await self.execute(sql, id_user, ser_name, fetchrow=True)
