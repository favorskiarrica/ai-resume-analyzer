# app.py
# app.py

import streamlit as st
import PyPDF2

from utils import (
    detect_job_type,
    get_similarity,
    get_keyword_match,
    get_missing_skills,
    get_ai_feedback
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(page_title="ResumeAI", page_icon="📄")

# ---------------- UI ---------------- #

st.title("ResumeAI 🚀")
st.subheader("AI-Powered Resume Analyzer & Job Matcher")

st.write("Upload your resume and paste a job description to get ATS scoring, skill analysis, and AI feedback.")

# ---------------- INPUTS ---------------- #

uploaded_file = st.file_uploader("📄 Upload your resume (PDF only)", type=["pdf"])

job_description = st.text_area(
    "💼 Paste Job Description",
    placeholder="Paste the job description here..."
)

# ---------------- PROCESS ---------------- #

if uploaded_file is not None:

    resume_text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        st.success("✅ Resume uploaded successfully!")

    except Exception:
        st.error("❌ Error reading PDF file.")
        st.stop()
job_type = detect_job_type(job_description)

st.write(f"🧠 Detected Job Type: {job_type}")
    # ---------------- VALIDATION ---------------- #

if not job_description:
    st.warning("⚠️ Please paste a job description.")
    st.stop()

if not resume_text:
    st.warning("⚠️ Could not extract text from PDF.")
    st.stop()

    # ---------------- ANALYSIS ---------------- #

score = get_similarity(resume_text, job_description, job_type)
matched_keywords = get_keyword_match(resume_text, job_description, job_type)
missing_skills = get_missing_skills(resume_text, job_description, job_type)
feedback = get_ai_feedback(score)

    # ---------------- DISPLAY ---------------- #
st.subheader("📊 Resume Analysis")

st.metric("ATS Score", f"{score}/100")

st.progress(score / 100)

# Matched skills
st.subheader("✅ Matched Skills")
st.write(", ".join(matched_keywords[:20]))

# Missing skills
st.subheader("⚠️ Missing Skills")
st.write(", ".join(missing_skills[:20]))

# Feedback
st.subheader("💡 AI Feedback")
st.write(feedback)
   

    # ---------------- DOWNLOAD REPORT ---------------- #

report = f"""
Resume Analysis Report

ATS Score: {score}/100

Matched Skills:
{matched_keywords}

Missing Skills:
{missing_skills}

Feedback:
{feedback}
"""

    st.download_button(
        label="📥 Download Report",
        data=report,
        file_name="resume_analysis.txt"
    )

# ---------------- DEFAULT STATE ---------------- #

else:
    st.info("📄 Upload your resume and add a job description to begin analysis.")
