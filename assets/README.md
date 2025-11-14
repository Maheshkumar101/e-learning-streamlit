# E-Learning (Streamlit) — Mini Project

Simple Streamlit-based e-learning demo.  
Structure:

- `streamlit_app.py` — entrypoint + navigation
- `pages/` — app pages (p1_home, p2_courses, p3_my_courses, p4_admin)
- `utils/` — helper modules (auth, data_io, ui, backblaze)
- `data/` — CSVs (ignored by git)

## Quick start (Windows)

1. `python -m venv .venv`
2. `.venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. `streamlit run streamlit_app.py`

## Test accounts

- admin_user / adminpass (admin)
- student_user / studentpass (student)

## Notes

- `data/*.csv` is ignored. Use `data/sample_*.csv` for demo data if you want to track it in git.
- Backblaze S3 support available — configure via `.env`.
