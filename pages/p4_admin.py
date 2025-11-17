# pages/p4_admin.py
import streamlit as st
from utils.ui import set_logo_and_style, topbar_html
from utils.data_io import add_course
from utils.backblaze import upload_fileobj


def app(user=None):
    set_logo_and_style()
    st.markdown(topbar_html(user.get("username")
                if user else None), unsafe_allow_html=True)
    st.title("🛠 Admin — Add a new course")

    # Role guard
    role = None
    if isinstance(user, dict):
        role = user.get("role")
    if role != "admin":
        st.error("You must be an admin to access this page.")
        return

    st.subheader("Course details")
    title = st.text_input("Course title", key="admin_title")
    description = st.text_area("Description", height=160, key="admin_desc")
    instructor = st.text_input("Instructor name", key="admin_instr")

    st.markdown("**Upload assets**")
    thumbnail = st.file_uploader(
        "Thumbnail (jpg/png)", type=["jpg", "jpeg", "png"], key="admin_thumb")
    pdf_file = st.file_uploader("Course PDF", type=["pdf"], key="admin_pdf")

    if st.button("Add course", key="admin_add"):
        if not title.strip():
            st.error("Please provide a course title.")
            st.stop()

        thumbnail_url = ""
        pdf_url = ""

        # Upload thumbnail (if provided)
        if thumbnail is not None:
            try:
                filename = f"thumbnails/{thumbnail.name}"
                # Streamlit's UploadedFile supports .read() and .seek()
                url = upload_fileobj(thumbnail, filename)
                if url:
                    thumbnail_url = url
                    st.success("Thumbnail uploaded.")
                else:
                    st.warning(
                        "Thumbnail upload returned no URL; saved locally (or failed).")
            except Exception as e:
                st.error(f"Thumbnail upload error: {e}")

        # Upload PDF (if provided)
        if pdf_file is not None:
            try:
                filename = f"pdfs/{pdf_file.name}"
                url = upload_fileobj(pdf_file, filename)
                if url:
                    pdf_url = url
                    st.success("PDF uploaded.")
                else:
                    st.warning(
                        "PDF upload returned no URL; saved locally (or failed).")
            except Exception as e:
                st.error(f"PDF upload error: {e}")

        # Save course record (thumbnail_url/pdf_url may be URLs or local paths)
        try:
            new_id = add_course(
                title=title.strip(),
                description=description.strip(),
                instructor=instructor.strip(),
                thumbnail=thumbnail_url or "",
                asset_path=pdf_url or ""
            )
            st.success(f"Course added (id={new_id}).")
        except Exception as e:
            st.error(f"Failed to save course: {e}")
