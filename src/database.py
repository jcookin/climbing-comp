import sqlite3
from typing import Tuple

db_path = "./"
db_name = "climbing.db"

con = None
cur = None

def init_db():
    global con, cur
    con = sqlite3.connect(f'{db_path}{db_name}', check_same_thread=False)
    cur = con.cursor()
    with open("./db/01.sql", "r") as dbf:
        sql = dbf.read()
        cur.executescript(sql)
    commit()

def commit():
    global con
    con.commit()


#######################
"""
User management
"""
def get_user_by_name(username: str) -> tuple:
    resp = cur.execute(f"SELECT username FROM climbers WHERE username='{username}'")
    users = resp.fetchone()
    print(users)
    return users

def get_user_id_from_name(username: str) -> int:
    resp = cur.execute(f"SELECT climber_id FROM climbers WHERE username='{username}'")
    users = resp.fetchone()
    if not users:
        return None
    return users[0]

def get_user_password(username: str) -> bytes:
    print(f'Getting password for user: {username}')
    resp = cur.execute(f"SELECT password_hash FROM climbers WHERE username='{username}'")
    hashpass = resp.fetchone()[0]
    print(hashpass) # TODO: remove
    return hashpass

def get_registration_code() -> str:
    cur = con.cursor()
    resp = cur.execute("SELECT register_code FROM app_data")
    return resp.fetchone()[0]

def insert_user(username: str, hashed_password: bytes, team_id: int = -1, is_admin: bool = False) -> int:
    params = (username, hashed_password, team_id, is_admin)
    cur = con.cursor()
    cur.execute("INSERT INTO climbers (username, password_hash, team_id, is_admin) VALUES (?, ?, ?, ?);", params)
    commit()
    created_user_id = cur.lastrowid
    print(f"Created user {username}, got id {created_user_id}")
    return created_user_id

def get_all_user_ids() -> tuple:
    resp = cur.execute(f"SELECT climber_id FROM climbers;")
    ids = resp.fetchall()
    print(f"Found all ids: {ids}")
    return ids
#######################

#######################
"""
Route details only obtainable by ID
"""
def get_route_by_id(id: int) -> tuple:
    print(f"Getting routes for id: {id}")
    resp = cur.execute(f"SELECT * FROM routes WHERE route_id='{id}';")
    route_id = resp.fetchone()
    print(f"route id: {route_id}")
    return route_id

"""
Used only to check route names during route creation
use 'get_route_by_id' for getting a route's details
"""
def get_route_by_name(name: str) -> tuple | None:
    print(f"Getting routes for name: {name}")
    resp = cur.execute(f"SELECT route_id, route_name FROM routes WHERE route_name='{name}';")
    routes = resp.fetchone()
    print(f"routes found: {routes}")
    return routes

def get_all_routes() -> tuple | None:
    print(f"Getting all routes in DB")
    resp = cur.execute("SELECT * FROM routes")
    routes = resp.fetchall()
    print(f"Got routes: {routes}")
    return routes

def get_column_names_from(table_name: str) -> tuple:
    resp = cur.execute(f"PRAGMA table_info({table_name})")
    table_desc = resp.fetchall()
    print(table_desc)
    column_names = []
    for d in table_desc:
        column_names.append(d[1])
    print(f"Got column names: {column_names}")
    return tuple(column_names)

def insert_route(name: str, grade: str, user: str) -> int:
    print(f"Creating route: {name}, {grade}, {user}")
    params = (name, grade, user)
    cur = con.cursor()
    cur.execute("INSERT INTO routes (route_name, route_grade, route_created_by) VALUES (?, ?, ?);", params)
    commit()
    created_route_id = cur.lastrowid
    print(f"Created new route {name}, got id {created_route_id}")
    # returns route ID for redirection to created route
    return created_route_id

def get_user_route_stats(user_id: str, route_id: int) -> tuple:
    print(f"Getting {user_id} stats for route {route_id}")
    resp = cur.execute(f"SELECT attempt_num, is_sent, send_date FROM attempts_sends WHERE route_id='{route_id}' and climber_id='{user_id}';")
    user_info = resp.fetchall()
    if not user_info:
        return None
    print(f"User {user_id} info for route {route_id}: {user_info[0]}")
    return user_info[0]

def bulk_add_users_to_routes(route_id: int, uids: list) -> str | None:
    print(f"Adding all the user's to route {route_id}")
    cur = con.cursor()
    for uid in uids:
        params = (route_id, uid[0])
        print(f"Bulk params for {uid[0]}")
        print(params)
        cur.execute("INSERT INTO attempts_sends (route_id, climber_id) VALUES (?, ?);", params)
    commit()
    return True
