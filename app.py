import streamlit as st
import sqlite3
import pandas as pd

# Database connection
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE IF NOT EXISTS users(
    username TEXT,
    password TEXT,
    skills_have TEXT,
    skills_need TEXT,
    points INTEGER
)
''')

conn.commit()

st.title("🤝 Skill Mitra")

menu = ["Register", "Login", "View Users"]
choice = st.sidebar.selectbox("Menu", menu)

# Register
if choice == "Register":
    st.subheader("Create New Account")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    skills_have = st.text_area("Skills You Have")
    skills_need = st.text_area("Skills You Want")

    if st.button("Register"):
        c.execute("INSERT INTO users VALUES (?,?,?,?,?)",
                  (username, password, skills_have, skills_need, 100))
        conn.commit()

        st.success("Account Created Successfully!")

# Login
elif choice == "Login":
    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, password))

        data = c.fetchone()

        if data:
            st.success(f"Welcome {username}")

            st.write("### Your Skills")
            st.write("Skills Have:", data[2])
            st.write("Skills Need:", data[3])
            st.write("Points:", data[4])

        else:
            st.error("Invalid Credentials")

# View Users
elif choice == "View Users":
    st.subheader("All Registered Users")

    df = pd.read_sql_query("SELECT username, skills_have, skills_need, points FROM users", conn)

    st.dataframe(df)
 