from flask import Flask, render_template, request
import sqlite3
from db_helper import DB_Helper

app = Flask(__name__)

@app.route('/')
def home():
    data = DB_Helper.get_all()
    return render_template('home.html',data=data)

@app.route('/add', methods=['POST'])
def add():
    data = request.form.get('userinput')

    DB_Helper.insert_item(data)
    return home()

@app.route('/clear')
def clear_db():
    DB_Helper.clear()
    return home()

















if __name__ == '__main__':
    app.run(port=5002, debug=True)
