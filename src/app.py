# save this as app.py
from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('home.html')

@app.route("/user", methods=["GET", "POST"])
def get_user():
    return "USER: TODO"

@app.route("/routes", methods=["GET", "POST"])
def route():
    return "ROUTES: TODO"

@app.route("/login")
def login():
    error = None
    if request.method == 'POST':
        if validate_login(request.form['username'],
                       request.form['password']):
            # return login_user(request.form['username'])
            return render_template('home.html', username="demouser123")
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

def validate_login(username, password):
    return True

def login_user():
    return "demo"
