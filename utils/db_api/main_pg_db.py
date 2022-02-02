import logging

import asyncpg

from asyncpg import Pool, Connection

from data.config import PG_PASS, host, PG_USER


class DatabaseMainPG:

    def __init__(self, pool):
        self.pool: Pool = pool
        self.buf_data = dict()

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
            CREATE TABLE IF NOT EXISTS MainPGDB(
                id SERIAL PRIMARY KEY,
                question varchar(2000) NOT NULL,
                answer varchar(2000) NOT NULL
                );
                 """
        await self.execute(sql, execute=True)
        print("""
_____________________________________
CREATE TABLE MainPGDB -> successfully
_____________________________________""")

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    async def select_sets_qs_as(self):
        sql = """
        SELECT question, answer FROM MainPGDB
        """
        print("""
_____________________________________
SELECT question, answer FROM MainPGDB
_____________________________________""")
        return await self.execute(sql, fetch=True)

    async def select_all_sets(self):
        sql = """
        SELECT * FROM MainPGDB
        """
        print("""
______________________________________
SELECT * FROM MainPGDB -> successfully
______________________________________""")
        return await self.execute(sql, fetch=True)

    async def select_one_set(self, **kwargs):
        sql = """
        SELECT * FROM MainPGDB WHERE id=$1
        """
        sql, parameters = self.format_args(sql, parameters=kwargs)
        print("""
__________________________________________________
SELECT * FROM MainPGDB WHERE id=$1 -> successfully
__________________________________________________""")
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count(self):
        print("""
_____________________________________________
SELECT COUNT(*) FROM MainPGDB -> successfully
_____________________________________________""")
        return await self.execute("SELECT COUNT(*) FROM MainPGDB", fetchval=True)

    async def update(self, answer, question):
        sql = """
                       UPDATE MainPGDB SET answer=$1 WHERE question=$2
                       """
        print("""
_______________________________
UPDATE MainPGDB -> successfully
_______________________________""")
        return await self.execute(sql, answer, question, execute=True)

    async def delete_one_set(self, question):
        await self.execute("""DELETE FROM MainPGDB WHERE question=$1""", question, execute=True)
        print("""
____________________________________________
DELETE FROM MainPGDB one set -> successfully
____________________________________________""")

    async def add_set(self, question, answer):
        sql = """
               INSERT INTO MainPGDB(question, answer) VALUES ($1, $2) 
               """
        print("""
______________________________________________________
INSERT INTO MainPGDB(question, answer) -> successfully
______________________________________________________""")
        return await self.execute(sql, question, answer, fetchrow=True)

    async def unload_data(self):

        self.buf_data = dict(await self.select_sets_qs_as())
        logging.info('Ebash_Bot unload_data -> successfully')
