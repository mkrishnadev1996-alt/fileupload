import streamlit as st
import os
from pathlib import Path
from datetime import datetime

# ----------------------------
# Configuration
# ----------------------------

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Hardcoded credentials (Demo only)
USERNAME = "admin"
PASSWORD = "password123"

# ----------------------------
# Authentication
# ----------------------------

def login():
    st.title("🔐 Simple Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid credentials")

def logout():
    st.session_state.authenticated = False
    st.rerun()

# ----------------------------
# File Upload
# ----------------------------

def upload_file():
    st.header("📤 Upload File")

    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        save_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        st.rerun()

# ----------------------------
# File List + Download + Delete
# ----------------------------

def list_files():
    st.header("📂 Uploaded Files")

    files = os.listdir(UPLOAD_FOLDER)

    if not files:
        st.info("No files uploaded yet.")
        return

    for file_name in files:
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        # Get timestamp
        timestamp = os.path.getmtime(file_path)
        upload_time = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

        with col1:
            st.write(f"**{file_name}**")

        with col2:
            st.write(f"🕒 {upload_time}")

        with col3:
            with open(file_path, "rb") as f:
                st.download_button(
                    label="Download",
                    data=f,
                    file_name=file_name,
                    key=f"download_{file_name}"
                )

        with col4:
            if st.button("❌", key=f"delete_{file_name}"):
                os.remove(file_path)
                st.success(f"{file_name} deleted")
                st.rerun()

# ----------------------------
# Main App
# ----------------------------

def main():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        login()
    else:
        st.sidebar.button("Logout", on_click=logout)
        st.title("📁 File Storage App")

        upload_file()
        list_files()

if __name__ == "__main__":
    main()