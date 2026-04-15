# utils.py

import re

STOPWORDS = {
    "the", "and", "is", "in", "to", "of", "a", "for", "on",
    "with", "as", "by", "an", "at", "from"
}

# 🔹 Job-specific skill dictionaries
JOB_SKILLS = {
    "Chiropractor": [
        "spinal", "rehabilitation", "therapy", "patient", "chiropractic",
        "musculoskeletal", "treatment", "diagnosis", "adjustment"
    ],
    "Data Analyst": [
        "python", "sql", "excel", "data", "analysis",
        "visualization", "pandas", "statistics", "dashboard"
    ],
    "Software Engineer": [
        "python", "java", "api", "backend", "frontend",
        "git", "algorithms", "system design", "debugging"
    ]
}

# 🔹 Clean text
def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text.lower())
    words = text.split()
    return [w for w in words if w not in STOPWORDS]


# 🔹 Detect job type automatically
def detect_job_type(text):
    text_words = set(clean_text(text))
    scores = {}

    for job, skills in JOB_SKILLS.items():
        match_count = len(text_words & set(skills))
        scores[job] = match_count

    return max(scores, key=scores.get)


# 🔹 Get job keywords
def get_job_keywords(job_type):
    return JOB_SKILLS.get(job_type, [])


# 🔹 Scoring
def get_similarity(resume_text, job_text, job_type):
    resume_words = set(clean_text(resume_text))
    job_words = set(clean_text(job_text)) | set(get_job_keywords(job_type))

    if not job_words:
        return 0

    matched = resume_words & job_words
    score = (len(matched) / len(job_words)) * 100

    return int(score)


# 🔹 Matched skills
def get_keyword_match(resume_text, job_text, job_type):
    resume_words = set(clean_text(resume_text))
    job_words = set(clean_text(job_text)) | set(get_job_keywords(job_type))

    return list(resume_words & job_words)


# 🔹 Missing skills
def get_missing_skills(resume_text, job_text, job_type):
    resume_words = set(clean_text(resume_text))
    job_words = set(clean_text(job_text)) | set(get_job_keywords(job_type))

    return list(job_words - resume_words)


# 🔹 Feedback
def get_ai_feedback(score):
    if score > 75:
        return "🔥 Excellent match! You're highly aligned with this role."
    elif score > 50:
        return "👍 Good match, but adding more relevant skills will improve your chances."
    else:
        return "⚠️ Low match. Tailor your resume to include more job-specific keywords and achievements."