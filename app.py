import streamlit as st
from PIL import Image
import cv2
import numpy as np
from io import BytesIO

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Adobe Scan Style Document Scanner",
    page_icon="📄",
    layout="centered"
)

# ---------------- TITLE ----------------
st.title("📄 Document Scanner")
st.write(
    "Upload a document image, convert it into a clean black & white scan, "
    "and download it as a PDF."
)

# ---------------- FILE UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload Document Image",
    type=["jpg", "jpeg", "png"]
)

# ---------------- IMAGE PROCESSING FUNCTION ----------------
def scan_document(pil_image):
    """
    Convert uploaded image into Adobe Scan-like black & white document.
    """

    # Convert PIL image to NumPy array
    image = np.array(pil_image)

    # Convert RGB to BGR (OpenCV format)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Remove noise
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

    # Open image
    image = Image.open(uploaded_file).convert("RGB")

    # Show original image
    st.subheader("🖼 Original Image")
    st.image(image, use_container_width=True)

    # Button
    if st.button("✨ Convert to Scanned PDF"):

        # Process image
        scanned_image = scan_document(image)

        # Show processed image
        st.subheader("📑 Scanned Black & White Image")
        st.image(scanned_image, use_container_width=True, clamp=True)

        # Convert NumPy array back to PIL
        scanned_pil = Image.fromarray(scanned_image)

        # Convert to RGB for PDF
        pdf_image = scanned_pil.convert("RGB")

        # Save PDF to memory
        pdf_buffer = BytesIO()
        pdf_image.save(pdf_buffer, format="PDF")
        pdf_buffer.seek(0)

        st.success("✅ PDF Created Successfully!")

        # Download button
        st.download_button(
            label="⬇ Download PDF",
            data=pdf_buffer,
            file_name="scanned_document.pdf",
            mime="application/pdf"
        )
