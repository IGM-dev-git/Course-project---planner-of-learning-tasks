from multiprocessing import connection
import sqlite3 as bd


class Database:

    # ����������� 
    def __init__(self):
        self.connection = bd.connect('database.db')
        self.cursor = self.connection.cursor()

        # ������� �������, ���� ��� �� ����������
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                chat_id TEXT PRIMARY KEY,
                status TEXT,
                login TEXT,
                password TEXT)
        ''')

        self.connection.commit() # ������������ ��������� � ��

    # ----- ������ �������������� � �� -----

    # ����� ���������� ������ � ��
    def AddUserData(self, chat_id, status = 'logged_out', login = None, password = None):
        self.cursor.execute(''' 
            INSERT OR REPLACE INTO users
            (chat_id,status, login, password)
            VALUES (?, ?, ?, ?)
        '''), (chat_id, status, login, password)
        self.connection.commit()

    # ����� ��������� ������� ������������
    def GetUserStatus(self, chat_id):
        self.cursor.execute(''' 
        SELECT status FROM users WHERE chat_id = ?
        ''', (chat_id))
        result = self.cursor.fetchone()
        return result[0] if result else None

    # ����� ��������� ���� ������ ������������ 
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

    # ����� �������� ������������
    def RemoveUser(self, chat_id):
        self. cursor.execute('''
        DELETE FROM users WHERE chat_if = ?
       ''', (chat_id))

    # ����� �������� ��
    def close(self):
        self.connection.close()





