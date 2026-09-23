from model_user import UserDAO
from menu_login import User
from datetime import datetime
from menu_note import MenuNote
import hashlib

class MenuBase:
    def __init__(self, db) -> None:
        self.db = db
        return None
    def showOptions(self) -> None:
        print("Options:")
        print("1 - Login")
        print("2 - Register")
        print("0 - Exit")
        return None
    def askChoice(self) -> int:
        choice: int = -1
        feed = input("Your choice: ")
        if feed.isdigit():
            choice = int(feed)
        return choice
    def activate(self) -> None:
        while True:
            self.showOptions()
            choice = self.askChoice()
            if choice == 0:
                break
            elif choice == 1:
                self.login()
            elif choice == 2:
                self.register()
            else:
                print("Unknown option.")
        return None
    
    def login(self) -> None:
        print("Insert credentials below:")
        name = input("Insert username: ")
        passwd = input("Insert password: ")
        user = User.userLogin(self.db, name, passwd)
        if user is None:
            print("Failed to authenticate!")
            print("")
        else:
            user_id, name = user
            print("Authenticated!\n")
            _menu = MenuNote(user_id, name)
            _menu.activate()
        return None
    def register(self) -> None:
        try:
            ask_user = input("Insert username: ")
            name = UserDAO.validUser(ask_user)
            if name is None:
                raise ValueError
            ask_passwd = input("Insert password: ")
            password = UserDAO.validPassword(ask_passwd)
            if password is None:
                raise ValueError
            cursor = self.db.connection.cursor()
            passwd_hashed = hashlib.md5(password.encode()).hexdigest()
            # passwd_hashed = hashlib.sha-256(password.encode()).hexdigest()
            now = int(datetime.now().timestamp())
            user = (name, passwd_hashed, now, now)
            sql_query = "INSERT INTO user (name, password, created_at, updated_at) VALUES (?, ?, ?, ?)"
            cursor.execute(sql_query, user)
            self.db.connection.commit()
            cursor.close()
            print("Registration completed!\n")
        except ValueError as e:
            print(e)
        return None