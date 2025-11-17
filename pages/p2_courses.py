# pages/p2_courses.py
import streamlit as st
import os
import math
import base64
import urllib.parse
from utils.ui import set_logo_and_style, course_card_html, topbar_html
from utils.data_io import load_courses, load_enrollments, enroll

PAGE_SIZE_OPTIONS = [6, 9, 12]


def _svg_placeholder_dataurl(label="No image"):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="360">
      <rect width="100%" height="100%" fill="#F1F5F9"/>
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#64748B" font-family="Arial, sans-serif" font-size="22">{label}</text>
    </svg>'''
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)


def _choose_thumb(thumb, title):
    try:
        if thumb and isinstance(thumb, str) and thumb.strip():
            if os.path.exists(thumb):
                return thumb
            return thumb  # assume URL
    except Exception:
        pass
    return _svg_placeholder_dataurl(label=(title[:30] or "No image"))


def get_popularity_map():
    try:
        enrolls = load_enrollments()
        if enrolls.empty:
            return {}
        counts = enrolls['course_id'].value_counts().to_dict()
        return {int(k): int(v) for k, v in counts.items()}
    except Exception:
        return {}


def app(user=None):
    set_logo_and_style()

    # Topbar
    st.markdown(topbar_html(user.get("username")
                if user else None), unsafe_allow_html=True)
    st.title("📚 Courses")
    st.caption("Browse the catalog, preview, download, and enroll.")

    courses = load_courses()
    if courses.empty:
        st.info("No courses available.")
        return

    df = courses.copy().reset_index(drop=True)

    # Controls with unique keys
    q = st.text_input("Search courses (title or instructor)",
                      key="course_search")
    sort_opt = st.selectbox(
        "Sort", ["Newest", "Title A→Z", "Instructor"], index=0, key="course_sort")
    page_size = st.selectbox(
        "Per page", PAGE_SIZE_OPTIONS, index=0, key="course_per_page")

    # Filter
    if q:
        df = df[
            df['title'].str.contains(q, case=False, na=False) |
            df['instructor'].str.contains(q, case=False, na=False)
        ]

    # Sort
    if sort_opt == "Title A→Z":
        df = df.sort_values("title")
    elif sort_opt == "Instructor":
        df = df.sort_values("instructor", na_position="last")

    popularity_map = get_popularity_map()

    # Pagination state
    total = len(df)
    total_pages = max(1, math.ceil(total / page_size))
    if "page" not in st.session_state:
        st.session_state.page = 1

    # Top pagination controls
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        if st.button("◀ Prev", key="top_prev") and st.session_state.page > 1:
            st.session_state.page -= 1
    with col3:
        if st.button("Next ▶", key="top_next") and st.session_state.page < total_pages:
            st.session_state.page += 1
    with col2:
        st.markdown(
            f"**Page {st.session_state.page} of {total_pages}** — {total} courses")

    # Page slice
    start = (st.session_state.page - 1) * page_size
    end = start + page_size
    page_df = df.iloc[start:end]

    # 3-column responsive grid
    cols = st.columns(3, gap="large")
    for idx, (_, row) in enumerate(page_df.iterrows()):
        with cols[idx % 3]:
            course_id = int(row["id"])
            title = row.get("title") or "Untitled Course"
            desc = row.get("description") or ""
            thumb = row.get("thumbnail")
            asset = row.get("asset_path")
            thumb_url = _choose_thumb(thumb, title)

            badges = ""
            if start + idx < 3:
                badges += '<span class="badge badge-new">NEW</span>'
            if popularity_map.get(course_id, 0) > 0:
                badges += ' <span class="badge badge-pop">POPULAR</span>'

            st.markdown(course_card_html(title=title, description=desc,
                        thumbnail_url=thumb_url, badges_html=badges), unsafe_allow_html=True)

            # Asset download/open
            if asset and isinstance(asset, str) and asset.strip():
                try:
                    # If asset is a local path
                    if os.path.exists(asset):
                        with open(asset, "rb") as f:
                            data = f.read()
                        st.download_button("📥 Download PDF", data=data, file_name=os.path.basename(
                            asset), mime="application/pdf", key=f"dl-{course_id}")
                        if len(data) <= 5 * 1024 * 1024:
                            b64 = base64.b64encode(data).decode("utf-8")
                            href = f'<a href="data:application/pdf;base64,{b64}" target="_blank">🔗 Open</a>'
                            st.markdown(href, unsafe_allow_html=True)
                        else:
                            st.caption("Large file — use Download.")
                    else:
                        # assume it's a URL (Backblaze)
                        st.markdown(
                            f"[📥 Download]({asset})", unsafe_allow_html=True)
                        st.markdown(
                            f'<a href="{asset}" target="_blank">🔗 Open in new tab</a>', unsafe_allow_html=True)
                except Exception:
                    st.caption("Asset not available")

            # Enroll button (unique key)
            enroll_key = f"enroll-{course_id}-{start}-{idx}"
            if st.button("Enroll", key=enroll_key):
                if not user:
                    st.error("Please log in to enroll.")
                else:
                    try:
                        uid = int(user.get("id")) if isinstance(
                            user, dict) else int(user)
                    except Exception:
                        st.error("Invalid user session; re-login.")
                        continue
                    ok = enroll(uid, course_id)
                    if ok:
                        st.success("Enrolled successfully.")
                        st.rerun()
                    else:
                        st.error("Enrollment failed.")

    # Bottom pagination
    b1, b2, b3 = st.columns([1, 3, 1])
    with b1:
        if st.button("◀ Prev (bottom)", key="bottom_prev") and st.session_state.page > 1:
            st.session_state.page -= 1
    with b3:
        if st.button("Next ▶ (bottom)", key="bottom_next") and st.session_state.page < total_pages:
            st.session_state.page += 1

    st.markdown("---")
