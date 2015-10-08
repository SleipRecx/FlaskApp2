# import's
from flask import Flask, render_template,url_for,redirect, request, session, flash, g
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy 
from config import *
from UserClass import Users

# create the application object
app = Flask(__name__)


# config's for the app
import os
app.config.from_object(os.environ['APP_SETTINGS'])
print "Server Restart"


#create the SQLAlchemy object
db = SQLAlchemy(app)
from models import *




# methods used for website behavouir
def logout_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You are already logged out')
            return redirect(url_for('homepage'))
    return wrap


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login to access')
            return redirect(url_for('login'))
    return wrap


def registerNewUser(username,password,isAdmin):
	if isAdmin == True:
		txt_file=open("admin.txt",'a')
	else:
		txt_file=open("users.txt",'a')
	txt_file.write(username+","+password+"\n")
	txt_file.close()


def fileToDict():
	dict_admin = {}
	dict_user= {}
	liste = list()
	for x in range(0,2):
		fil = open('users.txt','r')
		if x==1:
			fil = open('admin.txt','r')
		lines = fil.readlines()
		for line in lines:
			key = line.split(",")[0].rstrip()
			value = line.split(",")[1].rstrip()
			if x==1:
				dict_admin[key]=value	
			else:
				dict_user[key]=value
	liste.append(dict_user)
	liste.append(dict_admin)
	return liste



def containsUsername(username):
	liste = fileToDict()
	for x in range(0,len(liste)):
		for key, items in liste[x].items():
			if key == username:
				return True
	return False


def isValidUsernameAndPassword(username,password):
	liste = fileToDict()
	ADMIN_INDEX=1
	for x in range(0,len(liste)):
		for key,value in liste[x].items():
			if key == username and value == password:
				if x == ADMIN_INDEX:
					session['admin']=True
				else:
					session['admin']=False
				session['username']=username
				return True
	return False



# routing for different paths
@app.route('/')
@login_required
def homepage():
	title="Welcome To My HomePage"
	paragraph="This is the main site"
	posts=db.session.query(BlogPost).all()
	posts=reversed(posts)
	current_username = session['username']
	return render_template("index.html",posts=posts,username=current_username)


@app.route('/deleteAll')
@login_required
def delete_all():
	if session['admin']==True:
		db.create_all()
		db.session.query(BlogPost).delete()
		db.session.commit()
		flash("Wall deleted")
	else:
		flash("Only admin can delete wall")
	return redirect(url_for('homepage'))


@app.route('/post', methods = ['GET', 'POST'])
@login_required
def post():
	if request.method=='POST':
		title = request.form['title'].rstrip()
		description = request.form['description'].rstrip()
		from models import BlogPost
		db.session.add(BlogPost(title,description))
		db.session.commit()
	return redirect(url_for('homepage'))


@app.route('/about')
@login_required
def aboutpage():
	return render_template("about.html")



@app.route('/login', methods = ['GET', 'POST'])
@logout_required
def login():
	buttonValue="Login"
	error=None
	if request.method=='POST':
		username = request.form['username'].rstrip()
		password= request.form['password'].rstrip()
		if(isValidUsernameAndPassword(username,password)):
			session['logged_in']=True
			flash('You where just logged in')
			return redirect(url_for('homepage'))
		else:
			error = "invalid username or password"
	return render_template('login.html',buttonValue=buttonValue, error=error)



@app.route('/logout')
@login_required
def logout():
	session.pop("logged_in",False)
	session.pop("admin",False)
	session.pop('username',None)
	flash("You are now logged out")
	return redirect(url_for('login'))



@app.route('/register', methods = ['GET', 'POST'])
def register():
	buttonValue="Register"
	error=None
	if request.method=="POST":
		username = request.form['username'].rstrip()
		password= request.form['password'].rstrip()
		try:
			if session['admin'] == True:
				isAdmin=True
			else:
				isAdmin=False
		except KeyError:
			isAdmin=False
		if(containsUsername(username)==False):
			registerNewUser(username,password,isAdmin)
			flash("Registration succeeded")
			if isAdmin == True:
				return redirect(url_for('homepage'))	
			return redirect(url_for('login'))
		else:
			error="That username is already taken"
	return render_template('login.html', error=error,buttonValue=buttonValue)





# run the application
if __name__ == "__main__":
    app.run()


