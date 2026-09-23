from dataclasses import dataclass
import sqlite3

NOTES = []

@dataclass
class Note:
    id: int
    title: str
    content: str
        
class NoteDAO:
    @staticmethod
    def addNote(user_id: int, title: str, content: str) -> None:
        sql_query = "INSERT INTO note (user_id, title, content) VALUES (?, ?, ?)"
        values = (user_id, title, content)
        try:
            conn = sqlite3.connect('notes.db')
            cursor = conn.cursor()
            cursor.execute(sql_query, values)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error while inserting note.{e}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    @staticmethod
    def getNotes(user_id: int, limit: int = -1) -> list[Note]:
        notes: list[Note] = []
        try:
            conn = sqlite3.connect('notes.db')
            cursor = conn.cursor()
            sql_query = "SELECT id, title, content FROM note WHERE user_id = ?"
            params = [user_id]
            if limit > 0:
                sql_query += " LIMIT ?"
                params.append(limit)
            cursor.execute(sql_query, params)
            records = cursor.fetchall()
            cursor.close()
            for record in records:
                note = Note(*record)
                notes.append(note)
        except sqlite3.Error as e:
            print("Error while fetching notes.")
        finally:
            if conn:
               conn.close()
        return notes

    @staticmethod
    def getOneNote(user_id: int, title: str) -> Note | None:
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        sql_query = "SELECT * FROM note WHERE user_id = ? AND title = ?"
        params = (user_id, title)
        cursor.execute(sql_query, params)
        note: Note | None = None
        result = cursor.fetchone()
        if result:
            note = Note(id=result[0], title=result[2], content=result[3])
        cursor.close()
        conn.close()
        return note
    
    @staticmethod
    def editNote(user_id: int, note: Note) -> None:
        sql_query = "UPDATE note SET content = ? WHERE id = ? AND user_id = ?"
        params = (note.content, note.id, user_id)
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute(sql_query, params)
        conn.commit()
        cursor.close()
        return None
    
    @staticmethod
    def deleteNote(user_id: int, title: str) -> int:
        sql_query = "DELETE FROM note WHERE user_id = ? AND title = ?"
        params = (user_id, title)
        conn = sqlite3.connect('notes.db')
        cursor = conn.cursor()
        cursor.execute(sql_query, params)
        conn.commit()
        rowCount = cursor.rowcount
        cursor.close()
        conn.close()
        return rowCount