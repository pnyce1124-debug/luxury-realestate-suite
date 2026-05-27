import streamlit as st
import requests
from openai import OpenAI

# Set up the Streamlit page view layout for tablet and web compliance
st.set_page_config(page_title="Luxury Real Estate Marketing Suite", layout="wide")

# Initialize persistent memory states for tablet session stability
if "luxury_text" not in st.session_state:
    st.session_state.luxury_text = ""
if "image_url" not in st.session_state:
    st.session_state.image_url = None
