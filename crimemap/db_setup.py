import sqlite3

connection = sqlite3.connect('crimemap.db')
cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS crimes (id INTEGER PRIMARY KEY AUTOINCREMENT,latitude REAL, longitude REAL, date NUMERIC, category TEXT, description TEXT,updated_at NUMERIC)"

cursor.execute(create_table)
connection.commit()
connection.close()
