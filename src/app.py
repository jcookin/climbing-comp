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
    if not check_user_session():
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route("/home", methods=['GET', 'POST'])
def home():
    if not check_user_session():
        return redirect(url_for('login'))
    error = None
    routes = logic.get_routes()
    if not routes:
        error = "No routes found"
    return render_template('home.html', routes=routes, error=error)

@app.route("/user", methods=['GET', 'POST'])
def get_user():
    return "USER: TODO"

@app.route("/routes/<route_id>", methods=['GET', 'POST'])
def routes(route_id: int):
    if not check_user_session():
        return redirect(url_for('login'))
    error = None
    route_info, error = logic.get_route_by_id(route_id=route_id)
    user = session['username']
    
    # Handle form/button actions
    if request.method == 'POST':
        print(request.form)
        print("FORM ABOVE")
        if 'attempt' in request.form:
            print(f"Incrementing attempts on route {route_id} for user {user}")
            logic.add_route_attempt(user, route_id)
            # user_info['attempts'] = user_info['attempts'] + 1
        if 'sent' in request.form:
            print(f"Marking route as sent for user {user}")
            logic.mark_route_sent(session['username'], route_id)
            # user_info['sent'] = 1

    # Likely a no route for ID error
    if error:
        return render_template('routes.html', route_info={}, user_info={}, error=error)
    
    user_info, error = logic.get_user_info_for_route_id(username=user, route_id=route_id)
    if error:
        return render_template('routes.html', route_info={}, user_info={}, error=error)
    
    # user_info = {"username": "123test321", "attempts": "66", "sent": 0}
    # route_info = {"route_id": 3, "route_name": "whoa there pardner", "route_grade": 5}
    return render_template('routes.html', route_info=route_info, user_info=user_info, error=error)

@app.route("/routes/create", methods=['GET', 'POST'])
def create_route():
    if not check_user_session():
        return redirect(url_for('login'))
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
    print(f"Logging out user: {session['username']}")
    session.pop('username')
    return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    respcode = None
    if request.method == 'POST':
        print('request.form')
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
        err = logic.create_user(username=username, hashed_password=logic.hash_password(password=password))
        if not err:
            print(f"User '{username}' successfully created")
            session['username'] = username
            # session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            error = f'Unable to create user with error: {err}'
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

def check_user_session() -> bool:
    print("Checking if user has active logged in session")
    if 'username' not in session.keys():
        print("no user session found")
        return False
    return True