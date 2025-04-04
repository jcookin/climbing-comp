import database
import bcrypt
from typing import Tuple
import os

root_route = os.getenv("ROOT_ROUTE", "http://localhost")
default_admin = os.getenv("ADMIN_USER", "admin")
default_admin_password = os.getenv("ADMIN_PASSWORD", "admin")

global con

def init():
    global con
    con = database.init_db()
    # if not 
    database.insert_user(username=default_admin, password_hash=hash_password(default_admin_password), common_name="Admin", is_admin=True, team_id=-1)
    admin_id = get_user_id(default_admin)
    err = add_user_to_all_routes(admin_id)
    print(err)

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
    registration_code = database.get_registration_code()
    good = user_code == registration_code
    print(good)
    return good

def check_user_exists(username: str):
    print(f"Provided username: {username}")
    users = database.get_user_by_name(username=username)
    if users:
        print(f"Found existing user(s): {users}")
        userlist = list(users)
        if username in userlist:
            return True
    return False

def create_user(username: str, hashed_password: bytes, common_name: str = None) -> str | None:
    created_uid = database.insert_user(username, hashed_password, common_name)
    # Add user to every existing route by default
    err = add_user_to_all_routes(created_uid)
    return err

def hash_password(password: str) -> bytes:
    bpassword = password.encode('utf-8')
    hashed = bcrypt.hashpw(bpassword, bcrypt.gensalt())
    return hashed

def get_user_id(username: str):
    return database.get_user_id_from_name(username=username)

def check_user_id_is_admin(userid: int):
    user_info = database.get_user_by_id(userid)
    if not user_info:
        return False
    return user_info['is_admin']

def get_routes() -> list:
    routes = database.get_all_routes()
    column_names = database.get_column_names_from("routes")
    if not routes:
        return []
    list_routes = []
    for row in range(0,len(routes)):
        list_routes.append(dict(zip(column_names, routes[row])))
    print(f"route list as list of dicts: \n{list_routes}\n")
    return list_routes

def check_route_exists(route_name: str) -> Tuple[int, str]:
    print(f"Checking for existing route with name {route_name}")
    routes = database.get_route_by_name(route_name)
    if routes:
        routelist = list(routes)
        if route_name in routelist:
            print(f"found route: {route_name}")
            return routelist, None
    return None, None

def add_route(route_name: str, route_grade: int, route_points: int, creating_user: str) -> Tuple[int, str]:
    existing_id = database.get_route_by_name(route_name)
    if existing_id:
        return existing_id, 'Route with name already exists'
    id = database.insert_route(name=route_name, grade=route_grade, points=route_points, user=creating_user)
    if not id:
        print(f"Error adding route")
        return None, 'Error creating route'
    err = add_route_to_all_users(route_id=id)
    if err:
        print(f"Error while adding users to new route: {err}")
        return id, err
    return id, None

def add_user_to_all_routes(user_id: int) -> str | None:
    print("Adding new user to all existing routes")
    err = database.add_user_to_all_routes(user_id)
    return err

def add_route_to_all_users(route_id: int) -> str | None:
    print("Adding new route to all users")
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
    print(f"Getting route with id: {route_id}")
    route_info = database.get_route_by_id(route_id)
    column_names = database.get_column_names_from("routes")
    if not route_info:
        return None, f'No route found with id {route_id}'
    
    route_dict = dict(zip(column_names, route_info))
    return route_dict, None

def get_user_info_for_route_id(username: str, route_id: int) -> Tuple[dict, str]:
    print(f"Getting info for user '{username}' on route id '{route_id}'")
    user_id = database.get_user_id_from_name(username=username)
    user_info = database.get_user_route_stats(user_id=user_id, route_id=route_id)
    user_route_dict = {"attempts": user_info[0], "sent": bool(user_info[1]), "send_date": user_info[2]}
    return user_route_dict, None

def add_route_attempt(username: str, route_id: int) -> str | None:
    uid = database.get_user_id_from_name(username=username)
    return database.add_attempt(uid, route_id)

def mark_route_sent(username: str, route_id: int) -> str | None:
    uid = database.get_user_id_from_name(username=username)
    return database.mark_sent(uid, route_id)

def sort_routes_by_date(routes: list) -> list:
    """
    Args: list of dicts, representing routes
    Returns: list of dicts, inverse sorted by date (newest first)
    """
    for r in routes:
        print(r)
        # print(r.route_created)
    sorted_routes = sorted(routes, key=lambda r: r['route_created'], reverse=True)
    print(sorted_routes)
    return sorted_routes


############ DELETE ACTIONS ###################
def delete_route_by_id(route_id: int) -> bool:
    status = database.delete_route_with_id(route_id=route_id)
    return status