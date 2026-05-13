import streamlit as st
from PIL import Image
import cv2
import numpy as np
from io import BytesIO

st.set_page_config(
    page_title="Document Scanner",
    page_icon="📄",
    layout="centered"
)

st.title("📄 Adobe Scan Style Scanner")

uploaded_file = st.file_uploader(
    "Upload Document",
    type=["jpg", "jpeg", "png"]
)

def scan_document(pil_image):

    image = np.array(pil_image)

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

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

    image = Image.open(uploaded_file).convert("RGB")

    st.image(image, caption="Original Image", width=500)

    if st.button("Convert to PDF"):

        scanned_image = scan_document(image)

        st.image(
            scanned_image,
            caption="Scanned Image",
            width=500
        )

        scanned_pil = Image.fromarray(
            scanned_image
        ).convert("RGB")

        pdf_buffer = BytesIO()

        scanned_pil.save(
            pdf_buffer,
            format="PDF"
        )

        pdf_buffer.seek(0)

        st.download_button(
            label="Download PDF",
            data=pdf_buffer,
            file_name="scanned_document.pdf",
            mime="application/pdf"
        )
