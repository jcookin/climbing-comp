import database
import bcrypt
from typing import Tuple

def init():
    database.init_db()

def validate_login(username, password):
    if not check_user_exists(username=username):
        return False, 'Username not found'
    bpassword = password.encode('utf-8')
    hashed_password = database.get_user_password(username=username)
    if bcrypt.checkpw(password=bpassword, hashed_password=hashed_password):
        return True, None
    return False, 'Error validating credentials'

def validate_registration_code(user_code):
    print("validating user registration code")
    print(f"user code: {user_code}")
    registration_code = database.get_registration_code()
    good = user_code == registration_code
    print(good)
    return good

def check_user_exists(username: str):
    print(f"Provided username: {username}")
    users = database.get_user_by_name(username=username)
    print("users response:")
    print(users)
    if users:
        userlist = list(users)
        if username in userlist:
            return True
    return False

def create_user(username: str, hashed_password: bytes):
    database.insert_user(username, hashed_password)
    return True

def hash_password(password: str) -> bytes:
    bpassword = password.encode('utf-8')
    hashed = bcrypt.hashpw(bpassword, bcrypt.gensalt())
    return hashed

def get_routes() -> dict | None:
    routes = database.get_all_routes()
    print(type(routes))
    column_names = database.get_column_names_from("routes")
    if not routes:
        return None
    list_routes = []
    for row in range(0,len(routes)):
        list_routes.append(dict(zip(column_names, routes[row])))
    print(f"route list dict: \n{list_routes}\n")
    return list_routes
    # return [
    #     {"id": 1, "name": "cool route", "grade": 0},
    #     {"id": 2, "name": "test ma goats", "grade": 3},
    #     {"id": 3, "name": "lemon bomb", "grade": 8},
    # ]

def check_route_exists(route_name: str) -> Tuple[int, str]:
    routes = database.get_route_by_name(route_name)
    if routes:
        routelist = list(routes)
        if route_name in routelist:
            return routelist[route_name][1], None
    return None, None

def add_route(route_name: str, route_grade: int, creating_user: str) -> Tuple[int, str]:
    existing_id = database.get_route_by_name(route_name)
    if existing_id:
        return existing_id, 'Route with name already exists'
    id = database.insert_route(name=route_name, grade=route_grade, user=creating_user)
    if not id:
        return None, 'Error creating route'
    return id, None

def get_route_by_id(route_id: int) -> Tuple[int, str]:
    id, error = database.get_route_by_id(route_id)
    return id, error

