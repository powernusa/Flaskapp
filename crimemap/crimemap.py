from flask import Flask, render_template, request,redirect,url_for
from db_helper import DB_Helper
import json

app = Flask(__name__)

@app.route('/')
def home():
    crimes = DB_Helper.get_all_crimes()
    crimes = json.dumps(crimes)
    return render_template('home.html',crimes=crimes)

@app.route("/submitcrime", methods=['POST'])
def submitcrime():
    category = request.form.get("category")
    date = request.form.get("date")
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    description = request.form.get("description")
    DB_Helper.add_crime(category, date, latitude, longitude, description)
    return redirect(url_for('home'))

@app.route('/clear')
def clear_db():
    DB_Helper.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(port=5003, debug=True)
