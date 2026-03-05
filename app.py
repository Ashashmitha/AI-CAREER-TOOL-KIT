import streamlit as st
import subprocess

st.title("AI Career Toolkit")

st.write("Choose a tool")

option = st.selectbox(
    "Select Tool",
    ("Resume Builder", "Portfolio Generator", "Cover Letter Generator")
)

if option == "Resume Builder":
    subprocess.run(["streamlit", "run", "resume.py"])

elif option == "Portfolio Generator":
    subprocess.run(["streamlit", "run", "portfolio.py"])

elif option == "Cover Letter Generator":
    subprocess.run(["streamlit", "run", "cover_letter.py"])