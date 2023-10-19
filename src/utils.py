import streamlit as st


def keep_session_state_between_pages(key_suffix: str) -> None:
    """Keep the session state of the component with the given key suffix between pages.

    This does this by explicitly storing them in the st.session_state as mentioned here:
    https://discuss.streamlit.io/t/multi-page-apps-with-widget-state-preservation-the-simple-way/22303
    """
    st.session_state.update({key: value for key, value in st.session_state.items() if str(key).endswith(key_suffix)})