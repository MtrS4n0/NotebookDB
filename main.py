# Imports
from db_conn import DB, DB_FILEPATH
from base_menu import MenuBase
from datetime import datetime
import hashlib

# Main program structure
class Main:
    def __init__(self) -> None:
        # program code here
        print("Program starting.")
        # 1. initialize
        self.db = DB(DB_FILEPATH)
        self.initDemoUser()
        _menu = MenuBase(self.db)
        # 2. run
        _menu.activate()
        # 3. cleanup
        self.db.close()
        print("\nProgram ending.")
        return None
    def initDemoUser(self) -> None:
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT 1 FROM user WHERE name = ?", ("demo_user",))
        if cursor.fetchone() is None:
            password = "Secret123"
            passwd_hashed = hashlib.md5(password.encode()).hexdigest()
            now = int(datetime.now().timestamp())
            user = ("demo_user", passwd_hashed, now, now)
            sql_query = "INSERT INTO user (name, password, created_at, updated_at) VALUES (?, ?, ?, ?)"
            cursor.execute(sql_query, user)
            self.db.connection.commit()
        cursor.close()

if __name__ == "__main__":
    DB.initialize(DB_FILEPATH, 'setup.sql')
    app = Main()
