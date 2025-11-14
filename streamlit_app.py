# streamlit_app.py
import streamlit as st
import importlib
import traceback
from pathlib import Path

# try to import auth helpers (if present). If not, we'll provide simple CSV-backed fallbacks.
try:
    from utils.auth import login_user, register_user, get_user_role
    auth_using_module = True
except Exception:
    auth_using_module = False

from utils.data_io import ensure_data_files, load_users, save_users

# -------------------------
# CSV-backed fallback auth
# -------------------------


def _next_user_id(df):
    try:
        return int(df['id'].astype(int).max()) + 1
    except Exception:
        return len(df) + 1 if not df.empty else 1


def _fallback_register_user(username, password, role="student"):
    users = load_users()
    if users.empty:
        users = users.reindex(columns=['id', 'username', 'password', 'role'])
    # check existing username
    if not users.empty and (users['username'] == username).any():
        return False
    uid = _next_user_id(users)
    new = {'id': int(uid), 'username': username,
           'password': password, 'role': role}
    users = users.append(new, ignore_index=True)
    save_users(users)
    return True


def _fallback_login_user(username, password):
    users = load_users()
    if users.empty:
        return None
    # exact match (plain-text password). Adapt if you have hashed passwords.
    matched = users[(users['username'] == username) &
                    (users['password'] == password)]
    if matched.empty:
        return None
    row = matched.iloc[0].to_dict()
    # return a consistent dict: id, username, role
    return {'id': int(row.get('id')), 'username': row.get('username'), 'role': row.get('role')}


def _fallback_get_user_role(user):
    if not user:
        return None
    if isinstance(user, dict):
        return user.get('role')
    # if username string, lookup
    users = load_users()
    found = users[users['username'] == str(user)]
    if found.empty:
        return None
    return found.iloc[0].get('role')


# choose functions (use real auth if available, else fallback)
if not auth_using_module:
    login_user = _fallback_login_user
    register_user = _fallback_register_user
    get_user_role = _fallback_get_user_role

# -------------------------
# Ensure data files exist
# -------------------------
ensure_data_files()

# -------------------------
# Page navigation helpers
# -------------------------
PAGES = [
    ("p1_home", "p1 home"),
    ("p2_courses", "p2 courses"),
    ("p3_my_courses", "p3 my courses"),
    ("p4_admin", "p4 admin"),
]


def run_page(page_module_name, user):
    """
    Dynamically import pages.<page_module_name> and call its app(user) function.
    """
    try:
        module = importlib.import_module(f"pages.{page_module_name}")
        importlib.reload(module)
    except Exception as e:
        st.error(f"Failed to import page {page_module_name}: {e}")
        tb = traceback.format_exc()
        st.code(tb)
        return

    # call app(user) if available
    try:
        if hasattr(module, "app"):
            # some pages accept user arg, some may not — try both
            try:
                module.app(user)
            except TypeError:
                module.app()
        else:
            st.error(f"Page module {page_module_name} has no `app` function.")
    except Exception as e:
        st.error(f"Error while running page {page_module_name}: {e}")
        st.code(traceback.format_exc())

# -------------------------
# App layout & auth sidebar
# -------------------------


def auth_sidebar():
    st.sidebar.title("🔐 Authentication")
    # ensure session keys exist
    if "user" not in st.session_state:
        st.session_state.user = None
    if "role" not in st.session_state:
        st.session_state.role = None

    if st.session_state.user:
        u = st.session_state.user
        username = u.get("username") if isinstance(u, dict) else str(u)
        role = u.get("role") if isinstance(u, dict) else get_user_role(u)
        st.sidebar.success(f"Logged in as **{username}** ({role})")
        if st.sidebar.button("Logout", key="logout_btn"):
            st.session_state.user = None
            st.session_state.role = None
            st.rerun()
    else:
        action = st.sidebar.radio(
            "Select Action", ["Login", "Register"], index=0, key="auth_action")
        if action == "Login":
            username = st.sidebar.text_input("Username", key="login_username")
            password = st.sidebar.text_input(
                "Password", type="password", key="login_password")
            if st.sidebar.button("Login", key="login_btn"):
                user = login_user(username, password)
                if user:
                    # store full user dict
                    st.session_state.user = user
                    st.session_state.role = user.get("role") if isinstance(
                        user, dict) else get_user_role(user)
                    st.sidebar.success(
                        f"Welcome back, {user.get('username') if isinstance(user, dict) else user}")
                    st.rerun()
                else:
                    st.sidebar.error("Invalid username or password")
        else:
            new_user = st.sidebar.text_input(
                "New username", key="reg_username")
            new_pass = st.sidebar.text_input(
                "New password", type="password", key="reg_password")
            role = st.sidebar.selectbox(
                "Role", ["student", "admin"], key="reg_role")
            if st.sidebar.button("Register", key="reg_btn"):
                ok = register_user(new_user, new_pass, role)
                if ok:
                    st.sidebar.success("User registered — please log in.")
                else:
                    st.sidebar.error(
                        "Username already exists or registration failed.")

# -------------------------
# Main UI
# -------------------------


def main():
    st.set_page_config(page_title="E-Learning (Streamlit)", layout="wide")
    st.title("streamlit app")

    # Sidebar auth + navigation
    auth_sidebar()

    st.sidebar.markdown("---")
    st.sidebar.header("📚 Pages")
    page_labels = [label for (_, label) in PAGES]
    page_keys = [mod for (mod, _) in PAGES]

    # map label -> module index
    selected_label = st.sidebar.selectbox(
        "Go to", page_labels, index=0, key="nav_select")
    selected_index = page_labels.index(selected_label)
    selected_module = page_keys[selected_index]

    st.sidebar.markdown("---")
    st.sidebar.caption("Mini e-learning - Streamlit")

    # get current user object
    user = st.session_state.user

    # Run chosen page
    run_page(selected_module, user)


if __name__ == "__main__":
    main()
