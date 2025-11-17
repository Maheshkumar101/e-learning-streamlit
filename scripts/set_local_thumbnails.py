#!/usr/bin/env python3
# scripts/set_local_thumbnails.py
#
# Fully working script to set local thumbnail paths for courses.
# REPLACE your entire file with this EXACT version.

import sys
from pathlib import Path
import shutil
import pandas as pd
import datetime

ROOT = Path('.')
DATA_DIR = ROOT / 'data'
COURSES_FILE = DATA_DIR / 'courses.csv'
BACKUP_DIR = DATA_DIR / 'backups'
THUMB_DIR = ROOT / 'assets' / 'thumbnails'

# Mapping: course title -> local thumbnail path
THUMB_MAPPING = {
    "Data Science": "assets/thumbnails/data_science.jpg",
    "Cloud Computing": "assets/thumbnails/cloud_computing.jpg",
    "Environmental Studies": "assets/thumbnails/environmental_studies.jpg",
    "Machine Learning": "assets/thumbnails/machine_learning.jpg",
    "Machine Learning - Lab": "assets/thumbnails/machine_learning_lab.jpg",
    "Research Methodology and IPR": "assets/thumbnails/research_methodology_ipr.jpg"
}


def ensure_paths():
    if not DATA_DIR.exists():
        print(f"❌ data/ folder missing at {DATA_DIR}")
        sys.exit(1)
    if not COURSES_FILE.exists():
        print(f"❌ courses.csv missing at {COURSES_FILE}")
        sys.exit(1)

    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def backup_courses():
    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = BACKUP_DIR / f"courses.csv.bak.{ts}"
    shutil.copy2(COURSES_FILE, backup_file)
    print(f"📦 Backup created: {backup_file}")
    return backup_file


def load_courses():
    try:
        df = pd.read_csv(COURSES_FILE, dtype=str).fillna("")
        required_cols = ["id", "title", "description",
                         "instructor", "thumbnail", "asset_path"]
        for col in required_cols:
            if col not in df.columns:
                df[col] = ""
        return df
    except Exception as e:
        print("❌ Error reading courses.csv ->", e)
        sys.exit(1)


def apply_mapping(df):
    updated = 0
    for i, row in df.iterrows():
        title = str(row["title"]).strip()
        if title in THUMB_MAPPING:
            path = THUMB_MAPPING[title]

            # Warning if image not found
            if not Path(path).exists():
                print(f"⚠ Warning: file missing for '{title}': {path}")

            df.at[i, "thumbnail"] = path
            updated += 1

    return df, updated


def write_courses(df):
    try:
        df.to_csv(COURSES_FILE, index=False, encoding="utf-8")
        print(f"💾 Updated {COURSES_FILE}")
    except Exception as e:
        print("❌ Error writing courses.csv:", e)
        sys.exit(1)


def main():
    print("\n=== Setting Local Thumbnails ===")
    ensure_paths()
    backup_courses()
    df = load_courses()
    df, count = apply_mapping(df)
    write_courses(df)
    print(f"✔ Done — updated {count} course thumbnails\n")


if __name__ == "__main__":
    main()
