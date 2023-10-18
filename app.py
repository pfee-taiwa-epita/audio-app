import streamlit as st

from src.sidebar import default_sidebar
from src.central import default_central

st.set_page_config(
    page_title='Audio Sampler V2',
    page_icon="🎤",
    layout='wide',
    initial_sidebar_state='expanded',
)

def init_session_state():
    if 'label_options' not in st.session_state:
        st.session_state['label_options'] = ["Bouleau", "Chene", "Accacia", "Sapin"]
    if 'audio_files' not in st.session_state:
        st.session_state['audio_files'] = {}

def main():
    st.title("Audio Recorder 🎤")
    init_session_state()
    
    default_sidebar()

    default_central()


if __name__ == "__main__":
    main()