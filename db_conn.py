# from sqlite3 import Connection
import sqlite3
from pathlib import Path
import sys


DB_FILEPATH = Path('app.db')

class DB:
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    @staticmethod
    def loadSqlScript(filepath: str) -> str:
        content = ""
        try:
            with open(filepath, 'r', encoding='UTF-8') as file:
                content = file.read()
        except Exception as e:
            print(f"Failed to read '{filepath}' file.")
            sys.exit(-1)
        return content
    
    @staticmethod
    def initialize(db_name: str, script_path:str) -> None:
        script = DB.loadSqlScript(script_path)
        connection = sqlite3.connect(db_name)
        cursor = connection.cursor()
        cursor.executescript(script)
        connection.commit()
        cursor.close()
        connection.close()

    def close(self):
        self.connection.close()