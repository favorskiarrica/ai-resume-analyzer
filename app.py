# app.py

import streamlit as st
import PyPDF2

from utils import get_match_percentage, get_ai_feedback, detect_job_type

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(page_title="ResumeAI", page_icon="📄")

# ---------------- UI ---------------- #

st.title("ResumeAI 🚀")
st.subheader("Smart Resume → Job Matching")

st.write("Upload your resume and paste a job description to see how well you match.")

# ---------------- INPUTS ---------------- #

uploaded_file = st.file_uploader("📄 Upload Resume (PDF)", type=["pdf"])

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
        st.error("❌ Error reading PDF.")
        st.stop()

    # ---------------- VALIDATION ---------------- #

    if not job_description:
        st.warning("⚠️ Please paste a job description.")
        st.stop()

    if not resume_text:
        st.warning("⚠️ Could not extract text from PDF.")
        st.stop()

    # ---------------- CAREER DETECTION ---------------- #

    job_type = detect_job_type(job_description)

    st.subheader("🧠 Detected Career Field")
    st.info(job_type)

    # ---------------- ANALYSIS ---------------- #

match_score, matched_keywords, missing_skills, job_type = get_match_percentage(
    resume_text, job_text
)
st.write("Detected Job Type:", job_type)

feedback = get_ai_feedback(match_score)

    # ---------------- DISPLAY ---------------- #

    st.divider()

    st.subheader("🎯 Job Match Score")
    st.metric("Match %", f"{match_score}%")
    st.progress(match_score / 100)

    # Matched
    st.subheader("✅ Matching Skills")
    if matched_keywords:
        st.write(", ".join(matched_keywords[:15]))
    else:
        st.write("No strong matches found")

    # Missing
    st.subheader("⚠️ Missing Key Skills")
    if missing_skills:
        st.write(", ".join(missing_skills[:15]))
    else:
        st.write("You're covering all key areas 🎉")

    # Feedback
    st.subheader("💡 AI Feedback")
    st.write(feedback)

    # ---------------- DOWNLOAD ---------------- #

    report = f"""
Resume Job Match Report

Match Score: {match_score}%

Detected Career Field:
{job_type}

Matching Skills:
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

# ---------------- DEFAULT ---------------- #

else:
    st.info("📄 Upload your resume and add a job description to begin.")