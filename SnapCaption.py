import streamlit as st
from configer import *

st.title("Image to Caption Generator for Social Media")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)


    # Generate and display caption
    caption = generate_caption(image)
    st.write("Generated Caption:")
    st.write(caption)

    st.write("Suggested Status for Facebook, Instagram, and WhatsApp:")
    st.write(f"📸 {caption} #ImageCaption #SocialMedia")
  
