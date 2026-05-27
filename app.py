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


def generate_luxury_image(details, openai_key):
    """
    Uses OpenAI's DALL-E 3 model to transform textual details 
    into an Editorial/Architectural Digest style visual graphic asset.
    """
    try:
        client = OpenAI(api_key=openai_key)
        image_prompt = (
            f"High-end luxury real estate photography, architectural digest style, "
            f"bright professional interior lighting, daytime, showcasing a stunning view of: {details[:400]}"
        )
        response = client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1
        )
        return response.data[0].url
    except Exception as e:
        return f"Image Generation Error: {str(e)}"


def publish_to_facebook(message, image_url, page_id, page_token):
    """
    Communicates via HTTP requests with the Meta Graph API v19.0+ 
    to automatically publish text and imagery directly onto a Facebook Page.
    """
    try:
        if image_url:
            # Endpoint designed for uploading photos with text captions
            url = f"https://graph.facebook.com/v19.0/{page_id}/photos"
            payload = {
                "url": image_url,
                "caption": message,
                "access_token": page_token
            }
        else:
            # Fallback endpoint designed for text-only timeline posts
            url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
            payload = {
                "message": message,
                "access_token": page_token
            }
        
        response = requests.post(url, data=payload)
        result = response.json()
        
        if "id" in result:
            return f"🚀 Success! Posted live to Facebook. Post ID: {result['id']}"
        else:
            return f"❌ Meta API Error: {result.get('error', {}).get('message', 'Unknown error')}"
    except Exception as e:
        return f"❌ Connection Error: {str(e)}"


# Create titles and dynamic user instructions
st.title("🏙️ Premium Real Estate AI Marketing Suite")
st.write("Transform raw descriptions into luxury copy and graphics, then auto-post them live.")

# Sidebar architecture for managing secret credentials securely
st.sidebar.header("🔑 Developer & API Settings")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
fb_page_id = st.sidebar.text_input("Facebook Page ID")
fb_page_token = st.sidebar.text_input("Facebook Page Access Token", type="password")

# Core layout columns for input data gathering
st.subheader("1. Enter Property Characteristics")
col_in1, col_in2 = st.columns([2, 1])

with col_in1:
    property_details = st.text_area(
        "Raw Property Details / Scraped Text", 
        placeholder="e.g., 4 bed, 5 bath, infinity pool, marble details, panoramic ocean view in Malibu..."
    )
with col_in2:
    writing_style = st.selectbox(
        "Brand Target Style", 
        ["Ultra-Luxury & Elegant", "Modern & Sleek", "High-Energy & Bold", "Sophisticated & Minimalist"]
    )

# Execution layout pipeline trigger button
if st.button("🔥 Generate All Assets", type="primary", use_container_width=True):
    if not openai_api_key:
        st.error("Please add your OpenAI API Key in the sidebar first!")
    elif not property_details:
        st.error("Please insert property details before running.")
    else:
        with st.spinner("Writing luxury copy and building AI graphics..."):
            # Execute backend generation functions sequentially
            st.session_state.luxury_text = generate_luxury_text(property_details, writing_style, openai_api_key)
            st.session_state.image_url = generate_luxury_image(property_details, openai_api_key)

# Render and Display assets dynamically if they exist within current context
if st.session_state.luxury_text:
    st.markdown("---")
    st.subheader("2. Review Generated Marketing Assets")
    
    col_out1, col_out2 = st.columns(2)
    
    with col_out1:
        st.write("### 📝 Text Listing & Caption")
        # Editable text area so agents can refine the text manually before pushing live
        st.session_state.luxury_text = st.text_area("Edit Copy:", value=st.session_state.luxury_text, height=350)
        
    with col_out2:
        st.write("### 🎨 AI Rendered Visual Asset")
        if st.session_state.image_url and not st.session_state.image_url.startswith("Image"):
            st.image(st.session_state.image_url, caption="Generated Visual Graphic", use_container_width=True)
        else:
            st.warning(st.session_state.image_url if st.session_state.image_url else "No image asset generated.")

    # Section for pushing generated assets onto live social networks
    st.markdown("---")
    st.subheader("3. Direct Distribution Hub")
    
    include_image_toggle = st.checkbox("Include visual graphic in social blast", value=True)
    
    if st.button("🚀 Publish Live to Facebook Business Feed", use_container_width=True):
        if not fb_page_id or not fb_page_token:
            st.error("Missing Facebook Page credentials in the sidebar!")
        else:
            with st.spinner("Publishing directly to Facebook..."):
                img_to_send = st.session_state.image_url if include_image_toggle else None
                status = publish_to_facebook(st.session_state.luxury_text, img_to_send, fb_page_id, fb_page_token)
                
                if "Success" in status:
                    st.success(status)
                else:
                    st.error(status)
