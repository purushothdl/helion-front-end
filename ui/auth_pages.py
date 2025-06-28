# ui/auth_pages.py
import streamlit as st
import requests
import time
from config import API_BASE_URL

def render_auth_page():
    """Renders the styled authentication page with login/register tabs."""
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div class="auth-container">
            <div class="auth-logo">⚡</div>
            <h1 class="auth-title">Helion Energy</h1>
            <p class="auth-subtitle">Intelligent Scheduling Portal</p>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔑  Sign In", "✨  Create Account"])
        with tab1:
            _render_login_form()
        with tab2:
            _render_register_form()

def _render_login_form():
    """Renders the login form within the styled layout."""
    with st.form("login_form"):
        email = st.text_input("Email", placeholder="your.email@helion.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Sign In Securely", use_container_width=True, type="primary")

        if submitted:
            if not email or not password:
                st.error("Please provide both email and password.")
                return
            try:
                login_data = {"username": email, "password": password}
                response = requests.post(f"{API_BASE_URL}/auth/login", data=login_data)
                if response.status_code == 200:
                    st.session_state.token = response.json()["access_token"]
                    headers = {"Authorization": f"Bearer {st.session_state.token}"}
                    me_response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)
                    if me_response.status_code == 200:
                        user = me_response.json()
                        st.session_state.username = user.get("username", "user")
                        st.session_state.email = user.get("email", email)
                        st.session_state.timezone = user.get("timezone", "UTC")
                    st.success("✅ Login successful! Welcome back.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error(f"Login failed: {response.json().get('detail', 'Invalid credentials')}")
            except requests.RequestException as e:
                st.error(f"Connection failed: {e}")

def _render_register_form():
    """
    Renders the registration form with Username, Email, and Password.
    This version is integrated into the styled layout.
    """
    with st.form("register_form"):
        st.markdown("Join the future of energy scheduling.")
        
        username = st.text_input("Username", placeholder="Choose a public username")
        email = st.text_input("Email", placeholder="your.email@helion.com")
        password = st.text_input("Password", type="password", placeholder="Choose a secure password")
        
        submitted = st.form_submit_button("Create Account", use_container_width=True)

        if submitted:
            if not all([username, email, password]):
                st.warning("Please fill out all fields.")
                return

            try:

                register_data = {"username": username, "password": password, "email": email}
                response = requests.post(f"{API_BASE_URL}/auth/register", json=register_data)
                
                if response.status_code in [200, 201]:
                    st.success("✅ Account created! Please proceed to the 'Sign In' tab to log in.")
                else:
                    st.error(f"Registration failed: {response.json().get('detail', 'Could not create account.')}")
            except requests.RequestException as e:
                st.error(f"Connection failed: {e}")