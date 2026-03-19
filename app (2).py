import streamlit as st
import pandas as pd
import numpy as np
import re
import os
import ast
from collections import Counter

# ── Auto-download data files from Google Drive ────────────────────────────
JOBS_CSV  = '/tmp/jobs_cleaned.csv'
JOBS_EMB  = '/tmp/job_embeddings.npy'
RESULTS_CSV = '/tmp/smart_practicum_results.csv'

DRIVE_FILES = {
    JOBS_CSV:    '1EQGIwPnsJAq0qkEy9bOCigq4BPfaXuTb',
    JOBS_EMB:    '194QIDw9Kdr5OtpGTKctNB8tdloAkpR1S',
    RESULTS_CSV: '1JdI0iYelpesaElQJ2S1lXLC7ytmFe6n2',
}

def download_data_files():
    try:
        import gdown
    except ImportError:
        os.system('pip install -q gdown')
        import gdown

    for dest, file_id in DRIVE_FILES.items():
        if not os.path.exists(dest):
            with st.spinner(f'Downloading {os.path.basename(dest)} from Google Drive...'):
                url = f'https://drive.google.com/uc?id={file_id}'
                gdown.download(url, dest, quiet=True, fuzzy=True)

download_data_files()

# ── Page config ───────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Practicum",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

h1, h2, h3 { font-family: 'Syne', sans-serif; }

