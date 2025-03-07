import sqlite3
from typing import Tuple
import os

db_path = os.getenv("DB_PATH", "./")
db_name = os.getenv("DB_NAME", "climbing.db")

con = None
cur = None

def init_db():
    global con, cur
    con = sqlite3.connect(f"{db_path}{db_name}", check_same_thread=False)
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
    resp = cur.execute("SELECT username FROM climbers WHERE username=(?)", ( username, ))
    users = resp.fetchone()
    print(users)
    return users

def get_user_id_from_name(username: str) -> int:
    resp = cur.execute("SELECT climber_id FROM climbers WHERE username=(?)", (username, ))
    users = resp.fetchone()
    if not users:
        return None
    return users[0]

def get_user_password(username: str) -> bytes:
    print(f'Getting password for user: {username}')
    resp = cur.execute("SELECT password_hash FROM climbers WHERE username=(?)", (username, ))
    hashpass = resp.fetchone()[0]
    return hashpass

def get_registration_code() -> str:
    cur = con.cursor()
    resp = cur.execute("SELECT register_code FROM app_data")
    return resp.fetchone()[0]

def insert_user(username: str, password_hash: bytes, common_name: str = None, team_id: int=-1, is_admin: bool=False) -> int:
    cur = con.cursor()
    print(f"{username}, {password_hash}, {common_name}, {team_id}, {is_admin}")
    query_str = "INSERT INTO climbers (username, password_hash, common_name, team_id, is_admin) VALUES (?, ?, ?, ?, ?);"
    vals = (username, password_hash, common_name, team_id, is_admin )
    print(query_str)
    print(vals)
    cur.execute(query_str, vals)
    commit()
    created_user_id = cur.lastrowid
    print("Created user {username}, got id {created_user_id}")
    return created_user_id

def get_all_user_ids() -> tuple:
    resp = cur.execute("SELECT climber_id FROM climbers;")
    ids = resp.fetchall()
    print(f"Found all ids: {ids}")
    return ids
#######################

#######################
"""
Route details only obtainable by ID
"""
def get_route_by_id(id: int) -> tuple:
    print("Getting routes for id: {id}")
    resp = cur.execute(f"SELECT * FROM routes WHERE route_id=(?);", (id, ))
    route_id = resp.fetchone()
    print(f"route id: {route_id}")
    return route_id

"""
Used only to check route names during route creation
use 'get_route_by_id' for getting a route's details
"""
def get_route_by_name(name: str) -> tuple | None:
    print("Getting routes for route name: {name}")
    resp = cur.execute("SELECT route_id, route_name FROM routes WHERE route_name=(?);", (name, ))
    routes = resp.fetchone()
    print(f"routes found: {routes}")
    return routes

def get_all_routes() -> tuple | None:
    print("Getting all routes in DB")
    resp = cur.execute("SELECT * FROM routes;")
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

def insert_route(name: str, grade: int, points: int, user: str) -> int:
    print(f"Creating route: {name}, {grade}, {user}")
    cur = con.cursor()
    cur.execute("INSERT INTO routes (route_name, route_grade, route_points, route_created_by) \
                VALUES (?, ?, ?, ?);",
                (name, grade, points, user))
    commit()
    created_route_id = cur.lastrowid
    print(f"Created new route {name}, got id {created_route_id}")
    # returns route ID for redirection to created route
    cur.close()
    return created_route_id

def get_user_route_stats(user_id: str, route_id: int) -> tuple:
    print(f"Getting {user_id} stats for route {route_id}")
    resp = cur.execute("SELECT attempt_num, is_sent, send_date \
                       FROM attempts_sends \
                       WHERE route_id=(?) and climber_id=(?);",
                       (route_id, user_id))
    user_info = resp.fetchall()
    if not user_info:
        return None
    print(f"User {user_id} info for route {route_id}: {user_info[0]}")
    return user_info[0]

def bulk_add_users_to_routes(route_id: int, uids: list) -> str | None:
    print(f"Adding all the user's to route {route_id}")
    cur = con.cursor()
    for uid in uids:
        print(f"Bulk params for {uid[0]}")
        cur.execute("INSERT INTO attempts_sends (route_id, climber_id) VALUES (?, ?);", (route_id, uid[0]))
    commit()
    cur.close()
    return True

def add_user_to_route(route_id: int, uid: str) -> str | None:
    print(f"Adding user {uid} to all route {route_id}")
    cur = con.cursor()
    cur.execute("UPSERT INTO attempts_sends (route_id, climber_id) VALUES (?, ?)", (route_id, uid))
    commit()
    cur.close()
    return

def add_user_to_all_routes(uid: str) -> str | None:
    print(f"Adding user {uid} to all current routes")
    routes = get_all_routes()
    cur = con.cursor()
    for route in routes:
        params = (route[0], uid)
        cur.execute("INSERT INTO attempts_sends (route_id, climber_id) VALUES (?, ?) ON CONFLICT (route_id, climber_id) DO NOTHING;", (route[0], uid) )
    commit()
    cur.close()
    return

def add_attempt(uid: int, route_id: int, attempts: int=1) -> str | None:
    print(f"Adding +{attempts} attempts to {uid} for route {route_id}")
    cur = con.cursor()
    cur.execute("UPDATE attempts_sends SET attempt_num = attempt_num + (?) WHERE climber_id = (?) and route_id = (?);", (attempts, uid, route_id) )
    commit()
    # cur.close()
    return None

def mark_sent(uid: int, route_id: int) -> str | None:
    print(f"Marking route {route_id} as sent for user {uid}")
    cur = con.cursor()
    cur.execute("UPDATE attempts_sends SET is_sent = True WHERE climber_id=(?) and route_id=(?)", (uid,route_id) )
    commit()
    cur.close()
    return None
