import streamlit as st

from src.dataloader import button_refresh_data

def label_filter_visu() -> None:
    st.multiselect("Label(s) ✍🏻", st.session_state['label_options'], key='label_name_visu')

def user_name_filter_visu() -> None:
    user_name_list = st.session_state['data']['user_name'].unique().tolist()
    user_name_list = [x.replace("_", " ").title() for x in user_name_list]

    st.multiselect("Utilisateur(s) 🧑🏻‍💻", user_name_list, key='user_name_visu')

def sidebar() -> None:
    with st.sidebar:
        label_filter_visu()
        user_name_filter_visu()
        button_refresh_data()