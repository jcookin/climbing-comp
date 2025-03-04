# save this as app.py
from flask import Flask
from flask import request, session, redirect, url_for, render_template

import logic

app = Flask(__name__)

with app.app_context():
    logic.init()

def run():
    app.run(debug=False, use_reloader=False)

app.secret_key = '[poasjdflkj1yt7289340-_()'

@app.route("/")
def root():
    if logic.user in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route("/home", methods=['GET', 'POST'])
def home():
    # if not session
    return render_template('home.html', username=session['username'], routes=logic.get_routes())

@app.route("/user", methods=['GET', 'POST'])
def get_user():
    return "USER: TODO"

@app.route("/routes/<route_id>", methods=['GET', 'POST'])
def routes(route_id):
    route_info = logic.get_route_by_id(route_id)
    return render_template('routes.html', about=route_info)

@app.route("/logout", methods=['POST'])
def logout():
    user = request.args['username']
    session.pop(request.args[user])
    return redirect(url_for('index'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        user_code = str(request.form['register_code'])

        # Check register code is valid
        if not logic.validate_registration_code(user_code):
            return render_template('register', error='Invalid registration code')   
        # Check if user already exists
        if not logic.check_user_exists(username):
            return render_template('register', error='Username already exists')
        # Check password length
        if len(password) < 8:
            return render_template('register', error='Password must be 8+ characters')
        # create user, then redirect to the home page
        if logic.create_user(username=username, password=logic.hash_password(password=password)):
            session['username'] = username
            # session['logged_in'] = True
            return redirect(url_for('login', username=username, password=password))
    return render_template('register.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if logic.validate_login(str(request.form['username']), str(request.form['password'])):
            session['username'] = str(request.form['username'])
            # session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            error = 'invalid login credentials'
            # return login_user(request.form['username'])
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)
