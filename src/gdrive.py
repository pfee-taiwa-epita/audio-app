import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def google_auth():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    if st.button("Upload data to Google Drive"):
        for label in st.session_state['audio_files']:
            for filename in label:
                st.write(label + '/' + filename)
                # file = drive.CreateFile({'title': label + '/' +filename})
                # file.SetContentFile(st.session_state['audio_files'][filename])
                # file.Upload()

    st.subheader("Liste des fichiers sur Google Drive :")
    file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file1 in file_list:
        st.write('title: %s, id: %s' % (file1['title'], file1['id']))