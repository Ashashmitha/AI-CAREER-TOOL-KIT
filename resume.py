import streamlit as st
from google import genai
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from textwrap import wrap
import io
import re

# ---------------- CONFIG ----------------
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="AI Resume Builder", layout="centered")
st.title("📄 AI Resume Builder")
st.write("Enter your details to generate a professional resume")

# ----------- USER INPUT FORM -----------

name = st.text_input("Full Name")
email = st.text_input("Email")
phone = st.text_input("Contact Number")

linkedin = st.text_input("LinkedIn URL (optional)")
github = st.text_input("GitHub URL (optional)")

college = st.text_input("College Name")
degree = st.text_input("Degree & Specialization")
start_year = st.text_input("Start Year")
grad_year = st.text_input("Expected Graduation Year")
cgpa = st.text_input("CGPA")

skills = st.text_area("Technical Skills (comma separated)")
projects = st.text_area("Projects (Title + Description)")

soft_skills = st.text_input("Soft Skills (optional)")
languages = st.text_input("Languages Known (optional)")

# Career type
career_type = st.radio("What are you seeking?", ("Internship", "Full-time Job"))

experience = ""
if career_type == "Full-time Job":
    experience = st.text_area("Work Experience (Company, Role, Duration, Description)")

include_declaration = st.checkbox("Include Declaration", value=True)

# ---------- HELPER FUNCTIONS ----------

def clean_text(text):
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"\|", "", text)

    # Remove anything after declaration sentence
    if "DECLARATION" in text:
        parts = text.split("DECLARATION")
        text = parts[0] + "DECLARATION\n\nI hereby declare that the information provided above is true and accurate to the best of my knowledge."

    return text.strip()


def create_pdf(text):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    left_margin = 0.75 * inch
    x = left_margin
    y = height - 0.75 * inch

    normal_font = "Helvetica"
    bold_font = "Helvetica-Bold"

    normal_size = 10.5
    heading_size = 11.5

    headings = [
        "CAREER OBJECTIVE",
        "EDUCATION",
        "TECHNICAL SKILLS",
        "PROJECTS",
        "SOFT SKILLS",
        "LANGUAGES",
        "EXPERIENCE",
        "DECLARATION"
    ]

    c.setFont(normal_font, normal_size)

    for line in text.split("\n"):
        line = line.strip()

        if line.upper() in headings:
            c.setFont(bold_font, heading_size)
            c.drawString(x, y, line)
            y -= 16
            c.setFont(normal_font, normal_size)
        else:
            wrapped_lines = wrap(line, 95)
            if not wrapped_lines:
                y -= 9
            for wline in wrapped_lines:
                c.drawString(x, y, wline)
                y -= 12

    c.save()
    buffer.seek(0)
    return buffer

# ----------- GENERATE BUTTON -----------

if st.button("Generate Resume"):
    if name and email and college and skills and projects:

        if career_type == "Internship":
            career_objective = """
Highly motivated and enthusiastic engineering student seeking an internship opportunity to apply academic knowledge in Artificial Intelligence and Machine Learning, gain hands-on industry experience, and contribute meaningfully to real-world projects.
"""
        else:
            career_objective = f"""
Results-driven engineering graduate seeking a full-time position in the field of Artificial Intelligence and Machine Learning, with professional experience in:
{experience}
Looking to leverage technical expertise and problem-solving skills to contribute to organizational growth and innovation.
"""

        prompt = f"""
You are a professional resume writer.

Generate a ONE PAGE, ATS-friendly resume.
No markdown.
No tables.
No stars.
No emojis.

Use this structure exactly:

FULL NAME
Email | Phone
LinkedIn | GitHub

CAREER OBJECTIVE
{career_objective}

EDUCATION

TECHNICAL SKILLS
"""

        if career_type == "Full-time Job":
            prompt += "\nEXPERIENCE\n"

        prompt += """
PROJECTS

SOFT SKILLS

LANGUAGES
"""

        if include_declaration:
            prompt += "\nDECLARATION\n"

        prompt += f"""
Name: {name}
Email: {email}
Phone: {phone}
LinkedIn: {linkedin}
GitHub: {github}
College: {college}
Degree: {degree}
Start Year: {start_year}
Expected Graduation: {grad_year}
CGPA: {cgpa}
Technical Skills: {skills}
Projects: {projects}
Experience: {experience}
Soft Skills: {soft_skills}
Languages: {languages}
"""

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        final_text = clean_text(response.text)

        st.subheader("📄 Your AI Generated Resume")
        st.text(final_text)

        pdf_file = create_pdf(final_text)

        st.download_button(
            label="📥 Download Resume as PDF",
            data=pdf_file,
            file_name="AI_Resume.pdf",
            mime="application/pdf"
        )

    else:
        st.warning("Please fill all mandatory fields.")
