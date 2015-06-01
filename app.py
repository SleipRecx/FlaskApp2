from flask import Flask, render_template,url_for,redirect, request, session, flash, g
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key="secret"

##database
app.database="saple.db"


def connect_db():
	return sqlite3.connect(app.database)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login to access')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required
def homepage():
	posts=[]
	try:
		title="Welcome To My HomePage"
		paragraph="This is the main site"
		pageType="main"
		#fetching data from database and placing it in a dictionary
		g.db=connect_db()
		data = g.db.execute('select * from posts')
		posts_dict={}
		for item in data.fetchall():
			posts_dict["title"]=item[0]
			posts_dict["description"]=item[1]
			posts.append(posts_dict)
			posts_dict={}
		g.db.close()
	except sqlite3.OperationalError:
		flash("You have noe database")
	return render_template("index.html",title=title,posts=posts,paragraph=paragraph,pageType=pageType)


@app.route('/about')
def aboutpage():
	return render_template("about.html")

@app.route('/login', methods = ['GET', 'POST'])
def login():
	buttonValue="Login"
	error=None
	if request.method=='POST':
		username = request.form['username'].rstrip()
		password= request.form['password'].rstrip()
		if(isValidUsernameAndPassword(username,password)):
			session['logged_in']=True
			flash('You are now logged in')
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
			return redirect(url_for('login'))
		else:
			error="That username is already taken"
	return render_template('login.html', error=error,buttonValue=buttonValue)


## Methods used for website behavouir
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


if __name__ == "__main__":
    app.run(debug=True)

