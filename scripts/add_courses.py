# scripts/add_courses.py
import pandas as pd
from pathlib import Path

DATA_DIR = Path('data')
COURSES_FILE = DATA_DIR / 'courses.csv'

new_courses = [
    ('Data Science', 'Introductory Data Science course covering statistics, Python, and visualization.', 'TBD', '', ''),
    ('Cloud Computing', 'Fundamentals of cloud platforms, deployment, and services.', 'TBD', '', ''),
    ('Environmental Studies', 'Study of environment, ecosystems, and sustainability.', 'TBD', '', ''),
    ('Machine Learning', 'Theory and practice of machine learning models and workflows.', 'TBD', '', ''),
    ('Machine Learning - Lab', 'Hands-on lab course to implement ML models (practical).', 'TBD', '', ''),
    ('Research Methodology and IPR', 'Research methods, academic writing and Intellectual Property Rights.', 'TBD', '', ''),
]

def ensure_courses_file():
    DATA_DIR.mkdir(exist_ok=True)
    if not COURSES_FILE.exists():
        COURSES_FILE.write_text("id,title,description,instructor,thumbnail,asset_path\n", encoding="utf-8")

def load_courses():
    try:
        return pd.read_csv(COURSES_FILE)
    except Exception:
        return pd.DataFrame(columns=["id","title","description","instructor","thumbnail","asset_path"])

def next_id(df):
    if df.empty:
        return 1
    try:
        return int(pd.to_numeric(df["id"], errors="coerce").max()) + 1
    except Exception:
        return len(df) + 1

def main():
    ensure_courses_file()
    df = load_courses()
    start = next_id(df)
    rows = []
    for i, (title, desc, instr, thumb, asset) in enumerate(new_courses):
        rows.append({
            "id": start + i,
            "title": title,
            "description": desc,
            "instructor": instr,
            "thumbnail": thumb,
            "asset_path": asset
        })
    if rows:
        new_df = pd.concat([df, pd.DataFrame(rows)], ignore_index=True)
        new_df.to_csv(COURSES_FILE, index=False, encoding="utf-8")
        print(f"Added {len(rows)} courses to {COURSES_FILE}")
    else:
        print("No courses to add.")
    print(pd.read_csv(COURSES_FILE).to_string(index=False))

if __name__ == '__main__':
    main()
