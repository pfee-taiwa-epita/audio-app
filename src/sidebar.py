import streamlit as st

def label_filter() -> None:
    if 'label_name' not in st.session_state:
        st.session_state['label_name'] = st.session_state['label_options'][0]

    label_name = st.selectbox("Label de l'enregistrement ✍🏻", st.session_state['label_options'], key='label_name')


def sample_value() -> None:
    if 'sample_value' not in st.session_state:
        st.session_state['sample_value'] = 2
    number_input_value = st.number_input("Nombre de sample 🧮", key='sample_value', min_value=1, max_value=1000)

def debug_information() -> None:
    st.write("# Debug Information 🐜")
    st.write("## Session State")

    st.write(st.session_state)

def default_sidebar() -> None:
    with st.sidebar:
        label_filter()
        sample_value()
        