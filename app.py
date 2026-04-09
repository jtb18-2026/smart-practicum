import streamlit as st

# ── Page config MUST be first Streamlit call ──────────────────────────────
st.set_page_config(
    page_title="Smart Practicum",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
import numpy as np
import re
import os
import ast
from collections import Counter

# ── Custom CSS — Professional Navy + Emerald Theme ────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

/* ═══════════════════════════════════════════════
   PROFESSIONAL CAREER PALETTE
   Inspired by LinkedIn, Indeed, Handshake

   Page BG:    #f0f4f8   (cool light grey)
   Card BG:    #ffffff   (clean white)
   Sidebar:    #ffffff
   Border:     #dde3ea   (soft grey border)
   Navy:       #0a2540   (primary — deep professional navy)
   Blue:       #1a56db   (interactive — buttons, links)
   Emerald:    #047857   (success, strong match, growth)
   Sky:        #0284c7   (company names, secondary info)
   Text:       #111827   (near black — max readability)
   Muted:      #6b7280   (grey — captions, labels)
   Soft match: #2563eb   (partial match — clean blue)
   Red:        #b91c1c   (weak match)
   Border-L:   #3b82f6   (left accent on section headers)
═══════════════════════════════════════════════ */

/* ── Base ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap');

html, body, [class*="css"],
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"],
.main {
    background-color: #f0f4f8 !important;
    color: #111827 !important;
    font-family: 'Inter', sans-serif;
    font-size: 15px;
}
.block-container, [data-testid="block-container"] {
    background-color: #f0f4f8 !important;
    padding: 1.5rem 2.5rem;
    max-width: 1400px;
}
p, span, div, label, li, td, th { color: #111827; }
h1, h2, h3 { font-family: 'Plus Jakarta Sans', sans-serif; color: #0a2540; }

/* ── Sidebar ── */
section[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background-color: #ffffff !important;
    border-right: 1px solid #dde3ea !important;
}
[data-testid="stRadio"] label,
[data-testid="stRadio"] div { color: #111827 !important; }
[data-testid="stSlider"] label,
[data-testid="stSlider"] div { color: #111827 !important; }
[data-testid="stTextArea"] label { color: #111827 !important; }
[data-testid="stMultiSelect"] label { color: #111827 !important; }
[data-testid="stSelectbox"] label { color: #111827 !important; }
[data-testid="stCheckbox"] label { color: #111827 !important; }
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] div,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploadDropzone"] {
    color: #111827 !important;
    background-color: #ffffff !important;
    border-color: #dde3ea !important;
}
[data-testid="stCaptionContainer"] { color: #6b7280 !important; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #0a2540 0%, #1e3a5f 55%, #1a56db 100%);
    border-radius: 16px;
    padding: 1.8rem 2.8rem;
    margin-bottom: 1.8rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(10,37,64,0.18);
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -5%;
    width: 380px;
    height: 380px;
    background: radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 65%);
    pointer-events: none;
}
.hero-banner::after {
    content: '';
    position: absolute;
    bottom: -20%;
    left: 30%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(4,120,87,0.15) 0%, transparent 65%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2.3rem;
    font-weight: 800;
    color: #ffffff !important;
    margin: 0 0 0.3rem 0;
    line-height: 1.15;
    letter-spacing: -0.01em;
    text-shadow: 0 2px 16px rgba(0,0,0,0.7) !important;
}
/* Override global h1 color inside hero */
.hero-banner h1, .hero-banner .hero-title {
    color: #ffffff !important;
    text-shadow: 0 2px 16px rgba(0,0,0,0.7) !important;
}
.hero-sub {
    color: #93c5fd;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 0 0 0.4rem 0;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ── Metric Cards ── */
.metric-card {
    background: #ffffff;
    border: 1px solid #dde3ea;
    border-top: 3px solid #1a56db;
    border-radius: 12px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}
.metric-value {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2.3rem;
    font-weight: 800;
    color: #0a2540;
    margin: 0;
}
.metric-label {
    font-size: 0.78rem;
    color: #6b7280;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 0.35rem 0 0 0;
    font-weight: 600;
}

/* ── Match Cards ── */
.match-card {
    background: #ffffff;
    border: 1px solid #dde3ea;
    border-radius: 12px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.1rem;
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.15s;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
}
.match-card:hover {
    border-color: #1a56db;
    box-shadow: 0 6px 22px rgba(26,86,219,0.1);
    transform: translateY(-1px);
}
.match-rank {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.16em;
    color: #9ca3af;
    margin-bottom: 0.25rem;
}
.match-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: #0a2540;
    margin: 0 0 0.2rem 0;
    line-height: 1.3;
}
.match-company {
    color: #0284c7;
    font-size: 0.92rem;
    font-weight: 500;
    margin: 0 0 0.7rem 0;
}
.score-bar-bg {
    background: #e5e7eb;
    border-radius: 99px;
    height: 10px;
    width: 100%;
    margin: 0.4rem 0;
}
.score-bar-fill {
    height: 10px;
    border-radius: 99px;
    transition: width 0.6s ease;
}
.skill-tag {
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    border: 1px solid #bfdbfe;
    border-radius: 5px;
    padding: 0.18rem 0.65rem;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 0.15rem 0.15rem 0.15rem 0;
    font-family: 'Inter', sans-serif;
}
.section-header {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #0a2540;
    border-left: 4px solid #1a56db;
    padding-left: 0.85rem;
    margin: 1.5rem 0 1rem 0;
}
.info-box {
    background: #ffffff;
    border: 1px solid #dde3ea;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.stTextArea textarea {
    background: #ffffff !important;
    border: 1px solid #dde3ea !important;
    color: #111827 !important;
    font-family: 'Inter', sans-serif !important;
    border-radius: 10px !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #2563eb, #60a5fa) !important;
    color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2rem !important;
    font-size: 1rem !important;
    letter-spacing: 0.02em !important;
    width: 100% !important;
    transition: all 0.2s !important;
    text-shadow: 0 1px 3px rgba(0,0,0,0.35) !important;
}
.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: #ffffff !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(37,99,235,0.4) !important;
}
.sidebar-section {
    background: #f8fafc;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.75rem;
    border: 1px solid #dde3ea;
}
.job-link-btn {
    display: inline-block;
    background: #0a2540;
    color: #ffffff !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    font-size: 0.85rem;
    padding: 0.38rem 1rem;
    border-radius: 7px;
    text-decoration: none !important;
    margin-top: 0.6rem;
    transition: background 0.2s;
    letter-spacing: 0.01em;
}
.job-link-btn:hover { background: #1a56db; }
.badge {
    display: inline-block;
    padding: 0.18rem 0.6rem;
    border-radius: 5px;
    font-size: 0.76rem;
    font-weight: 600;
    margin: 0 0.2rem 0.2rem 0;
    font-family: 'Inter', sans-serif;
}
.badge-work  { background: #eff6ff; color: #1d4ed8; }
.badge-remote { background: #ecfdf5; color: #047857; }
.badge-salary { background: #f0fdf4; color: #15803d; }
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────
HARD_SKILLS_DB = sorted([
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c',
    'r', 'scala', 'kotlin', 'swift', 'go', 'rust', 'php', 'ruby',
    'matlab', 'bash', 'shell', 'perl', 'vba',
    'html', 'css', 'react', 'angular', 'vue', 'node.js', 'nodejs',
    'django', 'flask', 'fastapi', 'spring', 'express', 'jquery',
    'rest api', 'graphql', 'bootstrap',
    'sql', 'mysql', 'postgresql', 'sqlite', 'oracle', 'nosql',
    'mongodb', 'redis', 'cassandra', 'elasticsearch',
    'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'plotly',
    'tableau', 'power bi', 'excel', 'google sheets', 'looker',
    'machine learning', 'deep learning', 'neural networks',
    'nlp', 'natural language processing', 'computer vision',
    'scikit-learn', 'tensorflow', 'keras', 'pytorch',
    'hugging face', 'transformers', 'xgboost', 'lightgbm',
    'random forest', 'regression', 'classification', 'clustering',
    'reinforcement learning', 'llm', 'generative ai',
    'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes',
    'terraform', 'ci/cd', 'jenkins', 'git', 'github', 'gitlab',
    'linux', 'unix', 'devops', 'mlops',
    'spark', 'hadoop', 'kafka', 'airflow', 'dbt', 'snowflake',
    'databricks', 'bigquery', 'redshift', 'etl', 'data pipeline',
    'cybersecurity', 'penetration testing', 'network security',
    'firewalls', 'encryption', 'siem',
    'agile', 'scrum', 'jira', 'confluence', 'figma', 'photoshop',
    'autocad', 'solidworks', 'sas', 'spss', 'stata',
    'api', 'microservices', 'object-oriented',
], key=len, reverse=True)

EMBEDDINGS_URL = "https://github.com/jtb18-2026/smart-practicum/releases/download/v1.0/job_embeddings.npy"

# ── Helper functions ───────────────────────────────────────────────────────
def clean_text(text):
    if not isinstance(text, str) or text.strip() == '':
        return ''
    text = text.lower()
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'[^a-z0-9\s\+\#]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def extract_hard_skills(text):
    return list(set(skill for skill in HARD_SKILLS_DB if skill in text))

def detect_education_level(text):
    if any(w in text for w in ['phd', 'ph.d', 'doctorate', 'doctoral']): return 4
    elif any(w in text for w in ['master', 'mba', 'msc', 'm.s.', 'graduate degree']): return 3
    elif any(w in text for w in ['bachelor', 'b.s.', 'b.a.', 'undergraduate', 'university', 'college', 'degree']): return 2
    elif any(w in text for w in ['associate', 'community college', 'vocational']): return 1
    return 0

def detect_experience_level(text):
    year_match = re.search(r'(\d+)[+\-–]?\s*(?:to\s*\d+)?\s*years?\s+(?:of\s+)?(?:experience|exp)', text)
    if year_match:
        yrs = int(year_match.group(1))
        if yrs <= 2: return 'entry'
        elif yrs <= 5: return 'mid'
        else: return 'senior'
    if any(w in text for w in ['senior', 'lead', 'principal', 'director', 'manager']): return 'senior'
    if any(w in text for w in ['entry level', 'entry-level', 'junior', 'new grad', 'intern']): return 'entry'
    if 'experience' in text or 'mid level' in text: return 'mid'
    return 'unknown'

def score_color(score):
    if score >= 0.75: return "#047857"
    elif score >= 0.55: return "#2563eb"
    return "#b91c1c"

def score_label(score):
    if score >= 0.75: return "🟢 Strong Match"
    elif score >= 0.55: return "🟡 Partial Match"
    return "🔴 Weak Match"

def fmt_salary(row):
    sal = row.get('normalized_salary')
    period = str(row.get('pay_period', '')).upper()
    if pd.isna(sal) or sal == 0:
        return None
    sal = int(sal)
    if period == 'HOURLY':
        return f"${sal:,}/hr"
    elif period in ('YEARLY', ''):
        return f"${sal:,}/yr"
    elif period == 'MONTHLY':
        return f"${sal:,}/mo"
    return f"${sal:,}"

# ── Data loading ───────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Loading model (first time only)...")
def load_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource(show_spinner="Loading job data (first time only)...")
def load_all_data():
    import requests
    app_dir = os.path.dirname(os.path.abspath(__file__))

    jobs_df = pd.read_csv(os.path.join(app_dir, 'jobs_slim.csv'))
    jobs_df['required_skills'] = jobs_df['required_skills'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else []
    )

    results_csv = os.path.join(app_dir, 'smart_practicum_results.csv')
    results_df = None
    if os.path.exists(results_csv):
        results_df = pd.read_csv(results_csv)
        results_df['Skills_Matched'] = results_df['Skills_Matched'].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else []
        )

    emb_path = '/tmp/job_embeddings.npy'
    if not os.path.exists(emb_path) or os.path.getsize(emb_path) < 10_000_000:
        response = requests.get(EMBEDDINGS_URL, stream=True)
        response.raise_for_status()
        with open(emb_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=65536):
                if chunk:
                    f.write(chunk)

    job_embeddings = np.load(emb_path, allow_pickle=True)
    return jobs_df, job_embeddings, results_df

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:1rem 0 1.5rem 0;'>
        <div style='font-family:Plus Jakarta Sans,sans-serif; font-size:1.5rem;
                    font-weight:800; color:#0a2540;'>Smart Practicum</div>
        <div style='color:#1a56db; font-size:0.78rem; text-transform:uppercase;
                    letter-spacing:0.12em; margin-top:0.2rem; font-weight:600;'>
            AI Job Matching Engine</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", [
        "🔍 Match My Resume",
        "📊 Career Dashboard",
        "ℹ️ How It Works"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div class='sidebar-section'>
        <div style='color:#1a56db; font-size:0.72rem; text-transform:uppercase;
                    letter-spacing:0.1em; margin-bottom:0.5rem; font-weight:700;'>Data</div>
        <div style='color:#374151; font-size:0.85rem; line-height:1.8;'>
            ✅ 124k+ LinkedIn jobs<br>
            ✅ Auto-loaded on startup<br>
            <span style='color:#9ca3af; font-size:0.78rem;'>No setup needed</span>
        </div>
    </div>
    <div class='sidebar-section'>
        <div style='color:#1a56db; font-size:0.72rem; text-transform:uppercase;
                    letter-spacing:0.1em; margin-bottom:0.5rem; font-weight:700;'>Model</div>
        <div style='color:#374151; font-size:0.85rem; line-height:1.8;'>
            🤖 all-MiniLM-L6-v2<br>
            ⚖️ 40% Skills · 20% Edu<br>
            &nbsp;&nbsp;&nbsp;&nbsp;20% Exp · 20% Semantic
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Hero Banner ────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-banner'>
    <p class='hero-sub'>DATA-496 · Capstone Project</p>
    <h1 class='hero-title'>Smart Practicum</h1>
    <p style='color:#e0e7ff; margin:0.3rem 0 0 0; font-size:1rem; max-width:650px;'>
        Upload your resume and instantly see your top job matches across
        124,000+ real LinkedIn postings — powered by BERT embeddings.
    </p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 1: MATCH MY RESUME
# ══════════════════════════════════════════════════════════════════════════
if page == "🔍 Match My Resume":

    col_left, col_right = st.columns([1, 1.4], gap="large")

    with col_left:
        st.markdown("<div class='section-header'>Your Resume</div>", unsafe_allow_html=True)

        input_method = st.radio("How would you like to add your resume?",
                                ["📋 Paste Resume Text", "📄 Upload PDF"], horizontal=True)

        resume_text = ""
        if input_method == "📋 Paste Resume Text":
            resume_text = st.text_area(
                "Paste your resume text here", height=250,
                placeholder="Copy and paste the full text of your resume here...\n\nInclude: skills, work experience, education, projects"
            )
        else:
            uploaded = st.file_uploader("Upload your resume PDF", type=["pdf"])
            if uploaded:
                try:
                    import pdfplumber
                    with pdfplumber.open(uploaded) as pdf:
                        resume_text = "\n".join(p.extract_text() or "" for p in pdf.pages)
                    st.success(f"✅ PDF loaded — {len(resume_text):,} characters extracted")
                except ImportError:
                    st.error("pdfplumber not installed.")
                except Exception as e:
                    st.error(f"Could not read PDF: {e}")

        top_k = st.slider("Number of job matches to show", 3, 15, 5)

        # ── Filters ───────────────────────────────────────────────────────
        with st.expander("🔧 Filters", expanded=False):
            st.markdown("**Filter the job database before matching:**")

            loc_search = st.text_input("📍 Location (city or state)", placeholder="e.g. Los Angeles, CA or New York")

            work_types = st.multiselect(
                "💼 Job Type",
                ["Full-time", "Part-time", "Contract", "Internship", "Temporary"],
                default=[]
            )

            exp_levels = st.multiselect(
                "📈 Experience Level",
                ["Entry level", "Associate", "Mid-Senior level", "Director", "Executive", "Internship"],
                default=[]
            )

            edu_options = {
                "No requirement": 0, "Associate's": 1,
                "Bachelor's": 2, "Master's": 3, "PhD": 4
            }
            max_edu = st.selectbox("🎓 Max Education Required", ["Any"] + list(edu_options.keys()))

            remote_only = st.checkbox("🏠 Remote jobs only")

            min_score_pct = st.slider("⭐ Minimum match score", 0, 100, 0, step=5,
                                      help="Only show jobs above this match score")

            salary_filter = st.checkbox("💰 Only show jobs with salary info")

        run_btn = st.button("🔍 Find My Top Jobs", use_container_width=True)

        # ── Resume analysis preview ────────────────────────────────────────
        if resume_text.strip():
            clean = clean_text(resume_text)
            skills = extract_hard_skills(clean)
            edu = detect_education_level(clean)
            exp = detect_experience_level(clean)
            edu_labels = {0:"None detected",1:"Associate",2:"Bachelor's",3:"Master's",4:"PhD"}

            st.markdown("<div class='section-header'>Resume Analysis</div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class='info-box'>
                <div style='color:#64748b; font-size:0.75rem; text-transform:uppercase;
                            letter-spacing:0.08em; margin-bottom:0.6rem; font-weight:600;'>
                    Detected Profile</div>
                <div style='color:#0f172a; font-size:0.95rem; line-height:1.9;'>
                    🎓 <b>Education:</b> {edu_labels.get(edu, "Unknown")}<br>
                    💼 <b>Experience:</b> {exp.title()}<br>
                    🔧 <b>Skills found:</b> {len(skills)}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if skills:
                tags = "".join(f"<span class='skill-tag'>{s}</span>" for s in sorted(skills))
                st.markdown(tags, unsafe_allow_html=True)
            else:
                st.caption("No hard skills detected — try adding more technical keywords")

    with col_right:
        st.markdown("<div class='section-header'>Your Top Job Matches</div>", unsafe_allow_html=True)

        if run_btn and resume_text.strip():
            try:
                jobs_df, job_embeddings, _ = load_all_data()
                model = load_model()
            except Exception as e:
                st.error(f"Failed to load data: {e}\n\nPlease refresh the page and try again.")
                st.stop()

            with st.spinner("Computing your matches..."):
                clean  = clean_text(resume_text)
                skills = extract_hard_skills(clean)
                edu    = detect_education_level(clean)
                exp    = detect_experience_level(clean)

                resume_vec = model.encode(
                    [clean[:1000]], normalize_embeddings=True, show_progress_bar=False
                )[0].astype(np.float32)

                # ── Apply filters to job database ──────────────────────────
                mask = np.ones(len(jobs_df), dtype=bool)

                if loc_search.strip():
                    loc_lower = loc_search.strip().lower()
                    loc_mask = jobs_df['location'].fillna('').str.lower().str.contains(loc_lower)
                    mask &= loc_mask.values

                if work_types:
                    wt_mask = jobs_df['formatted_work_type'].fillna('').isin(work_types)
                    mask &= wt_mask.values

                if exp_levels:
                    el_mask = jobs_df['formatted_experience_level'].fillna('').isin(exp_levels)
                    mask &= el_mask.values

                if max_edu != "Any":
                    edu_val = edu_options[max_edu]
                    edu_mask = jobs_df['edu_required'].fillna(0) <= edu_val
                    mask &= edu_mask.values

                if remote_only:
                    rem_mask = jobs_df['remote_allowed'].fillna(0) == 1
                    mask &= rem_mask.values

                if salary_filter:
                    sal_mask = jobs_df['normalized_salary'].notna() & (jobs_df['normalized_salary'] > 0)
                    mask &= sal_mask.values

                filtered_df   = jobs_df[mask].reset_index(drop=True)
                filtered_embs = job_embeddings[mask]

                if len(filtered_df) == 0:
                    st.warning("No jobs match your filters. Try relaxing some filter options.")
                    st.stop()

                st.caption(f"Searching across {len(filtered_df):,} jobs matching your filters...")

                # ── Scoring ────────────────────────────────────────────────
                r_skills = set(skills)
                job_edu  = filtered_df['edu_required'].values.astype(np.float32)
                level_map = {'entry':1,'mid':2,'senior':3,'unknown':0}
                job_exp_num = np.array([level_map.get(str(e).lower().split('-')[0].strip(), 0)
                                        for e in filtered_df['exp_required'].tolist()], dtype=np.float32)

                cos_scores = (filtered_embs @ resume_vec).astype(np.float32)

                job_skill_sets = [set(s) if isinstance(s, list) else set()
                                  for s in filtered_df['required_skills']]
                skill_scores = np.array([
                    len(r_skills & js) / len(js) if js else 0.0
                    for js in job_skill_sets
                ], dtype=np.float32)

                edu_diff   = float(edu) - job_edu
                edu_scores = np.where(job_edu == 0, 0.7,
                             np.where(edu_diff >= 0, 1.0,
                             np.where(edu_diff >= -1, 0.5, 0.0))).astype(np.float32)

                r_exp_val  = level_map.get(exp, 0)
                exp_diff   = np.abs(r_exp_val - job_exp_num)
                exp_scores = np.where((r_exp_val == 0) | (job_exp_num == 0), 0.5,
                             np.where(exp_diff == 0, 1.0,
                             np.where(exp_diff == 1, 0.5, 0.0))).astype(np.float32)

                final_scores = (skill_scores * 0.40 + edu_scores * 0.20 +
                                exp_scores * 0.20 + cos_scores * 0.20)

                # Apply minimum score filter
                min_score = min_score_pct / 100.0
                score_mask = final_scores >= min_score
                if score_mask.sum() == 0:
                    st.warning(f"No jobs scored above {min_score_pct}%. Try lowering the minimum score.")
                    st.stop()

                k = min(top_k, int(score_mask.sum()))
                eligible_scores = np.where(score_mask, final_scores, -1)
                top_k_idx = np.argpartition(eligible_scores, -k)[-k:]
                top_k_idx = top_k_idx[np.argsort(eligible_scores[top_k_idx])[::-1]]

            # ── Render match cards ─────────────────────────────────────────
            for rank, j_idx in enumerate(top_k_idx, start=1):
                job_row = filtered_df.iloc[j_idx]
                score   = float(final_scores[j_idx])
                matched = sorted(r_skills & job_skill_sets[j_idx])
                color   = score_color(score)
                label   = score_label(score)
                pct     = int(score * 100)

                # Badges
                work_type  = job_row.get('formatted_work_type', '')
                is_remote  = job_row.get('remote_allowed', 0) == 1
                salary_str = fmt_salary(job_row)
                job_url    = job_row.get('job_posting_url', '')

                badges = ""
                if work_type and str(work_type) != 'nan':
                    badges += f"<span class='badge badge-work'>{work_type}</span>"
                if is_remote:
                    badges += "<span class='badge badge-remote'>🏠 Remote</span>"
                if salary_str:
                    badges += f"<span class='badge badge-salary'>💰 {salary_str}</span>"

                link_btn = ""
                if job_url and str(job_url) != 'nan':
                    link_btn = f"<a href='{job_url}' target='_blank' class='job-link-btn'>🔗 View Job on LinkedIn</a>"

                st.markdown(f"""
                <div class='match-card'>
                    <div class='match-rank'>Rank #{rank} · {label}</div>
                    <div class='match-title'>{job_row.get('title','Unknown')}</div>
                    <div class='match-company'>
                        {job_row.get('company_name', job_row.get('company','Unknown'))}
                        {f"· 📍 {job_row.get('location','')}" if job_row.get('location') else ''}
                    </div>
                    <div style='margin-bottom:0.6rem;'>{badges}</div>
                    <div style='display:flex; align-items:center; gap:0.8rem; margin:0.5rem 0;'>
                        <div class='score-bar-bg' style='flex:1;'>
                            <div class='score-bar-fill' style='width:{pct}%; background:{color};'></div>
                        </div>
                        <div style='font-family:Space Grotesk,sans-serif; font-weight:700;
                                    color:{color}; font-size:1.3rem; min-width:50px;'>{pct}%</div>
                    </div>
                    <div style='display:grid; grid-template-columns:1fr 1fr 1fr; gap:0.5rem; margin:0.8rem 0;'>
                        <div style='background:#f0f4f8; border:1px solid #dde3ea; border-radius:8px;
                                    padding:0.6rem; text-align:center;'>
                            <div style='color:#047857; font-size:1.1rem; font-weight:700;
                                        font-family:Plus Jakarta Sans,sans-serif;'>{int(skill_scores[j_idx]*100)}%</div>
                            <div style='color:#6b7280; font-size:0.72rem; text-transform:uppercase;
                                        font-weight:600; margin-top:0.1rem;'>Skills</div>
                        </div>
                        <div style='background:#f0f4f8; border:1px solid #dde3ea; border-radius:8px;
                                    padding:0.6rem; text-align:center;'>
                            <div style='color:#0284c7; font-size:1.1rem; font-weight:700;
                                        font-family:Plus Jakarta Sans,sans-serif;'>{int(edu_scores[j_idx]*100)}%</div>
                            <div style='color:#6b7280; font-size:0.72rem; text-transform:uppercase;
                                        font-weight:600; margin-top:0.1rem;'>Education</div>
                        </div>
                        <div style='background:#f0f4f8; border:1px solid #dde3ea; border-radius:8px;
                                    padding:0.6rem; text-align:center;'>
                            <div style='color:#1a56db; font-size:1.1rem; font-weight:700;
                                        font-family:Plus Jakarta Sans,sans-serif;'>{int(cos_scores[j_idx]*100)}%</div>
                            <div style='color:#6b7280; font-size:0.72rem; text-transform:uppercase;
                                        font-weight:600; margin-top:0.1rem;'>Semantic</div>
                        </div>
                    </div>
                    {"<div style='margin:0.4rem 0;'>" + "".join(f"<span class='skill-tag'>✓ {s}</span>" for s in matched) + "</div>" if matched else "<div style='color:#94a3b8; font-size:0.85rem;'>No skill overlap detected</div>"}
                    {link_btn}
                </div>
                """, unsafe_allow_html=True)

        elif not resume_text.strip():
            st.markdown("""
            <div style='text-align:center; padding:4rem 2rem;
                        border:2px dashed #cbd5e1; border-radius:16px; background:#ffffff;'>
                <div style='font-size:3rem; margin-bottom:1rem;'>📄</div>
                <div style='font-family:Space Grotesk,sans-serif; font-size:1.2rem;
                            font-weight:600; color:#475569; line-height:1.7;'>
                    Paste your resume or upload a PDF<br>to see your job matches
                </div>
                <div style='color:#94a3b8; font-size:0.9rem; margin-top:0.6rem;'>
                    Results appear here instantly after clicking Find My Top Jobs
                </div>
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 2: CAREER DASHBOARD
# ══════════════════════════════════════════════════════════════════════════
elif page == "📊 Career Dashboard":
    import plotly.express as px
    import plotly.graph_objects as go

    st.markdown("<div class='section-header'>Career Services Dashboard</div>", unsafe_allow_html=True)

    try:
        _, _, matches_df = load_all_data()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        st.stop()

    if matches_df is None:
        st.warning("Results file not available.")
        st.stop()

    top1 = matches_df[matches_df['Resume_Rank'] == 1]

    CHART_BG   = '#ffffff'
    PLOT_BG    = '#f8fafc'
    FONT_COLOR = '#0a2540'
    GRID_COLOR = '#e5e7eb'

    c1, c2, c3, c4 = st.columns(4)
    for col, val, lbl in [
        (c1, f"{matches_df['Resume_Index'].nunique():,}", "Resumes Processed"),
        (c2, f"{matches_df['Job_Index'].nunique():,}", "Jobs Matched"),
        (c3, f"{top1['Final_Score'].mean()*100:.1f}%", "Avg Best Score"),
        (c4, f"{(top1['Final_Score'] >= 0.65).sum():,}", "Strong Matches"),
    ]:
        with col:
            st.markdown(f"""<div class='metric-card'>
                <p class='metric-value'>{val}</p>
                <p class='metric-label'>{lbl}</p></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(top1, x='Final_Score', nbins=30,
                           color_discrete_sequence=['#1a56db'],
                           title='Best Match Score Distribution')
        fig.add_vline(x=top1['Final_Score'].mean(), line_dash='dash',
                      line_color='#047857',
                      annotation_text=f"Mean: {top1['Final_Score'].mean():.2f}",
                      annotation_font_color='#047857', annotation_font_size=13)
        fig.update_layout(paper_bgcolor=CHART_BG, plot_bgcolor=PLOT_BG,
                          font_color=FONT_COLOR, font_size=13, height=320,
                          xaxis=dict(gridcolor=GRID_COLOR, color=FONT_COLOR),
                          yaxis=dict(gridcolor=GRID_COLOR, color=FONT_COLOR),
                          title_font_size=16, title_font_color=FONT_COLOR)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        quality = {
            'Strong (≥75%)': (top1['Final_Score'] >= 0.75).sum(),
            'Good (55-75%)': ((top1['Final_Score'] >= 0.55) & (top1['Final_Score'] < 0.75)).sum(),
            'Weak (<55%)':   (top1['Final_Score'] < 0.55).sum()
        }
        fig = px.pie(values=list(quality.values()), names=list(quality.keys()),
                     color_discrete_sequence=['#047857','#1a56db','#b91c1c'],
                     title='Match Quality Breakdown')
        fig.update_layout(paper_bgcolor=CHART_BG, font_color=FONT_COLOR,
                          font_size=13, height=320,
                          title_font_size=16, title_font_color=FONT_COLOR)
        st.plotly_chart(fig, use_container_width=True)

    all_skills = [s for sl in matches_df['Skills_Matched'] for s in sl]
    if all_skills:
        skill_counts = Counter(all_skills).most_common(15)
        skill_df = pd.DataFrame(skill_counts, columns=['Skill', 'Count'])
        fig = px.bar(skill_df, x='Count', y='Skill', orientation='h',
                     color='Count',
                     color_continuous_scale=[[0,'#dbeafe'],[0.5,'#1a56db'],[1,'#0a2540']],
                     title='Top 15 Most Matched Skills')
        fig.update_layout(paper_bgcolor=CHART_BG, plot_bgcolor=PLOT_BG,
                          font_color=FONT_COLOR, font_size=13, height=420,
                          yaxis={'autorange':'reversed','color':FONT_COLOR},
                          coloraxis_showscale=False,
                          xaxis=dict(gridcolor=GRID_COLOR, color=FONT_COLOR),
                          title_font_size=16, title_font_color=FONT_COLOR)
        st.plotly_chart(fig, use_container_width=True)

    if 'Resume_Category' in top1.columns:
        cat = top1.groupby('Resume_Category')['Final_Score'].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(cat, x='Resume_Category', y='Final_Score',
                     color='Final_Score', color_continuous_scale='RdYlGn',
                     range_color=[0,1], title='Average Match Score by Resume Category')
        fig.update_layout(paper_bgcolor=CHART_BG, plot_bgcolor=PLOT_BG,
                          font_color=FONT_COLOR, font_size=13, height=400,
                          xaxis_tickangle=-40, xaxis=dict(color=FONT_COLOR),
                          coloraxis_showscale=False,
                          yaxis=dict(gridcolor=GRID_COLOR, color=FONT_COLOR),
                          title_font_size=16, title_font_color=FONT_COLOR)
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 3: HOW IT WORKS
# ══════════════════════════════════════════════════════════════════════════
elif page == "ℹ️ How It Works":
    st.markdown("<div class='section-header'>How the Matching Engine Works</div>", unsafe_allow_html=True)

    steps = [
        ("1. Resume Processing", "Your resume is cleaned (HTML removed, lowercased, normalized) then analyzed to extract hard technical skills from a database of 120+ skills, detect your education level (None → PhD), and detect your experience level (Entry / Mid / Senior)."),
        ("2. BERT Embeddings", "The cleaned resume text is encoded using all-MiniLM-L6-v2, a BERT-based sentence transformer. This converts your resume into a 384-dimensional vector that captures the semantic meaning of your experience — not just keywords."),
        ("3. Matching Against 124k+ Jobs", "Your resume vector is compared against pre-computed embeddings for every job posting using cosine similarity. Three additional signals are computed: skill overlap, education alignment, and experience level match."),
        ("4. Weighted Final Score", "All four signals are combined into one final score:\nFinal Score = 40% Skill Overlap + 20% Education + 20% Experience + 20% Cosine Similarity"),
        ("5. Top-K Results", "Jobs are ranked by final score and your top matches are returned with a full breakdown of why each job was recommended — plus a direct link to apply on LinkedIn."),
    ]

    for title, desc in steps:
        st.markdown(f"""
        <div class='match-card'>
            <div style='font-family:Plus Jakarta Sans,sans-serif; font-weight:700;
                        color:#0a2540; font-size:1.1rem; margin-bottom:0.5rem;'>{title}</div>
            <div style='color:#374151; font-size:1rem; line-height:1.85;
                        white-space:pre-line;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Scoring Formula</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
        <table style='width:100%; border-collapse:collapse; font-size:1rem;'>
            <tr style='border-bottom:2px solid #dde3ea;'>
                <th style='padding:0.8rem 0.6rem; text-align:left; color:#0a2540; font-family:Plus Jakarta Sans,sans-serif;'>Component</th>
                <th style='padding:0.8rem 0.6rem; text-align:center; color:#0a2540; font-family:Plus Jakarta Sans,sans-serif;'>Weight</th>
                <th style='padding:0.8rem 0.6rem; text-align:left; color:#0a2540; font-family:Plus Jakarta Sans,sans-serif;'>What it measures</th>
            </tr>
            <tr style='border-bottom:1px solid #f0f4f8;'>
                <td style='padding:0.8rem 0.6rem; color:#111827; font-weight:500;'>Skill Overlap</td>
                <td style='padding:0.8rem 0.6rem; text-align:center; color:#047857; font-weight:700; font-size:1.1rem;'>40%</td>
                <td style='padding:0.8rem 0.6rem; color:#374151;'>Fraction of job's required skills found in your resume</td>
            </tr>
            <tr style='border-bottom:1px solid #f0f4f8;'>
                <td style='padding:0.8rem 0.6rem; color:#111827; font-weight:500;'>Education Match</td>
                <td style='padding:0.8rem 0.6rem; text-align:center; color:#0284c7; font-weight:700; font-size:1.1rem;'>20%</td>
                <td style='padding:0.8rem 0.6rem; color:#374151;'>Your education level vs job requirement</td>
            </tr>
            <tr style='border-bottom:1px solid #f0f4f8;'>
                <td style='padding:0.8rem 0.6rem; color:#111827; font-weight:500;'>Experience Match</td>
                <td style='padding:0.8rem 0.6rem; text-align:center; color:#1a56db; font-weight:700; font-size:1.1rem;'>20%</td>
                <td style='padding:0.8rem 0.6rem; color:#374151;'>Entry / Mid / Senior level alignment</td>
            </tr>
            <tr>
                <td style='padding:0.8rem 0.6rem; color:#111827; font-weight:500;'>Cosine Similarity</td>
                <td style='padding:0.8rem 0.6rem; text-align:center; color:#0a2540; font-weight:700; font-size:1.1rem;'>20%</td>
                <td style='padding:0.8rem 0.6rem; color:#374151;'>Semantic meaning match via BERT embeddings</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Evaluation Metric: Precision@5</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
        <div style='color:#334155; font-size:1rem; line-height:2;'>
            <b style='color:#1a56db;'>Precision@5</b> measures how many of the top 5
            recommended jobs are actually relevant to the resume's career field.<br><br>
            <b style='color:#0a2540;'>Formula:</b> Precision@5 = Relevant jobs in top 5 ÷ 5<br><br>
            <b style='color:#047857; font-size:1.1rem;'>BERT Result: 70.5%</b> — meaning on average,
            3–4 out of every 5 recommended jobs are genuinely relevant.<br>
            <span style='color:#9ca3af;'>BM25 baseline: 69.5% (BERT wins by 1 point)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
