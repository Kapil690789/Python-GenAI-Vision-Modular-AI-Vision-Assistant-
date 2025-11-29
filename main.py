import os
import streamlit as st
from PIL import Image
from gemini_utility import GeminiProcessor

st.set_page_config(
    page_title="AI Vision Analyst",
    page_icon="👁️",
    layout="centered"
)

st.title("👁️ AI Vision Analyst")
st.caption("Powered by Google Gemini 2.0 Flash & Python")

# 3. Sidebar for Inputs
with st.sidebar:
    st.header("Configuration")
    prompt_input = st.text_area(
        "Enter your prompt:", 
        # value="Describe this image in technical detail, focusing on lighting and composition."
        value = "Identify the fashion items in this image. List the material, color, and fit of each clothing article."
    )
    submit_button = st.button("Analyze Image")

# file uploader
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    if submit_button:
        with st.spinner("AI is analyzing the scene..."):

            # Create a temporary file to work with your existing logic
            # (Because your Class expects a file path, not a raw stream)
            temp_path = "temp_image_upload.png"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            processor = GeminiProcessor()

            result = processor.analyze_image(temp_path, prompt=prompt_input)

            # Clean up (Delete the temp file)
            if os.path.exists(temp_path):
                os.remove(temp_path)


        if result: 
            st.subheader(" Analysis Result")
            st.markdown(result)
            st.success("Analysis Complete!")
        else:
            st.error("Failed to generate analysis. Check the logs.")