    
   ## Endpoints
   (partial listings)
   
   ```python
	@app.route('/account/createtable', methods=['POST'])
	@login_required
	def account_createtable():
		pass

	@app.route('/account/deletetable')
	@login_required
	def account_deletetable():
		tableid = request.args.get('tableid')   #difference between request.form.get and request.args.get
		pass

	@app.route("/newrequest/<tid>")
	def new_request(tid):
		if DB.add_request(tid, datetime.datetime.now()):
			return "Your request has been logged and a waiter will be with you shortly"
    return "There is already a request pending for this table. Please be patient, a waiter will be there ASAP"
   
	@app.route("/dashboard")
	@login_required
	def dashboard():
		now = datetime.datetime.now()
		requests = DB.get_requests(current_user.get_id())
		for req in requests:
			deltaseconds = (now - req['time']).seconds
			req['wait_minutes'] = "{}.{}".format((deltaseconds/60), str(deltaseconds % 60).zfill(2))
		return render_template("dashboard.html", requests=requests)
		
	@app.route("/dashboard/resolve")
	@login_required
	def dashboard_resolve():
		pass
   ```
	
   ## Files used
   (partial listings)
   
   forms.py (for upgrade): 
   ```python
    from flask_wtf import Form
    from wtforms import PasswordField
    from wtforms import SubmitField
    from wtforms.fields.html5 import EmailField
    from wtforms import TextField 
    from wtforms import validators


    class RegistrationForm(Form):
		email = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
		password = PasswordField('password', validators=[validators.DataRequired(), 
								  validators.Length(min=8, message="Please choose a password of at least 8 characters")])
		password2 = PasswordField('password2', validators=[validators.DataRequired(), 
								   validators.EqualTo('password', message='Passwords must match')])
		submit = SubmitField('submit', [validators.DataRequired()])


	class LoginForm(Form):
		loginemail = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
		loginpassword = PasswordField('password', validators=[validators.DataRequired(message="Password field is required")])
		submit = SubmitField('submit', [validators.DataRequired()]) 


    class CreateTableForm(Form):
		tablenumber = TextField('tablenumber', validators=[validators.DataRequired()])
		submit = SubmitField('createtablesubmit', validators=[validators.DataRequired()])
   ```    
   
   Excerpt from dbhelper.py:
   ```python
   import pymongo
   from bson import ObjectId  # you need this to cast string into _id object

   DATABASE = "waitercaller"

   class DBHelper:
		def __init__(self):
			client = pymongo.MongoClient()
			self.db = client[DATABASE]
			
		def get_user(self, email):
			pass

		def add_user(self, email, salt, hashed):
			pass

		def add_table(self, number, owner):
			pass

		def update_table(self, _id, url):
			pass

		def get_tables(self, owner_id):
			pass

		def get_table(self, tableid):
			pass

		def delete_table(self, table_id):
			pass

		def add_request(self, table_id, time):
			pass

		def get_requests(self, owner_id):
			pass

		def delete_request(self, request_id):
			pass
   ```
   
   ## Mongo
   
   Mongo database for callerwaiter:
   <img width="80%" border="30" src="https://user-images.githubusercontent.com/13763933/29879726-21163b82-8dd0-11e7-9457-74bc64e66867.jpg"/>
   <br><br>
   Make email in users table unique. Also make table_id in requests table unique.<br>
   create_mongo_indices.py:
   
   ```python
	import pymongo
	
	client = pymongo.MongoClient()
	c = client['waitercaller']
	print c.users.create_index("email", unique=True)
	print c.requests.create_index("table_id", unique=True)
   ```
   ## Essential Bootstrap Format
   Download link: <a href="http://getbootstrap.com/docs/3.3/getting-started/#download">Bootstrap v3.3.7</a>
   <br>
   
   base.html: <br>
   <img width="80%" border="30" src="https://user-images.githubusercontent.com/13763933/29750689-766c91e4-8b6e-11e7-8c27-8fe4cdbb7429.jpg"/>
   <br><br><br>
   home.html:<br>
   <img width="80%" border="30" src="https://user-images.githubusercontent.com/13763933/29750746-9382e340-8b6f-11e7-9072-fffdad2908c6.jpg"/>
   <br>
   account.html:<br>
   <img width="80%" border="30" src="https://user-images.githubusercontent.com/13763933/29750748-95bd7c38-8b6f-11e7-998f-6afc01132963.jpg"/>
   <br>
   dashboard.html:<br>
   <img width="80%" border="30" src="https://user-images.githubusercontent.com/13763933/29835761-28621f40-8d1d-11e7-9cf9-743769fb3b84.jpg"/>
   <br>
   
   ```
    <head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		{% block metarefresh %} {% endblock %}
		<title>Waiter Caller</title>

		<!-- Bootstrap core CSS -->
		<link href="../static/css/bootstrap.min.css" rel="stylesheet">
		<link rel="shortcut icon" href="{{url_for('static',filename='favicon.ico')}}">
    </head>
	==========
	{% block navbar %}
		<nav class="navbar navbar-inverse navbar-fixed-top">
		  <div class="container">
			<div class="navbar-header">
			  <a class="navbar-brand" href="/dashboard">Dashboard</a>
			  <a class="navbar-brand" href="/account">Account</a>
			</div>
		  </div>
		</nav>
    {% endblock %}
	==========
    {% block content %}
    {% endblock %}
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
    <script src="../static/js/bootstrap.min.js"></script>
	==========
	{% block navbar %}
		<nav class="navbar navbar-inverse navbar-fixed-top">
		  <div class="container">
			<div class="navbar-header">
			  <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="true" aria-controls="navbar">
				<span class="sr-only">Toggle navigation</span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
			  </button>
			  <a class="navbar-brand" href="#">Home</a>
			</div>
			<div id="navbar" class="navbar-collapse collapse">
			  <form class="navbar-form navbar-right" action="/login" method="POST">
				<div class="form-group">
				  <input type="text" name="email" placeholder="Email" class="form-control" autofocus>
				</div>
				<div class="form-group">
				  <input type="password" name="password" placeholder="Password" class="form-control">
				</div>
				<input type="submit" value="Sign in" class="btn btn-success">
			  </form>
			</div><!--/.navbar-collapse -->
		  </div>
		</nav>
	{% endblock %}
	==========
	{% block content %}
    <div class="jumbotron">
      <div class="container">
        <h1>Waiter Caller</h1>
        <p>Your patrons can call their waiter anytime, using only their phone</p>
      </div>
    </div>
    <div class="container">
      <div class="row">
        <div class="col-md-4">
          <h2>Simple</h2>
          <p>Just print out the URLs and put them on the tables of your restaurant. No specialized hardware required. </p>
        </div>
        <div class="col-md-4">
          <h2>Cost effective</h2>
          <p>No need to buy hardware either for your tables or for your kitchen. Management and usage all directly from this page.</p>
       </div>
        <div class="col-md-4">
          <h2>Register now</h2>
             <form class="form-horizontal" action="/register" method="POST">
                <div class="form-group">
                    <div class="col-sm-9">
                        <input type="email" name="email" id="email" placeholder="Email address" class="form-control">
                    </div>
                </div>
                <div class="form-group">
                    <div class="col-sm-9">
                        <input type="password" name="password" id="password" placeholder="Password" class="form-control">
                    </div>
                </div>
                <div class="form-group">
                    <div class="col-sm-9">
                        <input type="password" name="password2" id="password2" placeholder="Confirm password" class="form-control">
                    </div>
                </div>

                <div class="form-group">
                    <div class="col-sm-9">
                        <input type="submit" value="Register" class="btn btn-primary btn-block">
                    </div>
                </div>
            </form> <!-- /form -->
        </div>
      </div>
    </div>
    {% endblock %}
    ==========
    <div class="jumbotron">
      <div class="container">
        <h1>Account</h1>
        <p>Manage tables and get URLs</p>
      </div>
    </div>
	==========
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h2>Add new table</h2>
          <form class="form-inline" action="/account/createtable" method="POST">
            <div class="form-group">
              <input type="text" name="tablenumber" placeholder="Table Name or number"  class="form-control" >
              <input type="submit" value="Create" class="btn btn-primary">
            </div>
          </form>
        </div>
      </div>
    </div>
	==========
	<div class="container">
      <div class="row">
        <div class="col-md-12">
          <h2>Tables</h2>
              <table class="table table-striped">
                <tr>
                  <th>No.</th>
                  <th>URL</th>
                  <th>Delete</th>
                </tr>
                {% for table in tables %}
                <form class="form-inline" action="/account/deletetable">
                    <tr>
                      <td>{{table.number}}</td>
                      <td>{{table.url}}</td>
                      <td> <input type="submit" value="Delete" class="form-control"></td>
                      <input type="text" name="tableid" value="{{table._id}}" hidden>
                    </tr>
                </form>
                {% endfor %}
              </table>
        </div>
      </div>
    </div>
	==============
	dashboard.html
	===============
	{% extends "base.html" %}
	{% block metarefresh %} <meta http-equiv="refresh" content="10" > {% endblock %}
	{% block content %}
		<div class="jumbotron">
		  <div class="container">
			<h1>Dashboard</h1>
			<p>View all patron requests below</p>
		  </div>
		</div>
		.................................................
		..................................................
	{% endblock %}
   ```
   
	 ## Appendix