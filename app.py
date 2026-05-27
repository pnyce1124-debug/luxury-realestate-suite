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


def generate_luxury_text(details, style, openai_key):
    """
    Uses OpenAI Chat Completions (gpt-4o-mini) to rewrite messy, 
    scraped property bullet points into sophisticated marketing copy.
    """
    try:
        client = OpenAI(api_key=openai_key)
        prompt = (
            f"You are an elite real estate copywriter. Take these property details: '{details}' "
            f"and write a high-end luxury real estate property listing and a matching social media post. "
            f"Optimize the tone to fit a writing style that is: '{style}'. Make it sound sophisticated, "
            f"exclusive, and highly marketable. Include relevant luxury real estate hashtags."
        )
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Text Generation Error: {str(e)}"
