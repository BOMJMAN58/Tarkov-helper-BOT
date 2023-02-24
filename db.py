import sqlite3


class SQLighter:

    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

    def select_all(self, id):
        """ Получаем все строки пользователя"""
        with self.connection:
            return self.cursor.execute('SELECT event FROM log WHERE id_user = ?', (id, )).fetchall()

    def add_log(self, id, event):
        """ Добавляем запись """
        with self.connection:
            return self.cursor.execute('INSERT INTO log (id_user, event) VALUES(?, ?)', (id, event, )).fetchall()

    def del_log(self, id):
        """ Удаляем историю"""
        with self.connection:
            return self.cursor.execute('DELETE FROM log WHERE id_user = ?', (id, )).fetchall()

    def close(self):
        """ Закрываем текущее соединение с БД """

        self.connection.close()
