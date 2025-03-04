import sqlite3

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


def get_user_by_name(username: str):
    pass

def put_user_in_db(username: str, password: str):
    pass

def get_salt():
    cur = con.cursor()
    resp = cur.execute("SELECT salt FROM app_data;")
    return resp.fetchone()[0]

def insert_user(username: str, hashed_password: str, is_admin: bool = False):
    resp = cur.execute(f"""
                INSERT INTO climbers 
                    (username, password_hash, is_admin, team_id)
                    VALUES ({username}, {hashed_password}, {is_admin});
                """)
    return resp.fetchone()