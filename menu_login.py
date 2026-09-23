import hashlib

class User:
    def userLogin(db, name: str, password: str):
        cursor = db.connection.cursor()
        passwd_hashed = hashlib.md5(password.encode()).hexdigest()
        sql_query = "SELECT id, name FROM user WHERE name = ? AND password = ?"
        params = (name, passwd_hashed)
        cursor.execute(sql_query, params)
        user = cursor.fetchone()
        cursor.close()
        if user:
            return user
        else:
            return None
        

