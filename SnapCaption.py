import streamlit as st
from PIL import Image
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration

# Load the pre-trained model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

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
