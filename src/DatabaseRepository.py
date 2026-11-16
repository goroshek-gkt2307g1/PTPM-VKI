import sqlite3

from .DatabaseInterface import DatabaseInterface

class DatabaseRepository(DatabaseInterface):
    
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS comments (id INTEGER, name TEXT NOT NULL CHECK(length(name) <= 256), message TEXT NOT NULL CHECK(length(message) <= 8096), PRIMARY KEY(id))")
        self.conn.commit() 
    
    def get_by_id(self, comment_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, message FROM comments WHERE id=?", (comment_id,))
        res = cursor.fetchone()
        return dict(res) if res else None

    def get_by_name(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, message FROM comments WHERE name=?", (username,))
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
    
    def add(self, comment_id, username, message):
        cursor = self.conn.cursor()
        if not (isinstance(comment_id, int)): 
            raise TypeError("Id некорректный")

        if not (isinstance(username, str)):
            raise TypeError("Логин неправильного типа")
        
        if (len(username) > 256):
            raise ValueError("Логин не больше 256")
                
        if not (isinstance(message, str)): 
            raise TypeError("Сообщение неправильного типа")

        if (len(message) > 8096):
            raise ValueError("Сообщение не больше 8096")

        cursor.execute("INSERT INTO comments (id, name, message) VALUES (?, ?, ?)", (comment_id, username, message))
        self.conn.commit()
        return True


    def update(self, comment_id, new_message):
        cursor = self.conn.cursor()
        
        if (isinstance(comment_id, int)):
            if not (isinstance(new_message, str)):
                raise TypeError("Неверный тип нового сообщения")

            if (len(new_message) > 8096):
                raise ValueError("Некорректное новое сообщение")
            cursor.execute("UPDATE comments SET message=? WHERE id=?", (new_message, comment_id,))
            if (cursor.rowcount == 0):
                return False
            self.conn.commit()
            return True
        else: raise TypeError("id некорретный")

            
    def delete(self, comment_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM comments WHERE id=?", (comment_id,))
        if (cursor.rowcount == 0):
            return False
        self.conn.commit()
        return True

    def close(self):
        self.conn.close()