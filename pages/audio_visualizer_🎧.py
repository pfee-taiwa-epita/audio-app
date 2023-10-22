import streamlit as st

from src.sidebar import label_filter
from src.utils import keep_session_state_between_pages
from src.dataset import visualize_audio


def sidebar() -> None:
    with st.sidebar:
        label_filter()

def main() -> None:
    keep_session_state_between_pages(key_suffix='')
    st.title("Audio Visualizer 🎤")
    sidebar()
    visualize_audio()

if __name__ == "__main__":
    main()