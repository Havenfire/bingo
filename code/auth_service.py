import json
import os
import bcrypt

USER_FILE = "users.json"


def load_users():
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    dirpath = os.path.dirname(USER_FILE)
    if dirpath:
        os.makedirs(dirpath, exist_ok=True)

    tmp_path = f"{USER_FILE}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)
    os.replace(tmp_path, USER_FILE)


def is_valid_email(email):
    email = (email or "").strip()
    return bool(email and "@" in email)


def is_valid_password(password):
    return bool(password and password.strip())


def register_user(email, password):
    email = (email or "").lower().strip()
    password = password or ""

    if not is_valid_email(email):
        return False, "Please provide a valid email address."
    if not is_valid_password(password):
        return False, "Password must be at least 8 characters."

    users = load_users()
    if email in users:
        return False, "Email already registered."

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    users[email] = {"password": hashed}
    save_users(users)

    return True, "Registration successful."


def authenticate(email, password):
    email = (email or "").lower().strip()
    password = password or ""

    if not is_valid_email(email):
        return False, "Please provide a valid email address."

    users = load_users()
    if email not in users:
        return False, "No account with that email."

    stored = users[email]["password"].encode()
    if bcrypt.checkpw(password.encode(), stored):
        return True, "Login successful."

    return False, "Incorrect password."
