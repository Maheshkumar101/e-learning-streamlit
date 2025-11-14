# pages/p1_home.py
import streamlit as st
import os
import urllib.parse
from utils.ui import set_logo_and_style, course_card_html, topbar_html
from utils.data_io import load_courses


def _svg_placeholder_dataurl(label="No image"):
    # simple gray SVG with label centered
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="360">
      <rect width="100%" height="100%" fill="#F1F5F9"/>
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#64748B" font-family="Arial, sans-serif" font-size="26">{label}</text>
    </svg>'''
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)


def _choose_thumb(thumb, title):
    if thumb and isinstance(thumb, str) and thumb.strip():
        # local file?
        try:
            if os.path.exists(thumb):
                return thumb
        except Exception:
            pass
        # otherwise assume thumb is URL
        return thumb
    # fallback placeholder with title as label
    return _svg_placeholder_dataurl(label=title[:30] or "No image")


def app(user=None):
    set_logo_and_style()
    st.markdown(topbar_html(user.get("username")
                if user else None), unsafe_allow_html=True)

    st.title("Welcome to E-Learn")
    st.write(
        "A small e-learning demo — browse courses, enroll, and download materials.")

    courses = load_courses()
    if courses.empty:
        st.info("No courses available yet. Ask an admin to add courses in Admin page.")
        return

    st.header("Featured courses")
    featured = courses.head(4).reset_index(drop=True)
    cols = st.columns(2, gap="large")
    for i, (_, row) in enumerate(featured.iterrows()):
        col = cols[i % 2]
        title = row.get("title") if hasattr(row, "get") else row["title"]
        desc = row.get("description") if hasattr(
            row, "get") else row["description"]
        thumb = row.get("thumbnail") if hasattr(
            row, "get") else row["thumbnail"]
        thumb_url = _choose_thumb(thumb, title)
        with col:
            st.markdown(course_card_html(title=title, description=desc,
                        thumbnail_url=thumb_url), unsafe_allow_html=True)
