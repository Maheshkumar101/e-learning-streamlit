#!/usr/bin/env python3
# scripts/auto_download_thumbnails.py
"""
Auto-download 6 thumbnails from Unsplash and update data/courses.csv.

Usage:
  python scripts/auto_download_thumbnails.py
"""

import sys
from pathlib import Path
import requests
import shutil
import datetime
import pandas as pd

ROOT = Path('.')
THUMB_DIR = ROOT / 'assets' / 'thumbnails'
DATA_DIR = ROOT / 'data'
COURSES_CSV = DATA_DIR / 'courses.csv'
BACKUP_DIR = DATA_DIR / 'backups'

THUMB_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# Mapping: course title -> (filename, direct image URL)
# I selected stable Unsplash image IDs — if any fail, replace the URL with one you copy from Unsplash.
IMAGE_MAP = {
    "Data Science": ("data_science.jpg",
                     "https://images.unsplash.com/photo-1519389950473-47ba0277781c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"),
    "Cloud Computing": ("cloud_computing.jpg",
                        "https://images.unsplash.com/photo-1505685296765-3a2736de412f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"),
    "Environmental Studies": ("environmental_studies.jpg",
                              "https://images.unsplash.com/photo-1501785888041-af3ef285b470?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"),
    "Machine Learning": ("machine_learning.jpg",
                         "https://images.unsplash.com/photo-1502880195258-8d5b2a8f5f4b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"),
    "Machine Learning - Lab": ("machine_learning_lab.jpg",
                               "https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"),
    "Research Methodology and IPR": ("research_methodology_ipr.jpg",
                                     "https://images.unsplash.com/photo-1522071820081-009f0129c71c?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80"),
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (E-Learning Streamlit Project)"
}


def backup_csv():
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = BACKUP_DIR / f"courses.csv.bak.{ts}"
    shutil.copy2(COURSES_CSV, bak)
    print("Backup created:", bak)
    return bak


def download_image(url: str, dest: Path) -> bool:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20, stream=True)
        resp.raise_for_status()
        # write file
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("Saved:", dest)
        return True
    except Exception as e:
        print("Failed to download:", url, "->", e)
        if dest.exists():
            try:
                dest.unlink()
            except Exception:
                pass
        return False


def update_csv_for_downloads(success_map):
    # load and update CSV
    df = pd.read_csv(COURSES_CSV, dtype=str).fillna("")
    changed = 0
    for title, (fname, _) in IMAGE_MAP.items():
        if success_map.get(title):
            local = str((THUMB_DIR / fname).as_posix())
            # match by exact title
            mask = df['title'].astype(str).str.strip() == title
            if mask.any():
                df.loc[mask, 'thumbnail'] = local
                changed += int(mask.sum())
            else:
                print("Warning: title not found in CSV:", title)
    if changed:
        df.to_csv(COURSES_CSV, index=False, encoding="utf-8")
        print(f"Updated {changed} rows in {COURSES_CSV}")
    else:
        print("No CSV rows changed (titles not found or downloads failed).")


def main():
    if not COURSES_CSV.exists():
        print("ERROR: courses CSV not found at", COURSES_CSV)
        sys.exit(1)

    print("Starting thumbnail downloads...")
    backup_csv()

    success = {}
    for title, (fname, url) in IMAGE_MAP.items():
        dest = THUMB_DIR / fname
        # skip if already exists
        if dest.exists():
            print("Already exists, skipping:", dest)
            success[title] = True
            continue
        ok = download_image(url, dest)
        success[title] = ok

    # Update CSV with local paths for successful downloads
    update_csv_for_downloads(success)
    print("Done.")


if __name__ == "__main__":
    main()
