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

# ── Custom CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap');

/* ═══════════════════════════════════════════
   COLOR PALETTE
   BG:        #0d1117  (near-black slate)
   Card:      #161b22  (dark slate)
   Border:    #30363d  (medium slate)
   Text:      #e6edf3  (off-white)
   Muted:     #8b949e  (grey — captions/labels)
   Violet:    #a78bfa  (brand — buttons, borders, section headers ONLY)
   Teal:      #2dd4bf  (secondary — links, company names, metric numbers)
   Green:     #3fb950  (semantic — strong match)
   Amber:     #d29922  (semantic — partial match)
   Red:       #f85149  (semantic — weak match)
   Charts:    violet, teal, green, amber, red, pink — always distinct
═══════════════════════════════════════════ */

/* ── Force dark everywhere ── */
html, body, [class*="css"],
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"],
.main {
    background-color: #0d1117 !important;
    color: #e6edf3 !important;
    font-family: 'Inter', sans-serif;
    font-size: 16px;
}
.block-container, [data-testid="block-container"] {
    background-color: #0d1117 !important;
    padding: 2rem 3rem;
    max-width: 1400px;
}
p, span, div, label, li, td, th { color: #e6edf3; }
h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; color: #f0f6fc; }

/* ── Sidebar ── */
section[data-testid="stSidebar"],
[data-testid="stSidebar"] > div {
    background-color: #161b22 !important;
    border-right: 1px solid #30363d !important;
}
[data-testid="stRadio"] label, [data-testid="stRadio"] div { color: #e6edf3 !important; }
[data-testid="stSlider"] label, [data-testid="stSlider"] div { color: #e6edf3 !important; }
[data-testid="stTextArea"] label { color: #e6edf3 !important; }
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] div,
[data-testid="stFileUploader"] span,
[data-testid="stFileUploadDropzone"] {
    color: #e6edf3 !important;
    background-color: #161b22 !important;
    border-color: #30363d !important;
}
[data-testid="stCaptionContainer"] { color: #8b949e !important; }

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, #1a1040 0%, #2d1b69 45%, #1e3a5f 100%);
    border: 1px solid rgba(167,139,250,0.4);
    border-radius: 20px;
    padding: 3rem 4rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -20%;
    right: -5%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(167,139,250,0.12) 0%, transparent 65%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.8rem;
    font-weight: 700;
    color: #f0f6fc;
    margin: 0 0 0.5rem 0;
    line-height: 1.1;
    letter-spacing: -0.02em;
    text-shadow: 0 2px 20px rgba(0,0,0,0.6);
}
.hero-sub {
    color: #c4b5fd;
    font-size: 1.05rem;
    font-weight: 600;
    margin: 0 0 0.5rem 0;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* ── Metric Cards ── */
.metric-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 1.6rem 1.5rem;
    text-align: center;
}
.metric-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #2dd4bf;
    margin: 0;
}
.metric-label {
    font-size: 0.88rem;
    color: #8b949e;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin: 0.4rem 0 0 0;
    font-weight: 600;
}

/* ── Match Cards ── */
.match-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 16px;
    padding: 1.8rem 2.2rem;
    margin-bottom: 1.4rem;
    transition: border-color 0.25s, box-shadow 0.25s;
}
.match-card:hover {
    border-color: #a78bfa;
    box-shadow: 0 4px 24px rgba(167,139,250,0.15);
}
.match-rank {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    color: #8b949e;
    margin-bottom: 0.4rem;
}
.match-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #f0f6fc;
    margin: 0 0 0.25rem 0;
    line-height: 1.25;
}
.match-company {
    color: #2dd4bf;
    font-size: 1.05rem;
    font-weight: 500;
    margin: 0 0 1rem 0;
}
.score-bar-bg {
    background: #21262d;
    border-radius: 99px;
    height: 14px;
    width: 100%;
    margin: 0.5rem 0;
}
.score-bar-fill {
    height: 14px;
    border-radius: 99px;
    transition: width 0.6s ease;
}
.skill-tag {
    display: inline-block;
    background: rgba(167,139,250,0.12);
    color: #c4b5fd;
    border: 1px solid rgba(167,139,250,0.35);
    border-radius: 8px;
    padding: 0.28rem 0.85rem;
    font-size: 0.88rem;
    font-weight: 600;
    margin: 0.2rem 0.2rem 0.2rem 0;
}
.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.55rem;
    font-weight: 700;
    color: #f0f6fc;
    border-left: 4px solid #a78bfa;
    padding-left: 1rem;
    margin: 1.8rem 0 1.2rem 0;
}
.info-box {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 1.3rem 1.6rem;
    margin-bottom: 1.2rem;
}
.stTextArea textarea {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    color: #e6edf3 !important;
    font-family: 'Inter', sans-serif !important;
    border-radius: 12px !important;
    font-size: 1rem !important;
    line-height: 1.6 !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6d28d9, #a78bfa) !important;
    color: #ffffff !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2rem !important;
    font-size: 1.15rem !important;
    letter-spacing: 0.03em !important;
    width: 100% !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #7c3aed, #c4b5fd) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(167,139,250,0.35) !important;
}
.sidebar-section {
    background: #0d1117;
    border-radius: 12px;
    padding: 1.2rem 1.3rem;
    margin-bottom: 1rem;
    border: 1px solid #30363d;
}
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

