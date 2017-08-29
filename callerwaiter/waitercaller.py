from flask import Flask,render_template
from flask import redirect,url_for,request

# <manage logins>
# info: https://flask-login.readthedocs.io/en/latest/
from flask_login import LoginManager
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from user import User
# We have to associate each table item with an owner, so we have to
# import current_user to get the currently logged-in user's ID
from flask_login import current_user
# </manage logins>

from mockdbhelper import MockDBHelper as DBHelper
from passwordhelper import PasswordHelper
import config

app = Flask(__name__)
app.secret_key = 'tPXJY3X37Qybz4QykV+hOyUxVQeEXf1Ao2C8upz+fGQXKsM'  #used to create cookies
login_manager = LoginManager(app)   #manage logins

DB = DBHelper()
PH = PasswordHelper()

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/account")
@login_required
def account():
    tables = DB.get_tables(current_user.get_id())
    return render_template("account.html",tables=tables)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# When a user login it will call this def login() then it will call def load_user()
# this is done by the server
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    stored_user = DB.get_user(email)
    if stored_user and PH.validate_password(password,stored_user['salt'],stored_user['hashed']):
        user = User(email)
        login_user(user,remember=True)
        return redirect(url_for('account'))
    return home()

# user_loader callback
# This callback is used to reload the user object from the user id stored in the session
# It should take the unicode ID of a user, and return the correspodning user object
@login_manager.user_loader
def load_user(user_id):
    user_password = DB.get_user(user_id)   # needs to check db; seeems redundant but is important
    if user_password:
        return User(user_id)

@app.route("/logout")
def logout():
    logout_user()   # from flask_login import logout_user
    return redirect(url_for("home"))

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    pw1 = request.form.get('password')
    pw2 = request.form.get('password2')
    if not pw1 == pw2:
        return redirect(url_for('home'))
    if DB.get_user(email):
        return redirect(url_for('home'))
    salt = PH.get_salt()
    hashed = PH.get_hash(pw1 + salt)
    DB.add_user(email,salt,hashed)
    return home()

@app.route('/account/createtable', methods=['POST'])
@login_required
def account_createtable():
    tablename = request.form.get('tablenumber')
    tableid = DB.add_table(tablename, current_user.get_id())  # get_id returns email
    new_url = config.base_url + "newrequest/" + tableid
    DB.update_table(tableid, new_url)
    return redirect(url_for('account'))

@app.route('/account/deletetable')
@login_required
def account_deletetable():
    tableid = request.args.get('tableid')   #difference between request.form.get and request.args.get
    DB.delete_table(tableid)
    return redirect(url_for('account'))


if __name__ == '__main__':
    app.run(port=5003, debug=True)
