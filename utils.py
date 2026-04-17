# utils.py

import re

STOPWORDS = {
    "the", "and", "is", "in", "to", "of", "a", "for", "on",
    "with", "as", "by", "an", "at", "from", "this", "that",
    "be", "are", "or", "it", "your"
}

# ---------------- CLEAN TEXT ---------------- #

def clean_text(text):
    text = re.sub(r"[^\w\s]", "", text.lower())
    words = text.split()
    return [w for w in words if w not in STOPWORDS and len(w) > 2]


# ---------------- EXTRACT KEYWORDS ---------------- #

def extract_job_keywords(job_text):
    words = clean_text(job_text)

    freq = {}
    for word in words:
        freq[word] = freq.get(word, 0) + 1

    # sort by importance (frequency)
    sorted_words = sorted(freq, key=freq.get, reverse=True)

    return set(sorted_words[:30])  # top 30 important words


# ---------------- MATCHING ENGINE ---------------- #

def get_match_percentage(resume_text, job_text):
    resume_words = set(clean_text(resume_text))
    job_keywords = extract_job_keywords(job_text)

    matched = resume_words & job_keywords
    missing = job_keywords - resume_words

    if not job_keywords:
        return 0, [], []

    score = (len(matched) / len(job_keywords)) * 100

    return int(score), list(matched), list(missing)


# ---------------- FEEDBACK ---------------- #

def get_ai_feedback(score):
    if score >= 80:
        return "🔥 Excellent match! Your resume is highly aligned with this role."
    elif score >= 60:
        return "👍 Good match! Add a few more relevant keywords to improve further."
    elif score >= 40:
        return "⚠️ متوسط match. Improve alignment by adding job-specific skills."
    else:
        return "❌ Low match. Tailor your resume to better reflect this job description."

# ---------------- CAREER DETECTION ---------------- #

JOB_CATEGORIES = {
    "Chiropractor": [
        "chiropractic", "spinal", "rehabilitation", "therapy",
        "patient", "musculoskeletal", "treatment", "adjustment"
    ],
    "Data Analyst": [
        "data", "analysis", "sql", "excel", "dashboard",
        "visualization", "pandas", "statistics"
    ],
    "Software Engineer": [
        "python", "java", "api", "backend", "frontend",
        "git", "algorithms", "debugging"
    ],
    "Healthcare": [
        "patient", "clinical", "medical", "treatment",
        "healthcare", "diagnosis", "care"
    ]
}

def detect_job_type(job_text):
    words = set(clean_text(job_text))

    scores = {}

    for job, keywords in JOB_CATEGORIES.items():
        match_count = len(words & set(keywords))
        scores[job] = match_count

    # Return best match
    best_match = max(scores, key=scores.get)

    return best_match