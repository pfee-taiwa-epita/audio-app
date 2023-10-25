import streamlit as st
import os

from src.sidebar import default_sidebar
from src.central import default_central
from src.utils import keep_session_state_between_pages
from src.dataset import download_dataset, clear_data_info

st.set_page_config(
    page_title='Audio Sampler V2',
    page_icon="🎤",
    layout='wide',
    initial_sidebar_state='expanded',
)

def init_session_state() -> None:
    if 'label_options' not in st.session_state:
        st.session_state['label_options'] = ["Bouleau", "Chene", "Accacia", "Sapin"]
    if 'wave_output_folder' not in st.session_state:
        st.session_state['wave_output_folder'] = "./records/"
    if 'hugging_face_repo' not in st.session_state:
        st.session_state['hugging_face_repo'] = "PFEE-TxE/audio_sampler"

def create_folder(folder_names) -> None:
    for folder_name in folder_names:
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

def main() -> None:
    init_session_state()
    keep_session_state_between_pages(key_suffix='')
    create_folder(["records", "preprocess"])


    download_dataset()
    st.title("Audio Recorder 🎤")
    
    default_sidebar()

    default_central()


if __name__ == "__main__":
    main()