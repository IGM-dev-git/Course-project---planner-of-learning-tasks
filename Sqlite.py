from multiprocessing import connection
import sqlite3 as bd


class Database:

    # Конструктор 
    def __init__(self):
        self.connection = bd.connect('database.db')
        self.cursor = self.connection.cursor()

        # Создаем таблицу, если она не существует
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                chat_id TEXT PRIMARY KEY,
                status TEXT,
                login TEXT,
                password TEXT)
        ''')

        self.connection.commit() # Подтверждаем изменения в бд

    # ----- Методы взаимодействия с БД -----

    # Метод добавления записи в БД
    def AddUserData(self, chat_id, status = 'logged_out', login = None, password = None):
        self.cursor.execute(''' 
            INSERT OR REPLACE INTO users
            (chat_id,status, login, password)
            VALUES (?, ?, ?, ?)
        '''), (chat_id, status, login, password)
        self.connection.commit()

    # Метод получения статуса пользователя
    def GetUserStatus(self, chat_id):
        self.cursor.execute(''' 
        SELECT status FROM users WHERE chat_id = ?
        ''', (chat_id))
        result = self.cursor.fetchone()
        return result[0] if result else None

    # Метод получения всех данных пользователя 
    def GetAllUserData(self, chat_id):
        self.cursor.execute(''' 
            SELECT login, password FROM users WHERE chat_id = ?
        ''', (chat_id))
        result = self.cursor.fetchone()
        if result: 
            return {
                'login' : result[0],
                'password' : result[1]
            }
        else:
            return None

    # Метод удаления пользователя
    def RemoveUser(self, chat_id):
        self. cursor.execute('''
        DELETE FROM users WHERE chat_if = ?
       ''', (chat_id))

    # Метод закрытия БД
    def close(self):
        self.connection.close()





