import streamlit as st

from src.records import record

def init_state():
    if 'is_recording' not in st.session_state:
        st.session_state['is_recording'] = False

def change_recording_state():
    st.session_state['is_recording'] = not st.session_state['is_recording']


def record_button():
    button = st.button("Start Recording", on_click=change_recording_state, disabled=st.session_state['is_recording'])

def show_audio_files():
    # show all the file for the selected label if there is any

    st.title("Audio Files 🎙 for " + st.session_state['label_name'])

    if st.session_state['label_name'] in st.session_state['audio_files']:
        i = 0
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.write("Name")
        with col2:
            st.write("Audio")
        with col3:
            st.write("Delete")
        with col4:
            st.write("ID")
        for file_name, audio_data, _, _, id, _ in st.session_state['audio_files'][st.session_state['label_name']]:
            col1, col2, col3, col4 = st.columns(4)
            i += 1
            with col1:
                st.write(st.session_state['label_name'] + "-" + str(i))
            with col2:
                st.audio(audio_data, format='audio/wav', start_time=0)
            with col3:
                # delete the file
                if st.button("Delete", key=file_name):
                    st.session_state['audio_files'][st.session_state['label_name']].remove((file_name, audio_data))
            with col4:
                st.write(id)
    else:
        st.write("No audio files for this label")
        

def default_central():
    init_state()

    record_button()

    if st.session_state['is_recording']:
        record(st.session_state['label_name'], 
               st.session_state['sample_value'])
        
    show_audio_files()