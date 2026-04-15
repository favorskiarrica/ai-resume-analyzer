import streamlit as st
import base64
import PyPDF2

from utils import get_similarity, get_ai_feedback, get_keyword_match

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🐘",
    layout="wide"
)

# ---- LOAD CSS ----
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---- ELEPHANT IMAGE ----
def show_elephant():
    with open("elephant.png", "rb") as f:
        data = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <div style="
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
        ">
            <img src="data:image/png;base64,{data}" width="250"
            style="
                opacity: 0.7;
                filter: drop-shadow(0 0 10px #00f5ff)
                        drop-shadow(0 0 25px #9d00ff);
            ">
        </div>
        """,
        unsafe_allow_html=True
    )

show_elephant()

# ---- TITLE ----
st.markdown("""
<h1 style='text-align: center; 
color: #00f5ff;
text-shadow: 0 0 10px #00f5ff, 0 0 20px #9d00ff;'>
🐘 AI Resume Analyzer
</h1>
<p style='text-align: center; color: white;'>
Match your resume with job descriptions using AI
</p>
""", unsafe_allow_html=True)

# ---- PDF UPLOAD ----
uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])

def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# ---- INPUTS ----
if uploaded_file:
    resume = extract_text_from_pdf(uploaded_file)
    st.success("✅ Resume uploaded successfully!")
else:
    resume = st.text_area("📌 Paste your resume here", height=250)

job = st.text_area("📌 Paste job description here", height=250)

# ---- ANALYZE BUTTON ----
if st.button("Analyze 🚀"):

    if not resume or not job:
        st.warning("Please provide both resume and job description.")
    else:
        try:
            # ---- SCORES ----
            score = float(get_similarity(resume, job))
            keyword_score, missing, job_type = get_keyword_match(resume, job)

            st.write(f"🧠 Detected Job Type: {job_type}")
            # ---- DISPLAY ----
            st.subheader("📊 Analysis Results")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Similarity Score", f"{score:.2f}%")

            with col2:
                st.metric("Keyword Match", f"{keyword_score:.2f}%")

            # ---- PROGRESS BAR ----
            st.progress(score / 100)

            # ---- FEEDBACK LABEL ----
            if score > 80:
                st.success("🔥 Strong match! You're a great fit.")
            elif score > 60:
                st.info("👍 Decent match, but room for improvement.")
            else:
                st.warning("⚠️ Low match. Improve your resume.")

            # ---- MISSING KEYWORDS ----
            if missing:
                st.subheader("❌ Missing Keywords")
                st.write(", ".join(missing))

            # ---- AI FEEDBACK ----
            st.subheader("🤖 AI Feedback")

            feedback = get_ai_feedback(resume, job)
            st.write(feedback)

            # ---- DOWNLOAD REPORT ----
            report = f"""
Match Score: {score:.2f}%
Keyword Match: {keyword_score:.2f}%

Missing Keywords:
{", ".join(missing)}

Feedback:
{feedback}
"""
            st.download_button("📥 Download Report", report, file_name="resume_analysis.txt")

        except Exception as e:
            st.error("Something went wrong. Please try again.")
            st.stop()