import streamlit as st

from src.components.sidebar_visu import sidebar
from src.utils import keep_session_state_between_pages, init_session_state
from src.dataset import visualize_audio

def main() -> None:
    init_session_state()
    keep_session_state_between_pages(key_suffix='')

    st.title("Audio Visualizer 🎤")

    sidebar()
    visualize_audio()

if __name__ == "__main__":
    main()