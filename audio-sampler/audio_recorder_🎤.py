import streamlit as st
import os

from src.components.sidebar import default_sidebar
from src.components.central import default_central
from src.utils import keep_session_state_between_pages, init_session_state

st.set_page_config(
    page_title='Audio Sampler V2',
    page_icon="🎤",
    layout='wide',
    initial_sidebar_state='expanded',
)

def create_folder(folder_names) -> None:
    for folder_name in folder_names:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

def main() -> None:
    init_session_state()
    keep_session_state_between_pages(key_suffix='')
    create_folder(["audio/records", "audio/preprocess"])

    st.title("Audio Recorder 🎤")
    
    default_sidebar()

    default_central()


if __name__ == "__main__":
    main()