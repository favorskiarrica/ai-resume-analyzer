import streamlit as st
import PyPDF2

from utils import (
    get_match_percentage,
    generate_ai_suggestions
)

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(page_title="ResumeAI", page_icon="📄", layout="centered")

# ---------------- HEADER ---------------- #

st.title("ResumeAI 🚀")
st.subheader("AI Resume → Job Matching & Feedback System")

st.write("Upload your resume and paste a job description to analyze your match.")

st.divider()

# ---------------- INPUTS ---------------- #

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

job_description = st.text_area(
    "💼 Paste Job Description",
    placeholder="Paste the job description here..."
)

# ---------------- MAIN LOGIC ---------------- #

if uploaded_file and job_description:

    resume_text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)

        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                resume_text += text

        st.success("✅ Resume uploaded successfully!")

    except Exception:
        st.error("❌ Could not read PDF file.")
        st.stop()

    if not resume_text.strip():
        st.warning("⚠️ No readable text found in PDF.")
        st.stop()

    # ---------------- ANALYSIS ---------------- #

    match_score, matched_keywords, missing_skills, job_type = get_match_percentage(
        resume_text,
        job_description
    )

    feedback = generate_ai_suggestions(
        match_score,
        matched_keywords,
        missing_skills,
        job_type
    )

    # ---------------- RESULTS ---------------- #

    st.divider()

    st.subheader("🧠 Detected Job Type")
    st.info(job_type)

    st.subheader("🎯 Match Score")
    st.metric("Match %", f"{match_score}%")
    st.progress(match_score / 100)

    # ---------------- MATCHED SKILLS ---------------- #

    st.subheader("✅ Matching Skills")
    if matched_keywords:
        st.write(", ".join(list(matched_keywords)[:15]))
    else:
        st.write("No strong matches found")

    # ---------------- MISSING SKILLS ---------------- #

    st.subheader("⚠️ Missing Key Skills")
    if missing_skills:
        st.write(", ".join(list(missing_skills)[:15]))
    else:
        st.write("No major missing skills 🎉")

    # ---------------- AI FEEDBACK ---------------- #

    st.subheader("🧠 AI Resume Coach Feedback")
    st.markdown(feedback)

    # ---------------- DOWNLOAD REPORT ---------------- #

    report = f"""
=============================
Resume AI Analysis Report
=============================

Job Type: {job_type}

Match Score: {match_score}%

-----------------------------
Matching Skills:
{list(matched_keywords)}

-----------------------------
Missing Skills:
{list(missing_skills)}

-----------------------------
AI Feedback:
{feedback}
"""

    st.download_button(
        label="📥 Download Full Report",
        data=report,
        file_name="resume_ai_report.txt"
    )

# ---------------- DEFAULT STATE ---------------- #

else:
    st.info("📄 Upload your resume and paste a job description to begin analysis.")