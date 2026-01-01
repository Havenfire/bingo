import json
import os
import bcrypt

USER_FILE = "users.json"


def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)


def register_user(email, password):
    email = email.lower().strip()
    users = load_users()

    if email in users:
        return False, "Email already registered."

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[email] = {"password": hashed}
    save_users(users)

    return True, "Registration successful."


def authenticate(email, password):
    email = email.lower().strip()
    users = load_users()

    if email not in users:
        return False, "No account with that email."

    stored = users[email]["password"].encode()
    if bcrypt.checkpw(password.encode(), stored):
        return True, "Login successful."

    return False, "Incorrect password."
