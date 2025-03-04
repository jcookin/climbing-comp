import database
import bcrypt

def init():
    database.init_db()

def validate_login(username, password):
    return True

def validate_registration_code():
    print("validating registration code")
    return True

def check_user_exists():
    print("user exists check")
    return True

def create_user(username: str, hashed_password: str):
    database.insert_user(username, hashed_password)
    return True

def hash_password(password):
    salt = database.get_salt()
    hashed = bcrypt.hashpw(password, salt)
    return hashed

def get_routes():
    return [
        {"id": 1, "name": "cool route", "grade": 0},
        {"id": 2, "name": "test ma goats", "grade": 3},
        {"id": 3, "name": "lemon bomb", "grade": 8},
    ]

def get_route_by_id(route_id: int):
    return {"id": 3, "name": "whoa there pardner", "grade": 5, "attempts": 69, "sent": False}
