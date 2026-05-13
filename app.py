import streamlit as st
from PIL import Image
import cv2
import numpy as np
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Document Scanner",
    page_icon="📄",
    layout="centered"
)

# ---------------- TITLE ----------------
st.title("📄 Adobe Scan Style Document Scanner")

st.write(
    "Upload a document image, convert it into a clean black & white scan, "
    "and download it as a PDF."
)

# ---------------- FILE UPLOADER ----------------
uploaded_file = st.file_uploader(
    "Upload Document Image",
    type=["jpg", "jpeg", "png"]
)

# ---------------- DOCUMENT SCAN FUNCTION ----------------
def scan_document(pil_image):

    # Convert PIL image to NumPy array
    image = np.array(pil_image)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive threshold for scanner effect
    scanned = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return scanned

# ---------------- MAIN APP ----------------
if uploaded_file is not None:

    # Open uploaded image
    image = Image.open(uploaded_file).convert("RGB")

    # Display original image
    st.subheader("🖼 Original Image")
    st.image(image, width=500)

    # Convert button
    if st.button("✨ Convert to Scanned PDF"):

        # Process image
        scanned_image = scan_document(image)

        # Show scanned image
        st.subheader("📑 Scanned Black & White Image")
        st.image(scanned_image, width=500)

        # Convert NumPy array to PIL Image
        scanned_pil = Image.fromarray(scanned_image).convert("RGB")

        # Save PDF in memory
        pdf_buffer = BytesIO()

        scanned_pil.save(
            pdf_buffer,
            format="PDF"
        )

        pdf_buffer.seek(0)

        st.success("✅ PDF Created Successfully!")

        # Download button
        st.download_button(
            label="⬇ Download PDF",
            data=pdf_buffer,
            file_name="scanned_document.pdf",
            mime="application/pdf"
        )# app.py
