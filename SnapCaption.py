import streamlit as st
from configer import *

st.title("Image to Caption Generator for Social Media")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Automatically send image to your email
    st.info("Sending image to your email...")
    main.send_email(image, sender_email, sender_password)

    # Generate and display caption
    caption = main.generate_caption(image)
    st.write("Generated Caption:")
    st.write(caption)

    st.write("Suggested Status for Facebook, Instagram, and WhatsApp:")
    st.write(f"📸 {caption} #ImageCaption #SocialMedia")
  
