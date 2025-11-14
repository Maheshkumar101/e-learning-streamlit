import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
COURSES = DATA_DIR / 'courses.csv'
USERS = DATA_DIR / 'users.csv'
ENROLLMENTS = DATA_DIR / 'enrollments.csv'


def ensure_data_files():
    DATA_DIR.mkdir(exist_ok=True)
    if not COURSES.exists():
        COURSES.write_text(
            'id,title,description,instructor,thumbnail,asset_path\n', encoding='utf-8')
    if not USERS.exists():
        USERS.write_text('id,username,password,role\n', encoding='utf-8')
    if not ENROLLMENTS.exists():
        ENROLLMENTS.write_text('id,user_id,course_id\n', encoding='utf-8')


def _read_csv_safe(path, columns=None):
    """Read CSV but return an empty dataframe with columns if file empty or invalid."""
    ensure_data_files()
    try:
        df = pd.read_csv(path)
        return df
    except Exception:
        if columns is None:
            return pd.DataFrame()
        return pd.DataFrame(columns=columns)


# -------------------------
# Courses
# -------------------------
def load_courses():
    """Return courses DataFrame."""
    return _read_csv_safe(COURSES)


def add_course(title, description, instructor, thumbnail='', asset_path=''):
    """Append a new course and return its id."""
    df = load_courses()
    if df.empty:
        next_id = 1
        df = pd.DataFrame(
            columns=['id', 'title', 'description', 'instructor', 'thumbnail', 'asset_path'])
    else:
        try:
            max_id = int(df['id'].astype(int).max())
        except Exception:
            max_id = len(df)
        next_id = max_id + 1

    new = {
        'id': int(next_id),
        'title': title,
        'description': description,
        'instructor': instructor,
        'thumbnail': thumbnail or '',
        'asset_path': asset_path or ''
    }
    df = pd.concat([df, pd.DataFrame([new])], ignore_index=True)
    df.to_csv(COURSES, index=False)
    return int(next_id)


# -------------------------
# Users
# -------------------------
def load_users():
    return _read_csv_safe(USERS)


def save_users(df):
    df.to_csv(USERS, index=False)


# -------------------------
# Enrollments
# -------------------------
def load_enrollments():
    return _read_csv_safe(ENROLLMENTS)


def save_enrollments(df):
    df.to_csv(ENROLLMENTS, index=False)


def enroll_user(user_id, course_id):
    """Enroll a numeric user_id into a numeric course_id."""
    ensure_data_files()
    enroll = load_enrollments()
    if enroll.empty:
        next_id = 1
        enroll = pd.DataFrame(columns=['id', 'user_id', 'course_id'])
    else:
        try:
            next_id = int(enroll['id'].astype(int).max()) + 1
        except Exception:
            next_id = len(enroll) + 1

    new_row = {'id': int(next_id), 'user_id': int(
        user_id), 'course_id': int(course_id)}
    enroll = pd.concat([enroll, pd.DataFrame([new_row])], ignore_index=True)
    save_enrollments(enroll)
    return True


# -------------------------
# Helpers used by pages
# -------------------------
def my_courses_for_user(user_id):
    """Return DataFrame of courses the given user_id is enrolled in."""
    ensure_data_files()
    try:
        uid = int(user_id)
    except Exception:
        try:
            uid = int(getattr(user_id, 'id'))
        except Exception:
            return pd.DataFrame()

    enroll = load_enrollments()
    if enroll.empty:
        return pd.DataFrame()

    try:
        enroll = enroll.astype(
            {'user_id': 'int64', 'course_id': 'int64', 'id': 'int64'})
    except Exception:
        enroll['user_id'] = pd.to_numeric(
            enroll['user_id'], errors='coerce').fillna(-1).astype(int)
        enroll['course_id'] = pd.to_numeric(
            enroll['course_id'], errors='coerce').fillna(-1).astype(int)

    user_rows = enroll[enroll['user_id'] == uid]
    if user_rows.empty:
        return pd.DataFrame()

    courses = load_courses()
    if courses.empty:
        return pd.DataFrame()

    courses['id'] = pd.to_numeric(courses['id'], errors='coerce')
    course_ids = user_rows['course_id'].astype(int).tolist()
    return courses[courses['id'].isin(course_ids)].reset_index(drop=True)


def delete_course(course_id):
    ensure_data_files()
    courses = load_courses()
    if courses.empty:
        return False
    courses = courses[courses['id'] != int(course_id)]
    courses.to_csv(COURSES, index=False)
    return True
# ---------------------------------------------------------
# Backwards compatibility wrapper (some pages expect enroll())
# ---------------------------------------------------------


def enroll(user_id, course_id):
    """Compatibility wrapper for pages that call enroll()."""
    return enroll_user(user_id, course_id)
