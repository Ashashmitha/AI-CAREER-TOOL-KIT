import streamlit as st
from google import genai
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io
from datetime import date

# ---------------- CONFIG ----------------
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="AI Cover Letter Generator", layout="centered")
st.title("✉️ AI Cover Letter Generator")

# ---------------- USER INPUT ----------------
name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Contact Number")
linkedin = st.text_input("LinkedIn URL (optional)")
github = st.text_input("GitHub URL (optional)")

company = st.text_input("Company Name")
role = st.text_input("Job Role / Internship Role")

option = st.selectbox("Are you applying for:", ["Internship", "Full-time Job"])

experience = ""
if option == "Full-time Job":
    experience = st.text_area("Brief Work Experience")

skills = st.text_area("Key Skills")
projects = st.text_area("Key Projects")

# ---------------- GENERATE ----------------
if st.button("Generate Cover Letter"):
    if name and company and role and skills:

        prompt = f"""
Write a professional one-page cover letter.

Tone: formal, professional, ATS-friendly.
No emojis.
No stars.
No markdown.

Structure:
Header with name, email, phone.
Date.
Hiring Team
Company Name

3–4 strong paragraphs.

End with:
Sincerely,
{name}

Details:
Name: {name}
Email: {email}
Phone: {phone}
LinkedIn: {linkedin}
GitHub: {github}
Company: {company}
Role: {role}
Applying for: {option}
Experience: {experience}
Skills: {skills}
Projects: {projects}
"""

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        cover_text = response.text
        st.subheader("Generated Cover Letter")
        st.text(cover_text)

        # ---------------- PDF CREATION ----------------
        def create_pdf(text):
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=50,
                leftMargin=50,
                topMargin=50,
                bottomMargin=50
            )

            styles = getSampleStyleSheet()
            normal = styles["Normal"]

            story = []
            for para in text.split("\n"):
                story.append(Paragraph(para, normal))
                story.append(Spacer(1, 10))

            doc.build(story)
            buffer.seek(0)
            return buffer

        pdf_file = create_pdf(cover_text)

        st.download_button(
            "📥 Download Cover Letter PDF",
            data=pdf_file,
            file_name="Cover_Letter.pdf",
            mime="application/pdf"
        )

    else:
        st.warning("Please fill all required fields.")
