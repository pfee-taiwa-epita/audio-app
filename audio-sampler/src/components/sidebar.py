import streamlit as st

def label_filter() -> None:
    st.selectbox("Label de l'enregistrement ✍🏻", st.session_state['label_options'], key='label_name')


def sample_value() -> None:
    st.number_input("Nombre de sample 🧮", key='sample_value', min_value=1, max_value=1000)

def user_name() -> None:
    st.text_input("Nom de l'utilisateur 🧑🏻‍💻", key='user_name')

def debug_information() -> None:
    st.write("# Debug Information 🐜")
    st.write("## Session State")

    st.write(st.session_state)

def default_sidebar() -> None:
    with st.sidebar:
        user_name()
        label_filter()
        sample_value()
        