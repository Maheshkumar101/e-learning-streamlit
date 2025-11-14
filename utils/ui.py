# utils/ui.py
import streamlit as st
import html
from pathlib import Path

# Optional default thumbnail (data URL or remote image); leave empty to disable
DEFAULT_THUMBNAIL = "https://img.icons8.com/fluency/240/000000/open-book.png"


def set_logo_and_style():
    """Inject CSS for global app look and topbar."""
    st.markdown(
        """
        <style>
        body, .stApp { background: #F7FAFC !important; color: #0F172A !important; font-family: Inter, Arial, sans-serif; }
        .topbar { display:flex; justify-content:space-between; align-items:center; padding:12px 20px; border-bottom:1px solid rgba(15,23,42,0.06); margin-bottom:16px; background: linear-gradient(90deg, rgba(37,99,235,0.03), rgba(6,182,212,0.02)); }
        .app-title { font-weight:800; font-size:20px; margin:0; color:#0F172A; }
        .avatar { width:36px; height:36px; border-radius:8px; display:inline-flex; align-items:center; justify-content:center; background:linear-gradient(135deg,#06B6D4,#2563EB); color:white; font-weight:700; }
        .course-card { padding:14px; border-radius:12px; background:#fff; border:1px solid rgba(15,23,42,0.04); box-shadow:0 6px 18px rgba(2,6,23,0.02); }
        .course-title { font-size:16px; font-weight:700; color:#0F172A; margin-bottom:6px; }
        .course-desc { color:#475569; font-size:13px; margin-bottom:12px; min-height:44px; }
        .badge { display:inline-block; padding:6px 10px; border-radius:999px; font-size:12px; font-weight:700; color:white; margin-left:6px; }
        .badge-new { background:#10B981; } .badge-pop { background:#F97316; }
        .stButton button { background: linear-gradient(180deg,#2563EB,#0B5ED7) !important; color:white !important; border-radius:10px !important; padding:8px 12px !important; font-weight:700 !important; }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea { border-radius:8px !important; border:1px solid rgba(15,23,42,0.06) !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _coerce_to_str(x):
    """
    Safely convert thumbnail-like values into a usable string.
    Returns empty string if value is None, NaN, empty, or not suitable.
    """
    if x is None:
        return ""
    # If Path, cast to str
    if isinstance(x, Path):
        return str(x)
    # Try string conversion
    try:
        s = str(x)
    except Exception:
        return ""
    if not s:
        return ""
    # common representations of missing values
    if s.strip().lower() in {"nan", "none", "null", "<na>"}:
        return ""
    return s


def _choose_thumbnail_src(thumb_candidate: str):
    """
    If thumb_candidate is a local file that exists, return that path.
    Otherwise, if it's a non-empty string, return it (assume URL).
    Otherwise return default thumbnail (if set) or empty string.
    """
    if not thumb_candidate:
        return DEFAULT_THUMBNAIL or ""
    # prefer local files if they exist
    try:
        p = Path(thumb_candidate)
        if p.exists():
            return str(p.as_posix())
    except Exception:
        pass
    return thumb_candidate


def course_card_html(title, description, thumbnail_url=None, badges_html=""):
    """
    Return HTML string for a styled course card.
    Safely handles thumbnail values that may be float('nan') from CSVs.
    """
    t = html.escape("" if title is None else str(title))
    d = html.escape("" if description is None else str(description))

    thumb_raw = _coerce_to_str(thumbnail_url)
    thumb_src = _choose_thumbnail_src(thumb_raw)

    thumb_tag = ""
    if thumb_src:
        thumb_tag = f'<div style="margin-bottom:10px"><img src="{html.escape(thumb_src)}" style="width:100%;border-radius:8px;object-fit:cover;max-height:160px" /></div>'

    html_block = f"""
    <div class="course-card">
      <div>
        {thumb_tag}
        <div style="display:flex;align-items:center;gap:8px">
            <div class="course-title">{t}</div>
            <div>{badges_html}</div>
        </div>
        <div class="course-desc">{d}</div>
      </div>
      <div style="margin-top:8px" class="card-footer"></div>
    </div>
    """
    return html_block


def course_card(title, description, thumbnail_url=None, badges_html=""):
    """Render a course card immediately via Streamlit markdown."""
    st.markdown(course_card_html(title, description, thumbnail_url,
                badges_html), unsafe_allow_html=True)


def topbar_html(username=None):
    """Return the topbar HTML with avatar."""
    display = (str(username)[0].upper() if username else "G")
    user_label = html.escape(str(username)) if username else "Guest"
    html_block = f"""
    <div class="topbar">
      <div style="display:flex;align-items:center;gap:12px">
        <img src="https://img.icons8.com/fluency/48/000000/books.png" style="height:30px"/>
        <div>
          <div class="app-title">E-Learn</div>
          <div style="font-size:12px;color:#475569">Learn anything — fast</div>
        </div>
      </div>
      <div style="text-align:right">
        <div class="avatar">{html.escape(display)}</div>
        <div style="font-size:12px;color:#475569;margin-top:6px">{user_label}</div>
      </div>
    </div>
    """
    return html_block
