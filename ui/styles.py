# ui/styles.py
import streamlit as st

def load_css():
    """Loads all custom CSS for the styled authentication page."""
    st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling */
    html, body, [class*="st-"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 100%);
    }

    /* --- Auth Page Specific Styling --- */
    .auth-container {
        text-align: center;
        padding-top: 2rem;
    }
    .auth-logo { font-size: 4rem; margin-bottom: 1rem; }
    .auth-title { color: #FFFFFF; font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; }
    .auth-subtitle { color: #667eea; font-weight: 300; }
    
    /* General Streamlit Element Styling for Auth Page*/
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        justify-content: center;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        padding: 10px;
        color: rgba(255, 255, 255, 0.7);
    }
    .stTabs [aria-selected="true"] {
        background: rgba(102, 126, 234, 0.1);
        border-radius: 8px;
        color: white;
    }
    
    /* Input Styling for Auth page */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
        color: white;
    }
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)