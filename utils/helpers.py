# utils/helpers.py
import streamlit as st


def initialize_session_state():
    """Initializes all necessary session state variables."""
    defaults = {
        "token": "",
        "history": [],
        "username": "",
        "email": "",
        "timezone": "",
        "page_selection": "Login", 
        "show_profile": False,
        "prompt_submitted": False, 
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def reset_chat():
    """Resets the chat history."""
    st.session_state.history = []
    st.toast("Chat history cleared!", icon="✔️")

def logout():
    """Logs the user out by clearing session state."""
    keys_to_clear = ["token", "history", "username", "email", "timezone", "show_profile", "prompt_submitted"]
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]
    initialize_session_state() 

def toggle_profile():
    """Toggles the profile visibility in the sidebar."""
    st.session_state.show_profile = not st.session_state.show_profile


def handle_suggestion_click(prompt_text):
    """
    This callback is triggered when a suggestion button is clicked.
    It adds the prompt directly to the chat history and triggers a rerun.
    """
    st.session_state.history.append({"type": "human", "content": prompt_text})
    # We don't need to call st.rerun() here. After a callback,
    # Streamlit automatically reruns the script from the top.