import streamlit as st

from src.records import record

def change_recording_state() -> None:
    st.session_state['is_recording'] = not st.session_state['is_recording']


def record_button() -> None:
    st.button("Start Recording", on_click=change_recording_state, disabled=st.session_state['user_name'] == "")
        
def default_central() -> None:
    record_button()

    if st.session_state['is_recording']:
        record(st.session_state['label_name'], 
               st.session_state['sample_value'])