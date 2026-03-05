import streamlit as st
from google import genai
import base64
import os
import re

# ---------------- CONFIG ----------------
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

st.set_page_config(page_title="AI Portfolio Generator", layout="centered")

st.title("🌐 AI Portfolio Generator")
st.write("Generate your professional AI-powered portfolio website")

# ---------------- CLEAN FUNCTION ----------------
def clean_text(text):
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"#", "", text)
    text = re.sub(r">", "", text)
    text = re.sub(r"-{2,}", "", text)
    text = re.sub(r"\|", "", text)
    text = text.replace("â€™", "'")
    return text.strip()

# ---------------- AI FUNCTION ----------------
def generate_ai(prompt):
    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=prompt
    )
    return clean_text(response.text)

# ---------------- INPUTS ----------------

name = st.text_input("Full Name")
role = st.text_input("Your Role (e.g AIML Student)")

email = st.text_input("Email")
linkedin = st.text_input("LinkedIn URL")
github = st.text_input("GitHub URL")

profile_pic = st.file_uploader("Upload Profile Picture (optional)", type=["png", "jpg", "jpeg"])
resume = st.file_uploader("Upload Resume PDF (optional)", type=["pdf"])

st.header("Projects")
num_projects = st.number_input("Number of Projects", 1, 5, 1)

projects = []

for i in range(num_projects):
    st.subheader(f"Project {i+1}")
    title = st.text_input(f"Project Title {i+1}")
    tech = st.text_input(f"Tech Stack {i+1}")
    link = st.text_input(f"GitHub Link {i+1}")
    projects.append((title, tech, link))

skills = st.text_area("Technical Skills (comma separated)")
certificates = st.text_area("Certificates (one per line)")

theme = st.radio("Choose Theme", ["Light", "Dark"])

# ---------------- GENERATE ----------------

if st.button("Generate Portfolio"):

    if not name or not role:
        st.warning("Please fill Name and Role")
    else:

        # AI BIO
        bio_prompt = f"""
        Write a professional 2-paragraph portfolio bio.

        IMPORTANT:
        - No markdown
        - No bullet points
        - No special characters
        - Only plain professional text

        Name: {name}
        Role: {role}
        """
        bio = generate_ai(bio_prompt)

        # AI PROJECT DESCRIPTIONS
        project_input = ""
        for p in projects:
            project_input += f"{p[0]} using {p[1]}\n"

        projects_prompt = f"""
        Write professional project descriptions.

        IMPORTANT:
        - No markdown
        - No bullet points
        - No special symbols
        - Only plain paragraphs

        Projects:
        {project_input}
        """
        projects_ai = generate_ai(projects_prompt)

        # AI SKILLS
        skills_prompt = f"""
        Write a strong technical skills summary.

        IMPORTANT:
        - No markdown
        - No bullet points
        - Plain paragraph only

        Role: {role}
        Skills: {skills}
        """
        skills_ai = generate_ai(skills_prompt)

        # AI CERTIFICATES
        cert_prompt = f"""
        Summarize these certificates professionally.

        IMPORTANT:
        - No markdown
        - No bullet points
        - Plain paragraph only

        Certificates:
        {certificates}
        """
        cert_ai = generate_ai(cert_prompt)

        # PROFILE IMAGE
        img_html = ""
        if profile_pic:
            img_bytes = profile_pic.read()
            encoded = base64.b64encode(img_bytes).decode()
            img_html = f'<img src="data:image/png;base64,{encoded}" width="180" style="border-radius:50%;"/>'

        # SAVE RESUME
        resume_link = ""
        if resume:
            os.makedirs("generated", exist_ok=True)
            with open("generated/resume.pdf", "wb") as f:
                f.write(resume.read())
            resume_link = "resume.pdf"

        # HTML CONTENT
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <title>{name} Portfolio</title>
        <style>
        body {{
            font-family: Arial;
            background: {"#121212" if theme=="Dark" else "white"};
            color: {"white" if theme=="Dark" else "black"};
            padding:40px;
            text-align:center;
        }}
        a {{
            color:#4da6ff;
            text-decoration:none;
        }}
        h2 {{
            margin-top:40px;
        }}
        p {{
            max-width:800px;
            margin:auto;
            line-height:1.6;
        }}
        </style>
        </head>
        <body>

        {img_html}
        <h1>{name}</h1>
        <h3>{role}</h3>

        <h2>About Me</h2>
        <p>{bio}</p>

        <h2>Projects</h2>
        <p>{projects_ai}</p>

        <h2>Skills</h2>
        <p>{skills_ai}</p>

        <h2>Certificates</h2>
        <p>{cert_ai}</p>

        <h2>Resume</h2>
        <a href="{resume_link}">Download Resume</a>

        <h2>Contact</h2>
        <p>Email: {email}</p>
        <p><a href="{linkedin}">LinkedIn</a></p>
        <p><a href="{github}">GitHub</a></p>

        </body>
        </html>
        """

        os.makedirs("generated", exist_ok=True)
        with open("generated/portfolio.html", "w", encoding="utf-8") as f:
            f.write(html)

        st.success("Portfolio Generated Successfully!")
        st.download_button("Download Portfolio HTML", html, file_name="portfolio.html")