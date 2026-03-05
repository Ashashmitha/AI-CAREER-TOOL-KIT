import streamlit as st
import resume
import portfolio
import cover_letter

option = st.sidebar.selectbox(
    "Choose Tool",
    ["Resume Builder", "Portfolio Generator", "Cover Letter Generator"]
)

if option == "Resume Builder":
    resume.main()

elif option == "Portfolio Generator":
    portfolio.main()

elif option == "Cover Letter Generator":
    cover_letter.main()
