import pandas as pd
from pathlib import Path

# File path for users CSV
USERS_FILE = Path("data/users.csv")

# ------------------------------------------------------------------
# Ensure file exists (header only if missing)
# ------------------------------------------------------------------


def ensure_user_file():
    USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not USERS_FILE.exists():
        USERS_FILE.write_text("id,username,password,role\n", encoding="utf-8")

# ------------------------------------------------------------------
# Read all users
# ------------------------------------------------------------------


def load_users():
    ensure_user_file()
    try:
        df = pd.read_csv(USERS_FILE)
        if df.empty:
            return []
        return df.to_dict(orient="records")
    except Exception:
        return []

# ------------------------------------------------------------------
# Save users
# ------------------------------------------------------------------


def save_users(users):
    pd.DataFrame(users).to_csv(USERS_FILE, index=False)

# ------------------------------------------------------------------
# Register a new user
# ------------------------------------------------------------------


def register_user(username, password, role="student"):
    ensure_user_file()
    users = load_users()

    # Prevent duplicates
    if any(u["username"] == username for u in users):
        return False

    new_id = len(users) + 1
    users.append({
        "id": new_id,
        "username": username,
        "password": password,
        "role": role
    })
    save_users(users)
    return True

# ------------------------------------------------------------------
# Authenticate (login)
# ------------------------------------------------------------------


def login_user(username, password):
    users = load_users()
    for u in users:
        if u["username"] == username and u["password"] == password:
            return u
    return None

# ------------------------------------------------------------------
# Get user role
# ------------------------------------------------------------------


def get_user_role(username):
    users = load_users()
    for u in users:
        if u["username"] == username:
            return u["role"]
    return None
