import os
import tempfile
import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


@st.cache_resource
def google_auth() -> GoogleDrive:
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    return drive

def write_file_to_gdrive(file_name, file_data, metadata) -> None:

    drive = google_auth()
    file = drive.CreateFile({
        'title': file_name,
        # 'date': metadata['date'],
        # 'user': metadata['user'],
        # 'id': metadata['id'],
        # 'timestamp': metadata['timestamp'],
        # 'label': metadata['label']
    })

    temp_file_path = tempfile.mktemp()

    try:
        with open(temp_file_path, 'wb') as temp_file:
            temp_file.write(file_data.getvalue())

        file.SetContentFile(temp_file_path)

        file.Upload()
        st.write("File uploaded to Google Drive")
    finally:
        os.remove(temp_file_path)

def load_all_file():
    drive = google_auth()
    file_list = drive.ListFile({'q': f"'root' in parents and trashed=false"}).GetList()
    for file in file_list:
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        with col1:
            st.write(file['title'])
        with col2:
            if 'Id' in file:
                st.write(file['Id'])
            else:
                st.write("N/A")
        with col3:
            if 'Label' in file:
                st.write(file['Label'])
            else:
                st.write("N/A")
        with col4:
            if 'Date' in file:
                st.write(file['Date'])
            else:
                st.write("N/A")
        with col5:
            if 'User' in file:
                st.write(file['User'])
            else:
                st.write("N/A")
        with col6:
            if 'Timestamp' in file:
                st.write(file['Timestamp'])
            else:
                st.write("N/A")