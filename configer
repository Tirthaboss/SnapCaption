from PIL import Image
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import io

# Load the pre-trained model and processor
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

# Function to send email with the uploaded image
def send_email(image, sender_email, sender_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = sender_email
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
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Function to generate caption for an image
def generate_caption(image):
    inputs = processor(images=image, return_tensors="pt")
    with torch.no_grad():
        output = model.generate(**inputs)
    caption = processor.decode(output[0], skip_special_tokens=True)
    return caption

# Example usage:
if __name__ == "__main__":
    # Replace with the actual image file path
    image_path = "example.jpg"
    image = Image.open(image_path)

    # Generate and print caption
    caption = generate_caption(image)
    print("Generated Caption:", caption)
    print("Suggested Status: 📸", caption, "#ImageCaption #SocialMedia")

    # Send the image via email
    sender_email = "youremail@gmail.com"
    sender_password = "yourpassword"
    send_email(image, sender_email, sender_password)
