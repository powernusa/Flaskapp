import sqlite3
import datetime

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
    def get_all_crimes(cls):
        connection = sqlite3.connect('crimemap.db')
        cursor = connection.cursor()
        query = "SELECT latitude,longitude,date,category,description FROM crimes"
        result = cursor.execute(query)
        data = result.fetchall()
        named_crimes = []
        for crime in data:
            named_crime = {
                'latitude': crime[0],
                'longitude': crime[1],
                 #'date': datetime.datetime.strftime(crime[2], '%Y-%m-%d'),
                 'date': crime[2],
                'category': crime[3],
                'description': crime[4]
            }
            named_crimes.append(named_crime)

        connection.close()
        return named_crimes


    @classmethod
    def clear(cls):
        connection = sqlite3.connect('crimemap.db')
        cursor = connection.cursor()
        query = "DELETE FROM crimes"
        cursor.execute(query)
        connection.commit()
        connection.close()

    @classmethod
    def add_crime(cls, category, date, latitude, longitude, desc):
        connection = sqlite3.connect('crimemap.db')
        cursor = connection.cursor()
        query = "INSERT INTO crimes (category, date, latitude, longitude, description) \
                    VALUES(?,?,?,?,?)"
        cursor.execute(query,(category,date,latitude,longitude,desc))
        connection.commit()
        connection.close()
