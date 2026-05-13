# app.py
import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Image to PDF Scanner", page_icon="📄")

st.title("📄 Image to PDF Scanner")
st.write("Upload an image of your document, convert it to black & white, and download as PDF!")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # Open image
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)
    
    # Button to process image
    if st.button("Convert to Grayscale & PDF"):
        # Convert to grayscale
        gray_image = image.convert("L")
        st.image(gray_image, caption="Grayscale Image", use_column_width=True)

        # Convert grayscale image to PDF
        pdf_bytes = io.BytesIO()
        gray_image.save(pdf_bytes, format="PDF")
        pdf_bytes.seek(0)

        # Download button
        st.download_button(
            label="📥 Download PDF",
            data=pdf_bytes,
            file_name="document.pdf",
            mime="application/pdf"
        )
