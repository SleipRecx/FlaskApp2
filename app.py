# import's
from flask import Flask, render_template,url_for,redirect, request, session, flash, g
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy 
from config import *

# create the application object
app = Flask(__name__)


# config's for the app
import os
app.config.from_object(os.environ['APP_SETTINGS'])
print os.environ['APP_SETTINGS']


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
            flash('You are already logged in')
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


def registerNewUser(username,password):
	txt_file=open("users.txt",'a')
	txt_file.write(username+","+password+"\n")
	txt_file.close()

def containsUsername(username):
	usernameList=[]
	txt_file = open('users.txt','r')
	lines =txt_file.readlines()
	txt_file.close()
	for line in lines:
		if(any(c.isalpha() for c in line)):
			usernameList.append(line.split(",")[0].rstrip())
	for thisUsername in usernameList:
		if (thisUsername==username):
			return True
	return False

def isValidUsernameAndPassword(username,password):
	usernameList=[]
	passwordList=[]
	txt_file = open('users.txt','r')
	lines =txt_file.readlines()
	txt_file.close()
	for line in lines:
		if(any(c.isalpha() for c in line)):
			usernameList.append(line.split(",")[0].rstrip())
			passwordList.append(line.split(",")[1].rstrip())
	for i in range(0,len(usernameList)):
		if(usernameList[i]==username):
			for j in range(0,len(passwordList)):
				if(passwordList[j]==password and i==j):
					return True
	return False



# routing for different paths
@app.route('/')
@login_required
def homepage():
	title="Welcome To My HomePage"
	paragraph="This is the main site"
	posts=db.session.query(BlogPost).all()
	return render_template("index.html",title=title,posts=posts,paragraph=paragraph)


@app.route('/post', methods = ['GET', 'POST'])
@login_required
def post():
	if request.method=='POST':
		title = request.form['title'].rstrip()
		description = request.form['description'].rstrip()
		from models import BlogPost
		db.session.add(BlogPost(title,description))
		db.session.commit()
		print(title)
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
	session.pop("logged_in",None)
	flash("You are now logged out")
	return redirect(url_for('login'))



@app.route('/register', methods = ['GET', 'POST'])
def register():
	buttonValue="Register"
	error=None
	if request.method=="POST":
		username = request.form['username'].rstrip()
		password= request.form['password'].rstrip()
		if(containsUsername(username)==False):
			registerNewUser(username,password)
			flash("Registration succeeded")
			return redirect(url_for('login'))
		else:
			error="That username is already taken"
	return render_template('login.html', error=error,buttonValue=buttonValue)




# run the application
if __name__ == "__main__":
    app.run()

