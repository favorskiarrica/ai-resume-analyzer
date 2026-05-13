import streamlit as st
import PyPDF2

from utils import (
    get_match_percentage,
    generate_ai_suggestions,
    chat_response,
    detect_job_type
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="ResumeAI",
    page_icon="📄",
    layout="wide"
)

# =========================================================
# DARK MODE STYLING
# =========================================================

st.markdown("""
<style>

/* Main app background */
.stApp {
    background-color: #0E1117;
    color: white;
}

/* Global text */
html, body, [class*="css"] {
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161B22;
}

/* Text inputs */
.stTextInput input,
.stTextArea textarea {
    background-color: #262730;
    color: white;
    border-radius: 10px;
    border: 1px solid #444;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background-color: #262730;
    border-radius: 10px;
    padding: 10px;
}

/* Buttons */
.stButton > button {
    background-color: #4F8BF9;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
}

/* Metric card */
[data-testid="metric-container"] {
    background-color: #1E1E1E;
    border-radius: 10px;
    padding: 15px;
}

/* Success message */
.stSuccess {
    background-color: #1E4620;
}

/* Warning message */
.stWarning {
    background-color: #4B3B00;
}

/* Info box */
.stInfo {
    background-color: #102A43;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #4F8BF9;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.title("🚀 ResumeAI")
st.subheader("Smart Resume → Job Matching System")

st.write(
    "Upload your resume and paste a job description to analyze "
    "your ATS match score, missing skills, strengths, and AI feedback."
)

st.divider()

# =========================================================
# INPUTS
# =========================================================

uploaded_file = st.file_uploader(
    "📄 Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "💼 Paste Job Description",
    placeholder="Paste the job description here..."
)

# =========================================================
# PROCESSING
# =========================================================

if uploaded_file is not None and job_description:

    resume_text = ""

    # ---------------- PDF EXTRACTION ---------------- #

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

    # ---------------- EMPTY CHECK ---------------- #

    if not resume_text:

        st.warning("⚠️ Could not extract text from the PDF.")
        st.stop()

    # =========================================================
    # ANALYSIS
    # =========================================================

    (
        match_score,
        matched_keywords,
        missing_skills,
        job_type,
        seniority
    ) = get_match_percentage(
        resume_text,
        job_description
    )

    feedback = generate_ai_suggestions(
        match_score,
        matched_keywords,
        missing_skills,
        job_type
    )

    # =========================================================
    # RESULTS
    # =========================================================

    st.divider()

    # Career Field
    st.subheader("🧠 Detected Career Field")
    st.info(job_type)

    # Seniority
    st.subheader("📊 Seniority Level Detected")
    st.info(seniority)

    # Match Score
    st.subheader("🎯 Job Match Score")

    st.metric(
        "Match %",
        f"{match_score}%"
    )

    st.progress(match_score / 100)

    # =========================================================
    # MATCHING SKILLS
    # =========================================================

    st.subheader("✅ Matching Skills")

    if matched_keywords:

        st.write(", ".join(matched_keywords))

    else:

        st.write("No strong matching skills found.")

    # =========================================================
    # MISSING SKILLS
    # =========================================================

    st.subheader("⚠️ Missing Key Skills")

    if missing_skills:

        st.write(", ".join(missing_skills))

    else:

        st.write("🎉 You're covering all major skills!")

    # =========================================================
    # AI FEEDBACK
    # =========================================================

    st.subheader("💡 AI Resume Coach Feedback")

    st.write(feedback)

    # =========================================================
    # CHATBOT SECTION
    # =========================================================

    st.divider()

    st.subheader("💬 AI Resume Chat Coach")

    user_question = st.text_input(
        "Ask anything about your resume:"
    )

    if user_question:

        response = chat_response(
            user_question,
            match_score,
            matched_keywords,
            missing_skills,
            job_type
        )

        st.write(response)

    # =========================================================
    # DOWNLOAD REPORT
    # =========================================================

    st.divider()

    report = f"""
Resume Analysis Report

==================================================

Career Field: {job_type}

Seniority Level: {seniority}

Match Score: {match_score}%

==================================================

MATCHING SKILLS:
{', '.join(matched_keywords)}

==================================================

MISSING SKILLS:
{', '.join(missing_skills)}

==================================================

AI FEEDBACK:
{feedback}
"""

    st.download_button(
        label="📥 Download Resume Report",
        data=report,
        file_name="resume_analysis_report.txt",
        mime="text/plain"
    )

# =========================================================
# DEFAULT SCREEN
# =========================================================

else:

    st.info(
        "📄 Upload your resume and paste a job description "
        "to begin analysis."
    )