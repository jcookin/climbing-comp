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
            print(f"found route: {routelist}")
            return routelist, None
    return None, None

def add_route(route_name: str, route_grade: int, creating_user: str) -> Tuple[int, str]:
    existing_id = database.get_route_by_name(route_name)
    if existing_id:
        return existing_id, 'Route with name already exists'
    id = database.insert_route(name=route_name, grade=route_grade, user=creating_user)
    if not id:
        return None, 'Error creating route'
    err = add_route_to_all_users(route_id=id)
    if err:
        return id, err
    return id, None

def add_route_to_all_users(route_id: int) -> str:
    users = database.get_all_user_ids()
    # if no users, exit cleanly anyway
    if not users:
        return None
    err = database.bulk_add_users_to_routes(route_id, users)
    if err:
        print(f"Error adding some users to the new route {route_id}")
        return 'Error adding all users to new route'
    return None

def get_route_by_id(route_id: int) -> Tuple[dict, str]:
    route_info = database.get_route_by_id(route_id)
    column_names = database.get_column_names_from("routes")
    if not route_info:
        return None, f'No route found with id {route_id}'
    
    route_dict = dict(zip(column_names, route_info))
    print(f"route_dict: {route_dict}")
    print(type(route_dict))
    return route_dict, None

def get_user_info_for_route_id(username: str, route_id: int) -> Tuple[dict, str]:
    user_id = database.get_user_id_from_name(username=username)
    user_info = database.get_user_route_stats(user_id=user_id, route_id=route_id)
    user_route_dict = {"attempts": user_info[0], "sent": bool(user_info[1]), "send_date": user_info[2]}
    print("~~~user route dict:")
    print(user_route_dict)
    return user_route_dict, None
