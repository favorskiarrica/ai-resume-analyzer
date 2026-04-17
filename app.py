import streamlit as st
import PyPDF2

from utils import get_match_percentage, get_ai_feedback

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(page_title="ResumeAI", page_icon="📄")

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

if uploaded_file is not None and job_description:

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

    if not resume_text:
        st.warning("⚠️ Could not extract text from PDF.")
        st.stop()

    # ---------------- ANALYSIS ---------------- #

    match_score, matched_keywords, missing_skills, job_type = get_match_percentage(
        resume_text, job_description
    )

    feedback = get_ai_feedback(match_score)

    # ---------------- DISPLAY ---------------- #

    st.divider()

    st.subheader("🧠 Detected Career Field")
    st.info(job_type)

    st.subheader("🎯 Job Match Score")
    st.metric("Match %", f"{match_score}%")
    st.progress(match_score / 100)

    st.subheader("✅ Matching Skills")
    st.write(", ".join(matched_keywords[:15]) if matched_keywords else "No strong matches found")

    st.subheader("⚠️ Missing Key Skills")
    st.write(", ".join(missing_skills[:15]) if missing_skills else "You're covering all key areas 🎉")

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

else:
    st.info("📄 Upload your resume and add a job description to begin.")