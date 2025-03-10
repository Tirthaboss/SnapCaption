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
import os

my_secret = os.getenv('Gmail_pass')

# Load the pre-trained model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Function to send email with the uploaded image
def send_email(image, recipient_email):
    # Set up the email server
    sender_email = "soupornochakraborty40@gmail.com"  # Replace with your email
    sender_password = my_secret  # Replace with your password

    # Create a multipart email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Uploaded Image from SnapCaption"

    # Save the image to a BytesIO object
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    # Attach the image to the email
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(img_byte_arr.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename="uploaded_image.png"')
    msg.attach(part)

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Streamlit App
st.title("Image to Caption Generator for Social Media")

# Upload Image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Open the image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Generate Caption
    if st.button("Generate Caption"):
        # Preprocess the image
        inputs = processor(images=image, return_tensors="pt")

        # Generate caption
        with torch.no_grad():
            output = model.generate(**inputs)

        # Decode the generated caption
        caption = processor.decode(output[0], skip_special_tokens=True)

        # Display the caption
        st.write("Generated Caption:")
        st.write(caption)

        # Social Media Status Suggestions
        st.write("Suggested Status for Facebook, Instagram, and WhatsApp:")
        st.write(f"📸 {caption} #ImageCaption #SocialMedia")

        # Email the image
        recipient_email = st.text_input("Enter recipient email address:")
        if st.button("Send Image via Email"):
            if recipient_email:
                send_email(image, recipient_email)
            else:
                st.error("Please enter a valid email address.")
