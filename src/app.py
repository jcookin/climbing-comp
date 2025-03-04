# save this as app.py
from flask import Flask
from flask import request, session, redirect, url_for, render_template
import sys

import logic

app = Flask(__name__)

with app.app_context():
    logic.init()

def run():
    app.run(debug=False, use_reloader=False)

app.secret_key = '[poasjdflkj1yt7289340-_()'

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error), 500

@app.route("/")
def root():
    if request.cookies.get('username') in session['username']:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route("/home", methods=['GET', 'POST'])
def home():
    error = None
    routes = logic.get_routes()
    if not routes:
        error = "No routes found"
    return render_template('home.html', username=session['username'], routes=routes, error=error)

@app.route("/user", methods=['GET', 'POST'])
def get_user():
    return "USER: TODO"

@app.route("/routes/<route_id>", methods=['GET', 'POST'])
def routes(route_id: int):
    error = None
    route_info, error = logic.get_route_by_id(route_id=route_id)
    
    # Likely a no route for ID error
    if error:
        return render_template('routes.html', route_info={}, user_info={}, error=error)
    
    user = session['username']
    user_info, error = logic.get_user_info_for_route_id(username=user, route_id=route_id)
    if error:
        return render_template('routes.html', route_info={}, user_info={}, error=error)
    
    # user_info = {"username": "123test321", "attempts": "66", "sent": 0}
    # route_info = {"route_id": 3, "route_name": "whoa there pardner", "route_grade": 5}
    return render_template('routes.html', route_info=route_info, user_info=user_info, error=error)

@app.route("/routes/create", methods=['GET', 'POST'])
def create_route():
    error = None
    id = None
    status = None
    if request.method == 'POST':
        route_name = str(request.form['route_name'])
        route_grade = int(request.form['route_grade'])
        creating_user = session['username']

        existing_id, error = logic.check_route_exists(route_name)
        # route already exists, provide link
        if existing_id and error:
            error = 'Route already exists'
            id = existing_id
            status = None
        
        id, error = logic.add_route(route_name=route_name, route_grade=route_grade, creating_user=creating_user)
        if id:
            status = "OK - Route created"
    if status:
        return render_template('create_route.html', route_id=id, route_name=request.form['route_name'], status=status)
    return render_template('create_route.html', error=error)

@app.route("/logout", methods=['POST'])
def logout():
    user = request.form['username']
    session.pop(request.args[user])
    return redirect(url_for('index'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    respcode = None
    if request.method == 'POST':
        print('POST HERE')
        username = str(request.form['username'])
        password = str(request.form['password'])
        user_code = str(request.form['register_code'])

        # Check register code is valid
        if not logic.validate_registration_code(user_code):
            return render_template('register.html', error='Invalid registration code'), 400
        # Check if user already exists
        elif logic.check_user_exists(username):
            return render_template('register.html', error='Username already exists'), 400
        # Check password length
        elif len(password) < 8:
            print(f"password too short for registering user {username}")
            return render_template('register.html', error='Password must be 8+ characters'), 400
        # create user, then redirect to the home page
        print("all registration checks passed")
        if logic.create_user(username=username, hashed_password=logic.hash_password(password=password)):
            print(f"User '{username}' successfully created")
            session['username'] = username
            # session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            error = 'Unable to create user'
            respcode = 500
    return render_template('register.html', error=error), respcode

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        ok, error = logic.validate_login(username, password)
        if ok:
            session['username'] = username
            # session['logged_in'] = True
            return redirect(url_for('home'))
    # if request is GET or the credentials were invalid
    return render_template('login.html', error=error)
