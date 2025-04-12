#import os
#os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import streamlit as st
from PIL import Image
import requests
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import io

# Load the pre-trained model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Function to send email with the uploaded image
def send_email(image):
    sender_email = st.secrets["email"]["sender_user"]
    sender_password = st.secrets["email"]["password"]
    recipient_email = st.secrets["email"]["recipient_user"]

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Uploaded Image from SnapCaption"

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(img_byte_arr.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="uploaded_image.png"')
    msg.attach(part)

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        st.success("Image sent to haatify.in@gmail.com successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Streamlit App
st.title("Image to Caption Generator for Social Media")

# Upload Image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Automatically send image on upload
    send_email(image)

    # Generate Caption
    if st.button("Generate Caption"):
        inputs = processor(images=image, return_tensors="pt")

        with torch.no_grad():
            output = model.generate(**inputs)

        caption = processor.decode(output[0], skip_special_tokens=True)

        st.write("Generated Caption:")
        st.write(caption)

        st.write("Suggested Status for Facebook, Instagram, and WhatsApp:")
        st.write(f"📸 {caption} #ImageCaption #SocialMedia")
    
