# scripts/download_images.py
import json
import requests
import os
from pathlib import Path
import pandas as pd
from urllib.parse import urlparse

PROJECT_ROOT = Path('.')
THUMB_DIR = PROJECT_ROOT / 'assets' / 'thumbnails'
COURSES_CSV = PROJECT_ROOT / 'data' / 'courses.csv'
JSON_MAP = PROJECT_ROOT / 'scripts' / 'image_urls.json'

THUMB_DIR.mkdir(parents=True, exist_ok=True)


def filename_from_url(url):
    parsed = urlparse(url)
    name = Path(parsed.path).name
    if not name:
        name = parsed.netloc.replace('.', '_')
    return name


def download(url, outpath):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; E-Learn-Project/1.0; +https://example.local/)"
    }
    try:
        r = requests.get(url, headers=headers, timeout=20)
        r.raise_for_status()
        with open(outpath, 'wb') as f:
            f.write(r.content)
        print(f"Saved {outpath}")
        return True
    except Exception as e:
        print("Failed to download", url, ":", e)
        return False


def load_map():
    if not JSON_MAP.exists():
        print("Missing:", JSON_MAP)
        return {}
    return json.loads(JSON_MAP.read_text(encoding='utf-8'))


def update_courses_csv(mapping):
    if not COURSES_CSV.exists():
        print("Missing courses CSV:", COURSES_CSV)
        return
    df = pd.read_csv(COURSES_CSV, dtype=str).fillna('')
    changed = 0
    for idx, row in df.iterrows():
        title = row.get('title', '')
        if title in mapping and mapping[title]:
            df.at[idx, 'thumbnail'] = str(
                (THUMB_DIR / mapping[title]).as_posix())
            changed += 1
    df.to_csv(COURSES_CSV, index=False, encoding='utf-8')
    print(f"Updated {changed} course thumbnails in {COURSES_CSV}")


def main():
    mapping = load_map()
    if not mapping:
        print("No mapping found in", JSON_MAP)
        return

    # for each mapping entry, download
    local_map = {}
    for title, url in mapping.items():
        if not url:
            print("Skipping", title, "empty URL")
            continue
        fname = filename_from_url(url)
        # avoid query strings in filename
        fname = fname.split('?')[0]
        dest = THUMB_DIR / fname
        if dest.exists():
            print("Already exists:", dest)
            local_map[title] = fname
            continue
        ok = download(url, dest)
        if ok:
            local_map[title] = fname

    # now update CSV to point to downloaded files
    update_courses_csv(local_map)
    print("Done.")


if __name__ == '__main__':
    main()
