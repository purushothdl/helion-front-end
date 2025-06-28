import streamlit as st
from utils.helpers import initialize_session_state
from ui.styles import load_css
from ui.auth_pages import render_auth_page
from ui.chat_interface import render_chat_interface

initialize_session_state()

if st.session_state.get("token"):

    render_chat_interface()
else:

    load_css()
    render_auth_page()