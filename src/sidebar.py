import streamlit as st

from src.gdrive import google_auth


def label_filter():
    if 'label_name' not in st.session_state:
        st.session_state['label_name'] = st.session_state['label_options'][0]

    label_name = st.selectbox("Label de l'enregistrement ✍🏻", st.session_state['label_options'], key='label_name')


def sample_value():
    if 'sample_value' not in st.session_state:
        st.session_state['sample_value'] = 1
    number_input_value = st.number_input("Nombre de sample 🧮", key='sample_value', min_value=1, max_value=1000)

def debug_information():
    st.write("# Debug Information 🐜")
    st.write("## Session State")

    st.write(st.session_state)

def default_sidebar():
    with st.sidebar:
        label_filter()
        sample_value()

        #disable for now
        #google_auth()

        debug_information()




