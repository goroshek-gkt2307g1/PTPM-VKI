import sqlite3

class Database:
    def __init__(self, path="dbLab3.db"):
        self.connection = sqlite3.connect(path)
        self.createTable()

    def createTable(self):
        cursor = self.connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS registrations (login TEXT, password TEXT, confPassword TEXT, result TEXT, message TEXT)")
        self.connection.commit()

    def addReg(self, login, password, confPassword, result, text):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO registrations (login, password, confPassword, result, message)" \
        " VALUES (?, ?, ?, ?, ?)", (login, password, confPassword, result, text))
        self.connection.commit()

    def get(self, login, password, confPassword):
        cursor = self.connection.cursor()
        cursor.execute("SELECT result, message FROM registrations WHERE login=?" \
        " AND password=? AND confPassword=?", (login, password, confPassword))
        res = cursor.fetchone()
        return res

    def delete(self, login, password, confPassword):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM registrations WHERE login=? AND password=? AND confPassword=?",
                       (login, password, confPassword))
        self.connection.commit()

    def close(self):
        self.connection.close()


    