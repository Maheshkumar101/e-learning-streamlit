# pages/p3_my_courses.py
import streamlit as st
import os
import base64
import urllib.parse
from utils.ui import set_logo_and_style, course_card_html, topbar_html
from utils.data_io import my_courses_for_user


def _svg_placeholder_dataurl(label="No image"):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="360">
      <rect width="100%" height="100%" fill="#F1F5F9"/>
      <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" fill="#64748B" font-family="Arial, sans-serif" font-size="22">{label}</text>
    </svg>'''
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg)


def _choose_thumb(thumb, title):
    if thumb and isinstance(thumb, str) and thumb.strip():
        try:
            if os.path.exists(thumb):
                return thumb
        except Exception:
            pass
        return thumb
    return _svg_placeholder_dataurl(label=(title[:30] or "No image"))


def app(user=None):
    set_logo_and_style()
    st.markdown(topbar_html(user.get("username")
                if user else None), unsafe_allow_html=True)

    st.title("🎓 My Courses")

    if not user:
        st.info("Please log in to see your enrolled courses.")
        return

    try:
        uid = int(user.get("id")) if isinstance(user, dict) else int(user)
    except Exception:
        st.error("Invalid user id. Please re-login.")
        return

    df = my_courses_for_user(uid)
    if df.empty:
        st.info("You haven't enrolled in any courses yet.")
        return

    # Show as grid (2 columns)
    cols = st.columns(2, gap="large")
    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i % 2]:
            title = row.get("title")
            desc = row.get("description")
            thumb = row.get("thumbnail")
            asset = row.get("asset_path")
            thumb_url = _choose_thumb(thumb, title)
            st.markdown(course_card_html(title=title, description=desc,
                        thumbnail_url=thumb_url), unsafe_allow_html=True)

            if asset and isinstance(asset, str) and asset.strip() and os.path.exists(asset):
                try:
                    with open(asset, "rb") as f:
                        data = f.read()
                    st.download_button("📥 Download PDF", data=data, file_name=os.path.basename(
                        asset), mime="application/pdf", key=f"mydl-{row['id']}")
                    if len(data) <= 5 * 1024 * 1024:
                        b64 = base64.b64encode(data).decode("utf-8")
                        href = f'<a href="data:application/pdf;base64,{b64}" target="_blank">🔗 Open PDF in new tab</a>'
                        st.markdown(href, unsafe_allow_html=True)
                    else:
                        st.caption("Large file; please download to open.")
                except Exception:
                    st.warning("Unable to open attached file.")