.main { background: #0f0f13; }
.block-container { padding: 2rem 2.5rem; }

.hero-banner {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 16px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(99,179,237,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.4rem 0;
    line-height: 1.1;
}
.hero-sub {
    color: #63b3ed;
    font-size: 1rem;
    font-weight: 300;
    margin: 0;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.metric-card {
    background: #1a1a2e;
    border: 1px solid rgba(99,179,237,0.15);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #63b3ed;
    margin: 0;
}
.metric-label {
    font-size: 0.78rem;
    color: #718096;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin: 0.2rem 0 0 0;
}

.match-card {
    background: #1a1a2e;
    border: 1px solid rgba(99,179,237,0.12);
    border-radius: 14px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.match-card:hover { border-color: rgba(99,179,237,0.4); }
.match-rank {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #4a5568;
    margin-bottom: 0.3rem;
}
.match-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 0 0 0.15rem 0;
}
.match-company {
    color: #63b3ed;
    font-size: 0.88rem;
    margin: 0 0 0.8rem 0;
}
.score-bar-bg {
    background: #2d3748;
    border-radius: 99px;
    height: 8px;
    width: 100%;
    margin: 0.5rem 0;
}
.score-bar-fill {
    height: 8px;
    border-radius: 99px;
    transition: width 0.6s ease;
}
.skill-tag {
    display: inline-block;
    background: rgba(99,179,237,0.12);
    color: #63b3ed;
    border: 1px solid rgba(99,179,237,0.25);
    border-radius: 6px;
    padding: 0.18rem 0.6rem;
    font-size: 0.75rem;
    margin: 0.18rem 0.18rem 0.18rem 0;
    font-family: 'DM Sans', monospace;
}
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #e2e8f0;
    border-left: 3px solid #63b3ed;
    padding-left: 0.8rem;
    margin: 1.5rem 0 1rem 0;
}
.info-box {
    background: rgba(99,179,237,0.06);
    border: 1px solid rgba(99,179,237,0.2);
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
}
.stTextArea textarea {
    background: #1a1a2e !important;
    border: 1px solid rgba(99,179,237,0.2) !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    border-radius: 10px !important;
}
.stButton > button {
    background: linear-gradient(135deg, #2b6cb0, #63b3ed) !important;
    color: white !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 2rem !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.05em !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(99,179,237,0.3) !important;
}
.sidebar-section {
    background: #1a1a2e;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 1px solid rgba(99,179,237,0.1);
}
</style>
""", unsafe_allow_html=True)

# ── Constants — same as notebook ──────────────────────────────────────────
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

# ── Helper functions — identical to notebook ───────────────────────────────
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

def edu_score(r_edu, j_edu):
    if j_edu == 0: return 0.7
    diff = r_edu - j_edu
    if diff >= 0: return 1.0
    elif diff == -1: return 0.5
    return 0.0

def exp_score(r_exp, j_exp):
    level_map = {'entry': 1, 'mid': 2, 'senior': 3, 'unknown': 0}
    r_val = level_map.get(r_exp, 0)
    j_val = level_map.get(j_exp, 0)
    if r_val == 0 or j_val == 0: return 0.5
    diff = abs(r_val - j_val)
    if diff == 0: return 1.0
    elif diff == 1: return 0.5
    return 0.0

def score_color(score):
    if score >= 0.75: return "#48bb78"   # green
    elif score >= 0.55: return "#ed8936" # orange
    return "#fc8181"                      # red

def score_label(score):
    if score >= 0.75: return "🟢 Strong Match"
    elif score >= 0.55: return "🟡 Partial Match"
    return "🔴 Weak Match"

# ── Load pre-computed data ─────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_jobs_data(jobs_csv_path, jobs_emb_path):
    try:
        jobs_df = pd.read_csv(jobs_csv_path, encoding='utf-8')
    except Exception:
        jobs_df = pd.read_csv(jobs_csv_path, encoding='latin-1')
    jobs_df['required_skills'] = jobs_df['required_skills'].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else []
    )
    job_embeddings = np.load(jobs_emb_path)
    return jobs_df, job_embeddings

@st.cache_resource(show_spinner=False)
def load_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem 0;'>
        <div style='font-family: Syne, sans-serif; font-size: 1.4rem;
                    font-weight: 800; color: #e2e8f0;'>Smart Practicum</div>
        <div style='color: #63b3ed; font-size: 0.75rem;
                    text-transform: uppercase; letter-spacing: 0.1em;'>
            AI Job Matching Engine</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio("", [
        "🔍 Match My Resume",
        "📊 Career Dashboard",
        "ℹ️ How It Works"
    ], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("""
    <div class='sidebar-section'>
        <div style='color:#63b3ed; font-size:0.75rem;
                    text-transform:uppercase; letter-spacing:0.1em;
                    margin-bottom:0.5rem;'>Data</div>
        <div style='color:#a0aec0; font-size:0.8rem; line-height:1.6;'>
            ✅ 124k+ LinkedIn jobs<br>
            ✅ Auto-loaded on startup<br>
            <span style='color:#4a5568; font-size:0.72rem;'>
            No setup needed</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='sidebar-section'>
        <div style='color:#63b3ed; font-size:0.75rem;
                    text-transform:uppercase; letter-spacing:0.1em;
                    margin-bottom:0.5rem;'>Model</div>
        <div style='color:#a0aec0; font-size:0.8rem; line-height:1.6;'>
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
    <p style='color:#a0aec0; margin:0.5rem 0 0 0; font-size:0.95rem;'>
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

        jobs_csv = JOBS_CSV
        jobs_emb = JOBS_EMB

        st.markdown("---")

        # Resume input — paste text OR upload PDF
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
                    st.error("Install pdfplumber: pip install pdfplumber")
                except Exception as e:
                    st.error(f"Could not read PDF: {e}")

        top_k = st.slider("Number of job matches to show", 3, 10, 5)
        run_btn = st.button("🔍 Find My Top Jobs", use_container_width=True)

        # Show resume analysis preview
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
                <div style='color:#718096; font-size:0.75rem;
                            text-transform:uppercase; letter-spacing:0.08em;
                            margin-bottom:0.6rem;'>Detected Profile</div>
                <div style='color:#e2e8f0; font-size:0.88rem; line-height:1.8;'>
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

    # ── Results column ────────────────────────────────────────────────────
    with col_right:
        st.markdown("<div class='section-header'>Your Top Job Matches</div>",
                    unsafe_allow_html=True)

        if run_btn and resume_text.strip():
            # Load data
            if not os.path.exists(jobs_csv):
                st.error(f"Cannot find: {jobs_csv}\nMake sure the path is correct.")
                st.stop()
            if not os.path.exists(jobs_emb):
                st.error(f"Cannot find: {jobs_emb}\nMake sure the path is correct.")
                st.stop()

            with st.spinner("Loading model and computing your matches..."):
                jobs_df, job_embeddings = load_jobs_data(jobs_csv, jobs_emb)
                model = load_model()

                # Process resume
                clean  = clean_text(resume_text)
                skills = extract_hard_skills(clean)
                edu    = detect_education_level(clean)
                exp    = detect_experience_level(clean)

                # Embed resume
                resume_vec = model.encode(
                    [clean[:1000]],
                    normalize_embeddings=True,
                    show_progress_bar=False
                )[0].astype(np.float32)

                # Score all jobs
                r_skills = set(skills)
                job_edu  = jobs_df['edu_required'].values.astype(np.float32)
                level_map = {'entry':1,'mid':2,'senior':3,'unknown':0}
                job_exp_num = np.array([level_map.get(e,0)
                                        for e in jobs_df['exp_required'].tolist()],
                                       dtype=np.float32)

                # Cosine similarity
                cos_scores = (job_embeddings @ resume_vec).astype(np.float32)

                # Skill overlap
                job_skill_sets = [set(s) if isinstance(s, list) else set()
                                  for s in jobs_df['required_skills']]
                skill_scores = np.array([
                    len(r_skills & js) / len(js) if js else 0.0
                    for js in job_skill_sets
                ], dtype=np.float32)

                # Education
                edu_diff   = float(edu) - job_edu
                edu_scores = np.where(job_edu == 0, 0.7,
                             np.where(edu_diff >= 0, 1.0,
                             np.where(edu_diff >= -1, 0.5, 0.0))).astype(np.float32)

                # Experience
                r_exp_val  = level_map.get(exp, 0)
                exp_diff   = np.abs(r_exp_val - job_exp_num)
                exp_scores = np.where((r_exp_val == 0) | (job_exp_num == 0), 0.5,
                             np.where(exp_diff == 0, 1.0,
                             np.where(exp_diff == 1, 0.5, 0.0))).astype(np.float32)

                # Final weighted score
                final_scores = (skill_scores * 0.40 +
                                edu_scores   * 0.20 +
                                exp_scores   * 0.20 +
                                cos_scores   * 0.20)

                top_k_idx = np.argpartition(final_scores, -top_k)[-top_k:]
                top_k_idx = top_k_idx[np.argsort(final_scores[top_k_idx])[::-1]]

            # Display results
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
                    <div style='display:flex; align-items:center; gap:0.8rem; margin:0.6rem 0;'>
                        <div class='score-bar-bg' style='flex:1;'>
                            <div class='score-bar-fill'
                                 style='width:{pct}%; background:{color};'></div>
                        </div>
                        <div style='font-family:Syne,sans-serif; font-weight:700;
                                    color:{color}; font-size:1.1rem; min-width:45px;'>
                            {pct}%
                        </div>
                    </div>
                    <div style='display:grid; grid-template-columns:1fr 1fr 1fr;
                                gap:0.5rem; margin:0.8rem 0;'>
                        <div style='background:#0f0f1a; border-radius:8px;
                                    padding:0.5rem; text-align:center;'>
                            <div style='color:#63b3ed; font-size:0.9rem;
                                        font-weight:700;'>{int(skill_scores[j_idx]*100)}%</div>
                            <div style='color:#4a5568; font-size:0.65rem;
                                        text-transform:uppercase;'>Skills</div>
                        </div>
                        <div style='background:#0f0f1a; border-radius:8px;
                                    padding:0.5rem; text-align:center;'>
                            <div style='color:#63b3ed; font-size:0.9rem;
                                        font-weight:700;'>{int(edu_scores[j_idx]*100)}%</div>
                            <div style='color:#4a5568; font-size:0.65rem;
                                        text-transform:uppercase;'>Education</div>
                        </div>
                        <div style='background:#0f0f1a; border-radius:8px;
                                    padding:0.5rem; text-align:center;'>
                            <div style='color:#63b3ed; font-size:0.9rem;
                                        font-weight:700;'>{int(cos_scores[j_idx]*100)}%</div>
                            <div style='color:#4a5568; font-size:0.65rem;
                                        text-transform:uppercase;'>Semantic</div>
                        </div>
                    </div>
                    {"<div>" + "".join(f"<span class='skill-tag'>✓ {s}</span>" for s in matched) + "</div>" if matched else "<div style='color:#4a5568; font-size:0.8rem;'>No skill overlap detected</div>"}
                </div>
                """, unsafe_allow_html=True)

        elif not resume_text.strip():
            st.markdown("""
            <div style='text-align:center; padding:4rem 2rem;
                        color:#4a5568; border: 1px dashed #2d3748;
                        border-radius:14px;'>
                <div style='font-size:3rem; margin-bottom:1rem;'>📄</div>
                <div style='font-family:Syne,sans-serif; font-size:1.1rem;
                            color:#718096;'>
                    Paste your resume or upload a PDF<br>to see your job matches
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

    results_path = RESULTS_CSV

    if not os.path.exists(results_path):
        st.warning(f"Results file not found at: {results_path}\n\n"
                   "Run your BERT notebook first to generate this file.")
        st.stop()

    @st.cache_data
    def load_results(path):
        df = pd.read_csv(path)
        df['Skills_Matched'] = df['Skills_Matched'].apply(
            lambda x: ast.literal_eval(x) if isinstance(x, str) and x.startswith('[') else []
        )
        return df

    matches_df = load_results(results_path)
    top1 = matches_df[matches_df['Resume_Rank'] == 1]

    # Metrics
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
                           color_discrete_sequence=['#63b3ed'],
                           title='Best Match Score Distribution')
        fig.add_vline(x=top1['Final_Score'].mean(), line_dash='dash',
                      line_color='#fc8181',
                      annotation_text=f"Mean: {top1['Final_Score'].mean():.2f}",
                      annotation_font_color='#fc8181')
        fig.update_layout(
            paper_bgcolor='#1a1a2e', plot_bgcolor='#0f0f13',
            font_color='#a0aec0', height=320,
            xaxis=dict(gridcolor='#2d3748'),
            yaxis=dict(gridcolor='#2d3748')
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
                     color_discrete_sequence=['#48bb78','#ed8936','#fc8181'],
                     title='Match Quality Breakdown')
        fig.update_layout(paper_bgcolor='#1a1a2e', font_color='#a0aec0', height=320)
        st.plotly_chart(fig, use_container_width=True)

    # Skills chart
    all_skills = [s for sl in matches_df['Skills_Matched'] for s in sl]
    if all_skills:
        skill_counts = Counter(all_skills).most_common(15)
        skill_df = pd.DataFrame(skill_counts, columns=['Skill', 'Count'])
        fig = px.bar(skill_df, x='Count', y='Skill', orientation='h',
                     color='Count', color_continuous_scale='Blues',
                     title='Top 15 Most Matched Skills')
        fig.update_layout(
            paper_bgcolor='#1a1a2e', plot_bgcolor='#0f0f13',
            font_color='#a0aec0', height=420,
            yaxis={'autorange':'reversed'},
            coloraxis_showscale=False,
            xaxis=dict(gridcolor='#2d3748')
        )
        st.plotly_chart(fig, use_container_width=True)

    # Category chart
    if 'Resume_Category' in top1.columns:
        cat = top1.groupby('Resume_Category')['Final_Score'].mean().sort_values(ascending=False).reset_index()
        fig = px.bar(cat, x='Resume_Category', y='Final_Score',
                     color='Final_Score', color_continuous_scale='RdYlGn',
                     range_color=[0,1],
                     title='Average Match Score by Resume Category')
        fig.update_layout(
            paper_bgcolor='#1a1a2e', plot_bgcolor='#0f0f13',
            font_color='#a0aec0', height=400,
            xaxis_tickangle=-40,
            coloraxis_showscale=False,
            yaxis=dict(gridcolor='#2d3748')
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
            <div style='font-family:Syne,sans-serif; font-weight:700;
                        color:#63b3ed; font-size:1rem; margin-bottom:0.5rem;'>
                {title}
            </div>
            <div style='color:#a0aec0; font-size:0.88rem; line-height:1.7;
                        white-space:pre-line;'>{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Scoring Formula</div>",
                unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
        <table style='width:100%; border-collapse:collapse; color:#a0aec0; font-size:0.88rem;'>
            <tr style='border-bottom:1px solid #2d3748;'>
                <th style='padding:0.5rem; text-align:left; color:#63b3ed;'>Component</th>
                <th style='padding:0.5rem; text-align:center; color:#63b3ed;'>Weight</th>
                <th style='padding:0.5rem; text-align:left; color:#63b3ed;'>What it measures</th>
            </tr>
            <tr style='border-bottom:1px solid #1a1a2e;'>
                <td style='padding:0.5rem;'>Skill Overlap</td>
                <td style='padding:0.5rem; text-align:center; color:#48bb78; font-weight:700;'>40%</td>
                <td style='padding:0.5rem;'>Fraction of job's required skills found in your resume</td>
            </tr>
            <tr style='border-bottom:1px solid #1a1a2e;'>
                <td style='padding:0.5rem;'>Education Match</td>
                <td style='padding:0.5rem; text-align:center; color:#63b3ed; font-weight:700;'>20%</td>
                <td style='padding:0.5rem;'>Your education level vs job requirement</td>
            </tr>
            <tr style='border-bottom:1px solid #1a1a2e;'>
                <td style='padding:0.5rem;'>Experience Match</td>
                <td style='padding:0.5rem; text-align:center; color:#63b3ed; font-weight:700;'>20%</td>
                <td style='padding:0.5rem;'>Entry / Mid / Senior level alignment</td>
            </tr>
            <tr>
                <td style='padding:0.5rem;'>Cosine Similarity</td>
                <td style='padding:0.5rem; text-align:center; color:#63b3ed; font-weight:700;'>20%</td>
                <td style='padding:0.5rem;'>Semantic meaning match via BERT embeddings</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='section-header'>Evaluation Metric: Precision@5</div>",
                unsafe_allow_html=True)
    st.markdown("""
    <div class='info-box'>
        <div style='color:#e2e8f0; font-size:0.92rem; line-height:1.8;'>
            <b style='color:#63b3ed;'>Precision@5</b> measures how many of the top 5
            recommended jobs are actually relevant to the resume's career field.<br><br>
            <b style='color:#63b3ed;'>Formula:</b>
            Precision@5 = Relevant jobs in top 5 ÷ 5<br><br>
            <b style='color:#48bb78;'>BERT Result: 70.5%</b> — meaning on average,
            3–4 out of every 5 recommended jobs are genuinely relevant.<br>
            <span style='color:#718096;'>BM25 baseline: 69.5% (BERT wins by 1 point)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
