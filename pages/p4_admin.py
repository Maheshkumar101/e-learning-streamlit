# pages/p4_admin.py
import streamlit as st
from utils.data_io import add_course
from utils.backblaze import upload_fileobj
from utils.ui import set_logo_and_style


def app(user=None):
    set_logo_and_style()

    st.title("🛠 Admin – Add New Course")

    if not user or user.get("role") != "admin":
        st.error("You must be an admin to access this page.")
        return

    st.subheader("Create a Course")

    title = st.text_input("Course Title")
    description = st.text_area("Description", height=120)
    instructor = st.text_input("Instructor Name")

    thumbnail = st.file_uploader(
        "Upload Thumbnail (jpg/png)", type=["jpg", "jpeg", "png"])
    pdf_file = st.file_uploader("Upload Course PDF", type=["pdf"])

    if st.button("Add Course", use_container_width=True):
        if not title or not description or not instructor:
            st.error("Please fill in all fields.")
            return

        thumbnail_url = ""
        pdf_url = ""

        # ------------------------ Upload Thumbnail -------------------------
        if thumbnail:
            try:
                filename = f"thumbnails/{thumbnail.name}"
                thumbnail_url = upload_fileobj(thumbnail, filename)
                st.success("Thumbnail uploaded successfully!")
            except Exception as e:
                st.error(f"Failed to upload thumbnail: {e}")

        # ------------------------ Upload PDF -------------------------------
        if pdf_file:
            try:
                filename = f"pdfs/{pdf_file.name}"
                pdf_url = upload_fileobj(pdf_file, filename)
                st.success("PDF uploaded successfully!")
            except Exception as e:
                st.error(f"Failed to upload PDF: {e}")

        # ------------------------ Save to CSV ------------------------------
        try:
            new_id = add_course(
                title=title,
                description=description,
                instructor=instructor,
                thumbnail=thumbnail_url,
                asset_path=pdf_url
            )
            st.success(f"Course '{title}' added successfully! (ID: {new_id})")
        except Exception as e:
            st.error(f"Error saving course: {e}")
