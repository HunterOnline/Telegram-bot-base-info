import logging
import sqlite3


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db
        self.buf_data = dict()

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_question_answer(self):
        sql = """
        CREATE TABLE QuestionAnswer(
            question varchar(2000) NOT NULL,
            answer varchar(2000) NOT NULL,
            PRIMARY KEY (question)
            );
"""
        self.execute(sql, commit=True)

    def add_question_answer(self, question: str, answer: str):
        sql = """
               INSERT INTO QuestionAnswer(question, answer) VALUES(?,?)
               """
        parameters = (question, answer)
        self.execute(sql, parameters=parameters, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def count_question_answer(self):
        return self.execute("SELECT COUNT(*) FROM QuestionAnswer;", fetchall=True)

    def update_question_answer(self, answer, question):
        sql = """
                       UPDATE QuestionAnswer SET answer=? WHERE question=?
                       """
        return self.execute(sql, parameters=(answer, question), commit=True)

    def select_all_sets(self):
        sql = """
        SELECT * FROM QuestionAnswer
        """
        return self.execute(sql, fetchall=True)

    def delete_question_answer(self, question):
        self.execute("""DELETE FROM QuestionAnswer WHERE question=?""", (question,), commit=True)

    def unload_data(self):

        self.buf_data = dict(self.select_all_sets())
        logging.info('Ebash_Bot unload_data -> successfully')


def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
