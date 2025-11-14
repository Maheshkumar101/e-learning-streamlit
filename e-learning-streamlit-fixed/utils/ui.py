# utils/ui.py
import streamlit as st
import html
from pathlib import Path


def set_logo_and_style():
    """Inject CSS for the global app look and the topbar."""
    st.markdown(
        """
        <style>
        /* Page background & base font */
        body, .stApp {
            background: #F7FAFC !important;
            color: #0F172A !important;
            font-family: Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
        }

        /* Topbar */
        .topbar {
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding: 12px 20px;
            border-bottom: 1px solid rgba(15,23,42,0.06);
            background: linear-gradient(90deg, rgba(37,99,235,0.06), rgba(6,182,212,0.03));
            margin-bottom: 18px;
            position: sticky;
            top: 0;
            z-index: 999;
        }
        .topbar-left { display:flex; gap:12px; align-items:center; }
        .app-title { font-weight:800; font-size:22px; color:#0F172A; margin:0; }
        .app-sub { color:#475569; font-size:12px; margin:0; }

        /* Avatar */
        .avatar {
            width:40px; height:40px; border-radius:10px; display:inline-flex;
            align-items:center; justify-content:center; font-weight:700;
            background: linear-gradient(135deg,#06B6D4,#2563EB); color:white;
            box-shadow: 0 6px 18px rgba(37,99,235,0.08);
        }

        /* Course card */
        .course-card {
            padding:14px;
            border-radius:12px;
            background: linear-gradient(180deg, #FFFFFF, #FBFDFF);
            border: 1px solid rgba(15,23,42,0.04);
            box-shadow: 0 6px 18px rgba(2,6,23,0.02);
            height:100%;
            display:flex;
            flex-direction:column;
            justify-content:space-between;
        }
        .course-title { font-size:18px; font-weight:700; color:#0F172A; margin-bottom:6px; }
        .course-desc { color:#475569; font-size:14px; margin-bottom:10px; min-height:44px; }
        .card-footer { display:flex; justify-content:space-between; align-items:center; margin-top:12px; }

        /* Badge styles */
        .badge {
            display:inline-block;
            padding:6px 10px;
            border-radius:999px;
            font-size:12px;
            font-weight:700;
            color:white;
            margin-left:6px;
        }
        .badge-new { background: #10B981; }     /* green */
        .badge-pop { background: #F97316; }     /* orange */

        /* Buttons */
        .stButton button {
            background: linear-gradient(180deg,#2563EB,#0B5ED7) !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 8px 12px !important;
            font-weight:700 !important;
            box-shadow: none !important;
        }

        /* Inputs rounded */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            border-radius:10px !important;
            border: 1px solid rgba(15,23,42,0.06) !important;
        }

        /* Make grid wrapper spacing nicer */
        .grid-wrap { display:block; gap:18px; }

        </style>
        """,
        unsafe_allow_html=True,
    )


def course_card_html(title, description, thumbnail_url=None, badges_html=""):
    """
    Return HTML string for a styled course card.
    - title: plain text
    - description: plain text
    - thumbnail_url: optional image URL or local path
    - badges_html: small HTML snippet for badges (can be empty)
    """
    t = html.escape(str(title))
    d = html.escape(str(description))

    thumb_tag = ""
    if thumbnail_url:
        thumb_tag = f'<div style="margin-bottom:10px"><img src="{html.escape(thumbnail_url)}" style="width:100%;border-radius:8px;object-fit:cover;max-height:140px"/></div>'

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
      <div class="card-footer"></div>
    </div>
    """
    return html_block


def course_card(title, description, thumbnail_url=None, badges_html=""):
    """Render a card via Streamlit markdown."""
    st.markdown(course_card_html(title, description, thumbnail_url,
                badges_html), unsafe_allow_html=True)


def topbar_html(username=None):
    display = (username[0].upper() if username else "G")
    user_label = html.escape(username) if username else "Guest"
    html_block = f"""
    <div class="topbar">
      <div class="topbar-left">
        <img src="https://img.icons8.com/fluency/48/000000/books.png" style="height:34px;margin-right:6px" />
        <div>
          <div class="app-title">E-Learn</div>
          <div class="app-sub">Learn anything — fast</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:12px">
        <div style="text-align:right">
          <div class="avatar">{display}</div>
          <div style="font-size:12px;color:#475569;margin-top:6px">{user_label}</div>
        </div>
      </div>
    </div>
    """
    return html_block
