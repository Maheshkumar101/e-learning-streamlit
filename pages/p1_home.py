# pages/p1_home.py
import streamlit as st
import os
import urllib.parse
from utils.ui import set_logo_and_style, course_card_html, topbar_html
from utils.data_io import load_courses


def _svg_placeholder_dataurl(label="No image"):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="450">
      <rect width="100%" height="100%" fill="#F1F5F9"/>
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#64748B" font-family="Arial, sans-serif" font-size="28">{label}</text>
    </svg>'''
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)


def _choose_thumb(thumb, title):
    # safe coercion and fallback to SVG placeholder with course title
    try:
        if thumb and isinstance(thumb, str) and thumb.strip():
            # prefer local file if exists
            if os.path.exists(thumb):
                return thumb
            # else assume it's a URL
            return thumb
    except Exception:
        pass
    # fallback
    return _svg_placeholder_dataurl(label=(title[:28] or "No image"))


def app(user=None):
    set_logo_and_style()
    st.markdown(topbar_html(user.get("username")
                if user else None), unsafe_allow_html=True)

    st.title("Welcome to E-Learn")
    st.write("Browse featured courses or go to Courses to see the full catalog.")

    courses = load_courses()
    if courses.empty:
        st.info("No courses available yet. Admin can add courses from the Admin page.")
        return

    featured = courses.head(4).reset_index(drop=True)
    cols = st.columns(2, gap="large")
    for i, (_, row) in enumerate(featured.iterrows()):
        col = cols[i % 2]
        title = row.get("title") or "Untitled Course"
        desc = row.get("description") or ""
        thumb = row.get("thumbnail") if "thumbnail" in row else None
        thumb_url = _choose_thumb(thumb, title)
        with col:
            st.markdown(course_card_html(title=title, description=desc,
                        thumbnail_url=thumb_url), unsafe_allow_html=True)
