import sqlite3

class DB_Helper():

    @classmethod
    def insert_item(cls,item):
        connection = sqlite3.connect('crimemap.db')
        cursor = connection.cursor()
        query = "INSERT INTO crimes (description) VALUES (?)"
        cursor.execute(query, (item,))
        connection.commit()
        connection.close()

    @classmethod
    def get_all(cls):
        connection = sqlite3.connect('crimemap.db')
        cursor = connection.cursor()
        query = "SELECT description FROM crimes"
        result = cursor.execute(query)
        data = result.fetchall()
        connection.close()
        return data

    @classmethod
    def clear(cls):
        connection = sqlite3.connect('crimemap.db')
        cursor = connection.cursor()
        query = "DELETE FROM crimes"
        cursor.execute(query)
        connection.commit()
        connection.close()
