import streamlit as st

from src.dataset import download_dataset

def keep_session_state_between_pages(key_suffix: str) -> None:
    """Keep the session state of the component with the given key suffix between pages.

    This does this by explicitly storing them in the st.session_state as mentioned here:
    https://discuss.streamlit.io/t/multi-page-apps-with-widget-state-preservation-the-simple-way/22303
    """
    st.session_state.update({key: value for key, value in st.session_state.items() if str(key).endswith(key_suffix)})

def init_session_state():
    if 'label_options' not in st.session_state:
        st.session_state['label_options'] = ["Bouleau", "Chene", "Accacia", "Sapin"]
    if 'wave_output_folder' not in st.session_state:
        st.session_state['wave_output_folder'] = "./audio/records/"
    if 'dataset_folder' not in st.session_state:
        st.session_state['dataset_folder'] = "../dataset/"
    if 'hugging_face_repo' not in st.session_state:
        st.session_state['hugging_face_repo'] = "PFEE-TxE/audio_sampler"

    if 'data' not in st.session_state:
        download_dataset()
    if 'preprocess_wave_output_folder' not in st.session_state:
        st.session_state['preprocess_wave_output_folder'] = "./audio/preprocess/"

    if 'is_recording' not in st.session_state:
        st.session_state['is_recording'] = False

    if 'label_name_visu' not in st.session_state:
        st.session_state['label_name_visu'] = []
    if 'user_name_visu' not in st.session_state:
        st.session_state['user_name_visu'] = []

    if 'label_name' not in st.session_state:
        st.session_state['label_name'] = st.session_state['label_options'][0]
    if 'sample_value' not in st.session_state:
        st.session_state['sample_value'] = 10
    if 'user_name' not in st.session_state:
        st.session_state['user_name'] = ""