# GitHub Release URL for the large embeddings file
# PASTE YOUR GITHUB RELEASE DOWNLOAD URL BELOW after uploading job_embeddings.npy to a release
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
    if score >= 0.75: return "#3fb950"
    elif score >= 0.55: return "#d29922"
    return "#f85149"

def score_label(score):
    if score >= 0.75: return "🟢 Strong Match"
    elif score >= 0.55: return "🟡 Partial Match"
    return "🔴 Weak Match"

# ── Data loading — cached so shared across all users ───────────────────────
@st.cache_resource(show_spinner="Loading model (first time only)...")
def load_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

@st.cache_resource(show_spinner="Loading job data (first time only)...")
def load_all_data():
    """Load CSVs from the repo and download embeddings from GitHub Releases.
    Uses cache_resource so this runs exactly once, shared across all users.
    """
    import requests

    app_dir = os.path.dirname(os.path.abspath(__file__))

    # Load CSVs directly from the repo (no download needed)
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

    # Download embeddings from GitHub Releases (only if not already cached)
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
    <div style='text-align:center; padding: 1.2rem 0 1.8rem 0;'>
        <div style='font-family: Space Grotesk, sans-serif; font-size: 1.6rem;
                    font-weight: 700; color: #f0f6fc; letter-spacing:-0.01em;'>Smart Practicum</div>
        <div style='color: #a78bfa; font-size: 0.82rem;
                    text-transform: uppercase; letter-spacing: 0.14em; margin-top:0.3rem;
                    font-weight: 600;'>
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
        <div style='color:#a78bfa; font-size:0.8rem;
                    text-transform:uppercase; letter-spacing:0.12em;
                    margin-bottom:0.6rem; font-weight:700;'>Data</div>
        <div style='color:#e6edf3; font-size:0.9rem; line-height:1.9;'>
            ✅ 124k+ LinkedIn jobs<br>
            ✅ Auto-loaded on startup<br>
            <span style='color:#8b949e; font-size:0.82rem;'>
            No setup needed</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='sidebar-section'>
        <div style='color:#a78bfa; font-size:0.8rem;
                    text-transform:uppercase; letter-spacing:0.12em;
                    margin-bottom:0.6rem; font-weight:700;'>Model</div>
        <div style='color:#e6edf3; font-size:0.9rem; line-height:1.9;'>
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
    <p style='color:#e2e8f0; margin:0.6rem 0 0 0; font-size:1.2rem; line-height:1.7; max-width:700px;'>
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
        st.markdown("<div class='section-header'>Your Resume</div>",
                    unsafe_allow_html=True)

        input_method = st.radio("How would you like to add your resume?",
                                 ["📋 Paste Resume Text", "📄 Upload PDF"],
                                 horizontal=True)

        resume_text = ""
        if input_method == "📋 Paste Resume Text":
            resume_text = st.text_area(
                "Paste your resume text here",
                height=280,
                placeholder="Copy and paste the full text of your resume here...\n\nInclude: skills, work experience, education, projects"
            )
        else:
            uploaded = st.file_uploader("Upload your resume PDF", type=["pdf"])
            if uploaded:
                try:
                    import pdfplumber
                    with pdfplumber.open(uploaded) as pdf:
                        resume_text = "\n".join(
                            page.extract_text() or "" for page in pdf.pages
                        )
                    st.success(f"✅ PDF loaded — {len(resume_text):,} characters extracted")
                except ImportError:
                    st.error("pdfplumber not installed — contact the app administrator.")
                except Exception as e:
                    st.error(f"Could not read PDF: {e}")

        top_k = st.slider("Number of job matches to show", 3, 10, 5)
        run_btn = st.button("🔍 Find My Top Jobs", use_container_width=True)

        if resume_text.strip():
            clean = clean_text(resume_text)
            skills = extract_hard_skills(clean)
            edu    = detect_education_level(clean)
            exp    = detect_experience_level(clean)
            edu_labels = {0:"None detected",1:"Associate",2:"Bachelor's",3:"Master's",4:"PhD"}

            st.markdown("<div class='section-header'>Resume Analysis</div>",
                        unsafe_allow_html=True)
            st.markdown(f"""
            <div class='info-box'>
                <div style='color:#94a3b8; font-size:0.82rem;
                            text-transform:uppercase; letter-spacing:0.1em;
                            margin-bottom:0.8rem; font-weight:600;'>Detected Profile</div>
                <div style='color:#f1f5f9; font-size:1rem; line-height:2;'>
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
        st.markdown("<div class='section-header'>Your Top Job Matches</div>",
                    unsafe_allow_html=True)

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
                    [clean[:1000]],
                    normalize_embeddings=True,
                    show_progress_bar=False
                )[0].astype(np.float32)

                r_skills = set(skills)
                job_edu  = jobs_df['edu_required'].values.astype(np.float32)
                level_map = {'entry':1,'mid':2,'senior':3,'unknown':0}
                job_exp_num = np.array([level_map.get(e, 0)
                                        for e in jobs_df['exp_required'].tolist()],
                                       dtype=np.float32)

                cos_scores = (job_embeddings @ resume_vec).astype(np.float32)

                job_skill_sets = [set(s) if isinstance(s, list) else set()
                                  for s in jobs_df['required_skills']]
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

                final_scores = (skill_scores * 0.40 +
                                edu_scores   * 0.20 +
                                exp_scores   * 0.20 +
                                cos_scores   * 0.20)

                top_k_idx = np.argpartition(final_scores, -top_k)[-top_k:]
                top_k_idx = top_k_idx[np.argsort(final_scores[top_k_idx])[::-1]]

            for rank, j_idx in enumerate(top_k_idx, start=1):
                job_row  = jobs_df.iloc[j_idx]
                score    = float(final_scores[j_idx])
                matched  = sorted(r_skills & job_skill_sets[j_idx])
                color    = score_color(score)
                label    = score_label(score)
                pct      = int(score * 100)

                st.markdown(f"""
                <div class='match-card'>
                    <div class='match-rank'>Rank #{rank} · {label}</div>
                    <div class='match-title'>{job_row.get('title','Unknown')}</div>
                    <div class='match-company'>
                        {job_row.get('company_name', job_row.get('company','Unknown'))}
                        {f"· {job_row.get('location','')}" if job_row.get('location') else ''}
                    </div>
                    <div style='display:flex; align-items:center; gap:1rem; margin:0.8rem 0;'>
                        <div class='score-bar-bg' style='flex:1;'>
                            <div class='score-bar-fill'
                                 style='width:{pct}%; background:{color};'></div>
                        </div>
                        <div style='font-family:Space Grotesk,sans-serif; font-weight:700;
                                    color:{color}; font-size:1.5rem; min-width:55px;'>
                            {pct}%
                        </div>
                    </div>
                    <div style='display:grid; grid-template-columns:1fr 1fr 1fr;
                                gap:0.6rem; margin:1rem 0;'>
                        <div style='background:#0d1117; border:1px solid #30363d;
                                    border-radius:10px; padding:0.75rem; text-align:center;'>
                            <div style='color:#3fb950; font-size:1.3rem;
                                        font-weight:700;'>{int(skill_scores[j_idx]*100)}%</div>
                            <div style='color:#8b949e; font-size:0.82rem;
                                        text-transform:uppercase; font-weight:600; margin-top:0.2rem;'>Skills</div>
                        </div>
                        <div style='background:#0d1117; border:1px solid #30363d;
                                    border-radius:10px; padding:0.75rem; text-align:center;'>
                            <div style='color:#2dd4bf; font-size:1.3rem;
                                        font-weight:700;'>{int(edu_scores[j_idx]*100)}%</div>
                            <div style='color:#8b949e; font-size:0.82rem;
                                        text-transform:uppercase; font-weight:600; margin-top:0.2rem;'>Education</div>
                        </div>
                        <div style='background:#0d1117; border:1px solid #30363d;
                                    border-radius:10px; padding:0.75rem; text-align:center;'>
                            <div style='color:#a78bfa; font-size:1.3rem;
                                        font-weight:700;'>{int(cos_scores[j_idx]*100)}%</div>
                            <div style='color:#8b949e; font-size:0.82rem;
                                        text-transform:uppercase; font-weight:600; margin-top:0.2rem;'>Semantic</div>
                        </div>
                    </div>
                    {"<div style='margin-top:0.5rem;'>" + "".join(f"<span class='skill-tag'>✓ {s}</span>" for s in matched) + "</div>" if matched else "<div style='color:#64748b; font-size:0.9rem; margin-top:0.5rem;'>No skill overlap detected</div>"}
                </div>
                """, unsafe_allow_html=True)

        elif not resume_text.strip():
            st.markdown("""
            <div style='text-align:center; padding:5rem 2rem;
                        border: 2px dashed rgba(56,189,248,0.35);
                        border-radius:18px; background: rgba(56,189,248,0.05);'>
                <div style='font-size:3.5rem; margin-bottom:1.2rem;'>📄</div>
                <div style='font-family:Space Grotesk,sans-serif; font-size:1.3rem;
                            font-weight:600; color:#e2e8f0; line-height:1.7;'>
                    Paste your resume or upload a PDF<br>to see your job matches
                </div>
                <div style='color:#94a3b8; font-size:1rem; margin-top:0.8rem;'>
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

    st.markdown("<div class='section-header'>Career Services Dashboard</div>",
                unsafe_allow_html=True)

    try:
        _, _, matches_df = load_all_data()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        st.stop()

    if matches_df is None:
        st.warning("Results file not available. Run your BERT notebook first to generate it.")
        st.stop()

    top1 = matches_df[matches_df['Resume_Rank'] == 1]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='metric-card'>
            <p class='metric-value'>{matches_df['Resume_Index'].nunique():,}</p>
            <p class='metric-label'>Resumes Processed</p></div>""",
            unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='metric-card'>
            <p class='metric-value'>{matches_df['Job_Index'].nunique():,}</p>
            <p class='metric-label'>Jobs Matched</p></div>""",
            unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='metric-card'>
            <p class='metric-value'>{top1['Final_Score'].mean()*100:.1f}%</p>
            <p class='metric-label'>Avg Best Score</p></div>""",
            unsafe_allow_html=True)
    with c4:
        good = (top1['Final_Score'] >= 0.65).sum()
        st.markdown(f"""<div class='metric-card'>
            <p class='metric-value'>{good:,}</p>
            <p class='metric-label'>Strong Matches</p></div>""",
            unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        fig = px.histogram(top1, x='Final_Score', nbins=30,
                           color_discrete_sequence=['#2dd4bf'],
                           title='Best Match Score Distribution')
        fig.add_vline(x=top1['Final_Score'].mean(), line_dash='dash',
                      line_color='#d29922',
                      annotation_text=f"Mean: {top1['Final_Score'].mean():.2f}",
                      annotation_font_color='#d29922',
                      annotation_font_size=14)
        fig.update_layout(
            paper_bgcolor='#161b22', plot_bgcolor='#0d1117',
            font_color='#e6edf3', font_size=14, height=340,
            xaxis=dict(gridcolor='#21262d', color='#e6edf3'),
            yaxis=dict(gridcolor='#21262d', color='#e6edf3'),
            title_font_size=18, title_font_color='#f0f6fc'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        quality = {
            'Strong (≥75%)':  (top1['Final_Score'] >= 0.75).sum(),
            'Good (55-75%)':  ((top1['Final_Score'] >= 0.55) & (top1['Final_Score'] < 0.75)).sum(),
            'Weak (<55%)':    (top1['Final_Score'] < 0.55).sum()
        }
        fig = px.pie(values=list(quality.values()),
                     names=list(quality.keys()),
                     color_discrete_sequence=['#3fb950','#d29922','#f85149'],
                     title='Match Quality Breakdown')
        fig.update_layout(
            paper_bgcolor='#161b22', font_color='#e6edf3',
            font_size=14, height=340,
            title_font_size=18, title_font_color='#f0f6fc'
        )
        st.plotly_chart(fig, use_container_width=True)

    all_skills = [s for sl in matches_df['Skills_Matched'] for s in sl]
    if all_skills:
        skill_counts = Counter(all_skills).most_common(15)
        skill_df = pd.DataFrame(skill_counts, columns=['Skill', 'Count'])
        fig = px.bar(skill_df, x='Count', y='Skill', orientation='h',
                     color='Count', color_continuous_scale=[[0,'#161b22'],[0.5,'#2dd4bf'],[1,'#a78bfa']],
                     title='Top 15 Most Matched Skills')
        fig.update_layout(
            paper_bgcolor='#161b22', plot_bgcolor='#0d1117',
            font_color='#e6edf3', font_size=14, height=450,
            yaxis={'autorange':'reversed', 'color':'#e6edf3'},
            coloraxis_showscale=False,
            xaxis=dict(gridcolor='#21262d', color='#e6edf3'),
            title_font_size=18, title_font_color='#f0f6fc'
        )
        st.plotly_chart(fig, use_container_width=True)

    if 'Resume_Category' in top1.columns:
        cat = top1.groupby('Resume_Category')['Final_Score'].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(cat, x='Resume_Category', y='Final_Score',
                     color='Final_Score', color_continuous_scale='RdYlGn',
                     range_color=[0,1],
                     title='Average Match Score by Resume Category')
        fig.update_layout(
            paper_bgcolor='#161b22', plot_bgcolor='#0d1117',
            font_color='#e6edf3', font_size=14, height=420,
            xaxis_tickangle=-40, xaxis=dict(color='#e6edf3'),
            coloraxis_showscale=False,
            yaxis=dict(gridcolor='#21262d', color='#e6edf3'),
            title_font_size=18, title_font_color='#f0f6fc'
        )
        st.plotly_chart(fig, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 3: HOW IT WORKS
# ══════════════════════════════════════════════════════════════════════════
elif page == "ℹ️ How It Works":
    st.markdown("<div class='section-header'>How the Matching Engine Works</div>",
                unsafe_allow_html=True)

    steps = [
        ("1. Resume Processing", "Your resume is cleaned (HTML removed, lowercased, normalized) then analyzed to extract hard technical skills from a database of 120+ skills, detect your education level (None → PhD), and detect your experience level (Entry / Mid / Senior)."),
        ("2. BERT Embeddings", "The cleaned resume text is encoded using all-MiniLM-L6-v2, a BERT-based sentence transformer. This converts your resume into a 384-dimensional vector that captures the semantic meaning of your experience — not just keywords."),
        ("3. Matching Against 124k+ Jobs", "Your resume vector is compared against pre-computed embeddings for every job posting using cosine similarity. Three additional signals are computed: skill overlap, education alignment, and experience level match."),
        ("4. Weighted Final Score", "All four signals are combined into one final score using the formula:\nFinal Score = 40% Skill Overlap + 20% Education + 20% Experience + 20% Cosine Similarity"),
        ("5. Top-K Results", "Jobs are ranked by final score and your top matches are returned with a full breakdown of why each job was recommended."),
    ]

    for title, desc in steps:
        st.markdown(f"""
        <div class='match-card'>
            <div style='font-family:Space Grotesk,sans-serif; font-weight:700;
                        color:#a78bfa; font-size:1.2rem; margin-bottom:0.6rem;'>
                {title}
            </div>
            <div style='color:#e6edf3; font-size:1.05rem; line-height:1.9;
                        white-space:pre-line;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Scoring Formula</div>",
                unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
        <table style='width:100%; border-collapse:collapse; color:#e6edf3; font-size:1.05rem;'>
            <tr style='border-bottom:2px solid #30363d;'>
                <th style='padding:0.9rem 0.6rem; text-align:left; color:#a78bfa; font-size:1.1rem;'>Component</th>
                <th style='padding:0.9rem 0.6rem; text-align:center; color:#a78bfa; font-size:1.1rem;'>Weight</th>
                <th style='padding:0.9rem 0.6rem; text-align:left; color:#a78bfa; font-size:1.1rem;'>What it measures</th>
            </tr>
            <tr style='border-bottom:1px solid #21262d;'>
                <td style='padding:0.9rem 0.6rem; color:#f0f6fc;'>Skill Overlap</td>
                <td style='padding:0.9rem 0.6rem; text-align:center; color:#3fb950; font-weight:700; font-size:1.2rem;'>40%</td>
                <td style='padding:0.9rem 0.6rem;'>Fraction of job's required skills found in your resume</td>
            </tr>
            <tr style='border-bottom:1px solid #21262d;'>
                <td style='padding:0.9rem 0.6rem; color:#f0f6fc;'>Education Match</td>
                <td style='padding:0.9rem 0.6rem; text-align:center; color:#2dd4bf; font-weight:700; font-size:1.2rem;'>20%</td>
                <td style='padding:0.9rem 0.6rem;'>Your education level vs job requirement</td>
            </tr>
            <tr style='border-bottom:1px solid #21262d;'>
                <td style='padding:0.9rem 0.6rem; color:#f0f6fc;'>Experience Match</td>
                <td style='padding:0.9rem 0.6rem; text-align:center; color:#a78bfa; font-weight:700; font-size:1.2rem;'>20%</td>
                <td style='padding:0.9rem 0.6rem;'>Entry / Mid / Senior level alignment</td>
            </tr>
            <tr>
                <td style='padding:0.9rem 0.6rem; color:#f0f6fc;'>Cosine Similarity</td>
                <td style='padding:0.9rem 0.6rem; text-align:center; color:#d29922; font-weight:700; font-size:1.2rem;'>20%</td>
                <td style='padding:0.9rem 0.6rem;'>Semantic meaning match via BERT embeddings</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Evaluation Metric: Precision@5</div>",
                unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
        <div style='color:#f1f5f9; font-size:1.05rem; line-height:2;'>
            <b style='color:#60a5fa;'>Precision@5</b> measures how many of the top 5
            recommended jobs are actually relevant to the resume's career field.<br><br>
            <b style='color:#60a5fa;'>Formula:</b>
            Precision@5 = Relevant jobs in top 5 ÷ 5<br><br>
            <b style='color:#4ade80; font-size:1.1rem;'>BERT Result: 70.5%</b> — meaning on average,
            3–4 out of every 5 recommended jobs are genuinely relevant.<br>
            <span style='color:#94a3b8;'>BM25 baseline: 69.5% (BERT wins by 1 point)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
