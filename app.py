# app.py
import streamlit as st
from PIL import Image
import cv2
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Document Scanner", layout="centered")

st.title("📄 Document Scanner")
st.write("Upload a document image, convert it to black & white, and download it as a PDF.")

uploaded_file = st.file_uploader(
    "Upload an image",
    type=["jpg", "jpeg", "png"]
)

def process_document(image):
    """
    Convert image to grayscale + adaptive threshold
    for Adobe Scan-like effect.
    """
    img_np = np.array(image)

    # Convert RGB to BGR for OpenCV
    img_cv = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)

    # Noise reduction
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive threshold for clean document look
    scanned = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return scanned

if uploaded_file is not None:
    # Open uploaded image
    image = Image.open(uploaded_file).convert("RGB")

    st.subheader("Original Image")
    st.image(image, use_container_width=True)

    if st.button("Convert to Scan PDF"):
        # Process image
        scanned_img = process_document(image)

        st.subheader("Scanned Black & White Image")
        st.image(scanned_img, clamp=True, use_container_width=True)

        # Convert numpy image to PIL
        pil_img = Image.fromarray(scanned_img)

        # Convert to RGB for PDF export
        pdf_img = pil_img.convert("RGB")

        # Save PDF in memory
        pdf_bytes = BytesIO()
        pdf_img.save(pdf_bytes, format="PDF")
        pdf_bytes.seek(0)

        st.success("PDF created successfully!")

        st.download_button(
            label="⬇ Download PDF",
            data=pdf_bytes,
            file_name="scanned_document.pdf",
            mime="application/pdf"
        )
