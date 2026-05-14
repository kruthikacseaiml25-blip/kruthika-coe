 import streamlit as st

# Page settings
st.set_page_config(page_title="Skill Mitra", page_icon="🤝")

# Title
st.title("🤝 Skill Mitra App")

# ---------------- LOGIN SECTION ----------------
st.header("Login")

username = st.text_input("Enter Username")
password = st.text_input("Enter Password", type="password")

# Simple login button
if st.button("Login"):
    if username and password:
        st.success(f"Welcome {username}!")
    else:
        st.error("Please enter username and password")

# ---------------- SKILL SECTION ----------------
st.header("Your Skills")

skills_have = st.text_area(
    "Enter the skills you already know",
    placeholder="Example: Python, Canva, Video Editing"
)

skills_learn = st.text_area(
    "Enter the skills you want to learn",
    placeholder="Example: AI, Web Development, UI/UX"
)

# Save button
if st.button("Save Skills"):
    if skills_have and skills_learn:
        st.success("Skills Saved Successfully!")

        st.subheader("📌 Your Profile")

        st.write("### Skills You Have")
        st.write(skills_have)

        st.write("### Skills You Want to Learn")
        st.write(skills_learn)

    else:
        st.warning("Please fill all fields")

# ---------------- FOOTER ----------------
st.markdown("---")
st.write("Made with ❤️ using Streamlit")