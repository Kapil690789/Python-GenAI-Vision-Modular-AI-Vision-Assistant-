import streamlit as st
import os
from PIL import Image

# Import our modular brains
from gemini_utility import GeminiProcessor       # For Vision & Text
from huggingface_utility import HuggingFaceGenerator # For Image Generation
from utils import save_uploaded_file, cleanup_temp_files # For File Handling

# Page Config
st.set_page_config(page_title="AI Studio Pro", layout="wide", page_icon="🤖")

st.title("🤖 AI Studio Pro")
st.caption("Powered by Google Gemini 2.0 & Hugging Face FLUX")

# --- SIDEBAR: PROVIDER SELECTION ---
with st.sidebar:
    st.header("Settings")
    
    # Toggle between Brains
    provider = st.radio(
        "Select AI Provider:", 
        ["Google Gemini (Vision/Text)", "Hugging Face (Image Gen)"]
    )
    
    st.divider()
    
    # Show info based on selection
    if provider == "Google Gemini (Vision/Text)":
        st.info("Status: Ready (Gemini 2.0 Flash)")
    else:
        st.info("Status: Ready (FLUX.1-dev)")

# ==========================================
# LOGIC 1: GOOGLE GEMINI (Vision & Text)
# ==========================================
if provider == "Google Gemini (Vision/Text)":
    
    # Initialize Gemini
    try:
        processor = GeminiProcessor()
    except Exception as e:
        st.error(f"Error connecting to Gemini: {e}")
        st.stop()

    # Task Selection
    task = st.selectbox("Choose Task:", ["Describe Image", "Extract Product Data (JSON)", "Chat with AI"])

    # --- Sub-Task: Image Description ---
    if task == "Describe Image":
        st.subheader("👁️ Image Analysis")
        uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            st.image(uploaded_file, width=400)
            user_prompt = st.text_input("Prompt:", value="Describe this image in detail.")
            
            if st.button("Analyze"):
                file_path = save_uploaded_file(uploaded_file)
                if file_path:
                    with st.spinner("Analyzing scene..."):
                        result = processor.img_to_text(file_path, user_prompt)
                        st.markdown(result)
                    cleanup_temp_files()

    # --- Sub-Task: JSON Data ---
    elif task == "Extract Product Data (JSON)":
        st.subheader("📊 Structured Data Extraction")
        uploaded_file = st.file_uploader("Upload Product Image", type=["jpg", "png", "jpeg"])
        
        if uploaded_file:
            st.image(uploaded_file, width=300)
            if st.button("Extract Data"):
                file_path = save_uploaded_file(uploaded_file)
                if file_path:
                    with st.spinner("Extracting parameters..."):
                        result = processor.img_to_json(file_path)
                        if result:
                            st.json(result)
                        else:
                            st.error("Extraction Failed.")
                    cleanup_temp_files()

    # --- Sub-Task: Chat ---
    elif task == "Chat with AI":
        st.subheader("💬 AI Assistant")
        user_question = st.text_area("Ask me anything:")
        if st.button("Send"):
            with st.spinner("Thinking..."):
                result = processor.text_to_text(user_question)
                st.markdown(result)

# ==========================================
# LOGIC 2: HUGGING FACE (Image Generation)
# ==========================================
elif provider == "Hugging Face (Image Gen)":
    
    st.subheader("🎨 Pro Image Generator")
    st.markdown("Create stunning images using **FLUX.1-dev** or **SDXL** models.")
    
    # Initialize Hugging Face
    try:
        hf_generator = HuggingFaceGenerator()
    except Exception as e:
        st.error(f"Error connecting to Hugging Face: {e}")
        st.stop()

    # Input
    img_prompt = st.text_area(
        "Enter your imagination:", 
        height=100, 
        value="A cyberpunk city street at night, neon lights, rain reflections, 8k resolution, cinematic"
    )
    
    if st.button("Generate Art 🎨"):
        with st.spinner("Generating High-Quality Image (This may take 10-20s)..."):
            
            # Call the new function
            image_path = hf_generator.generate_image(img_prompt)
            
            if image_path:
                # Display Result
                # st.image(image_path, caption=f"Generated: {img_prompt}", use_container_width=True)
                st.image(image_path, caption=f"Generated: {img_prompt}", use_column_width="always")
                
                # Download Button
                with open(image_path, "rb") as file:
                    st.download_button(
                        label="Download Image 📥",
                        data=file,
                        file_name="generated_art.png",
                        mime="image/png"
                    )
                st.success("Image generated successfully!")
            else:
                st.error("Generation failed. Check your API Token permissions or try a simpler prompt.")