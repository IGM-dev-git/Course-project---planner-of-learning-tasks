from multiprocessing import connection
import sqlite3 as bd


class Database:

    # Конструктор 
    def __init__(self):
        self.dbName = 'database.db'
        # Создаем таблицу при первом подключении
        with self._GetConnection() as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS users(
                chat_id TEXT PRIMARY KEY,
                status TEXT,
                login TEXT,
                password TEXT)
            ''')
            conn.commit() # Подтверждаем изменения в бд

    # Создание нового подключения для каждого запроса
    def _GetConnection(self):
        
        conn = bd.connect(self.dbName, check_same_thread=False)
        return conn

    # ----- Методы взаимодействия с БД -----

    # Метод добавления записи в БД
    def AddUserData(self, chat_id, status = 'logged_out', login = None, password = None):
        with self._GetConnection() as conn:
            conn.execute(''' 
                INSERT OR REPLACE INTO users
                (chat_id,status, login, password)
                VALUES (?, ?, ?, ?)
            ''', (chat_id, status, login, password))
            conn.commit()

    # Метод получения статуса пользователя
    def GetUserStatus(self, chat_id):
        with self._GetConnection() as conn:
            cursor= conn.execute(''' 
            SELECT status FROM users WHERE chat_id = ?
            ''', (chat_id,)) #Если что то убрать запятую!
            result = cursor.fetchone()
            return result[0] if result else None

    # Метод получения всех данных пользователя 
    def GetAllUserData(self, chat_id):
        with self._GetConnection() as conn:
            cursor = conn.execute(''' 
                SELECT login, password FROM users WHERE chat_id = ?
            ''', (chat_id,)) #Если что то убрать запятую!
            result = cursor.fetchone()
            if result: 
                return {
                    'login' : result[0],
                    'password' : result[1]
                }
            else:
                return None

    # Метод удаления пользователя
    def RemoveUser(self, chat_id):
        with self._GetConnection() as conn:
            conn.execute('''
            DELETE FROM users WHERE chat_id = ?
            ''', (chat_id, )) #Если что то убрать запятую!
            conn.commit()

    





