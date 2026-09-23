import re
import sqlite3

class UserDAO:
    MIN_LENGTH = 4
    MAX_LENGTH = 10
    @staticmethod
    def validUser(name: str):
        conn = None
        cursor = None
        try:
            if len(name) < UserDAO.MIN_LENGTH:
                raise ValueError(f"Username must be minimum of '{UserDAO.MIN_LENGTH}' characters long.")
            elif len(name) > UserDAO.MAX_LENGTH:
                raise ValueError(f"Username must be maximum of '{UserDAO.MAX_LENGTH}' characters long.")
            elif not re.match(r'^[A-Za-z0-9_-]+$', name):
                raise ValueError("Username can only contain:\n1. Lower case characters 'a-z'\n2. Upper case characters 'A-Z'\n3. Special characters '_' and '-'")
            conn = sqlite3.connect('user.db')
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM user WHERE name = ?", (name,))
            if cursor.fetchone():
                raise ValueError("Username already exists!")
        except ValueError as e:
            print(e)
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return name

    @staticmethod
    def validPassword(password: str):
        try:
            if len(password) < UserDAO.MIN_LENGTH:
                raise ValueError(f"Password must be minimum of '{UserDAO.MIN_LENGTH}' characters long.")
            elif len(password) > UserDAO.MAX_LENGTH:
                raise ValueError(f"Password must be maximum of '{UserDAO.MAX_LENGTH}' characters long.")
            elif not re.match(r'^[A-Za-z0-9_-]+$', password):
                raise ValueError("Password can only contain:\n1. Lower case characters 'a-z'\n2. Upper case characters 'A-Z'\n3. Special characters '_' and '-'")
            check_passwd = input("Insert password again: ")
            if password != check_passwd:
               raise ValueError("Passwords do not match!")
        except ValueError as e:
            print(e)
            return None
        return password