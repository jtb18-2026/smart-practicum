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
    text-shadow: 0 2px 16px rgba(0,0,0,0.7);
    display: block;
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
.badge-salary-none { background: #f8fafc; color: #9ca3af; border: 1px solid #e5e7eb; }
.missing-tag {
    display: inline-block;
    background: #fef2f2;
    color: #991b1b;
    border: 1px solid #fecaca;
    border-radius: 5px;
    padding: 0.18rem 0.65rem;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 0.15rem 0.15rem 0.15rem 0;
    font-family: 'Inter', sans-serif;
}
.gap-analysis-box {
    background: #fff7ed;
    border: 1px solid #fed7aa;
    border-left: 4px solid #ea580c;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    margin-top: 1.5rem;
}
@media (max-width: 768px) {
    .block-container { padding: 1rem !important; }
    .hero-banner { padding: 1.2rem 1.4rem; }
    .hero-title { font-size: 1.6rem !important; }
    .match-card { padding: 1rem 1.2rem; }
    .stButton > button { padding: 0.6rem 1rem !important; font-size: 0.9rem !important; }
}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────
# Expanded skill database — 300+ skills across many domains
HARD_SKILLS_DB = sorted(set([
    # Programming languages
    'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c',
    'r', 'scala', 'kotlin', 'swift', 'go', 'rust', 'php', 'ruby',
    'matlab', 'bash', 'shell', 'perl', 'vba', 'dart', 'lua', 'objective-c',
    # Web frameworks
    'html', 'css', 'sass', 'less', 'tailwind', 'bootstrap', 'material-ui',
    'react', 'angular', 'vue', 'svelte', 'next.js', 'nuxt', 'gatsby',
    'node.js', 'nodejs', 'deno',
    'django', 'flask', 'fastapi', 'spring', 'spring boot', 'express', 'jquery',
    'rails', 'laravel', '.net', 'asp.net',
    'rest api', 'graphql', 'grpc', 'soap', 'websocket', 'oauth', 'jwt',
    # Mobile
    'react native', 'flutter', 'ionic', 'xamarin', 'android', 'ios',
    # Databases
    'sql', 'mysql', 'postgresql', 'sqlite', 'oracle', 'sql server', 'mariadb',
    'nosql', 'mongodb', 'redis', 'cassandra', 'elasticsearch', 'dynamodb',
    'neo4j', 'firebase', 'supabase', 'cosmos db',
    # Data science / ML
    'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'plotly', 'bokeh',
    'tableau', 'power bi', 'excel', 'google sheets', 'looker', 'qlik', 'metabase',
    'power query', 'dax', 'pivot tables',
    'machine learning', 'deep learning', 'neural networks',
    'nlp', 'natural language processing', 'computer vision', 'object detection',
    'image segmentation', 'opencv',
    'scikit-learn', 'tensorflow', 'keras', 'pytorch', 'jax',
    'hugging face', 'transformers', 'bert', 'gpt', 'llm', 'large language model',
    'generative ai', 'fine-tuning', 'prompt engineering', 'rag',
    'xgboost', 'lightgbm', 'catboost',
    'random forest', 'regression', 'classification', 'clustering',
    'reinforcement learning', 'time series', 'forecasting',
    'a/b testing', 'experimentation', 'causal inference', 'feature engineering',
    'cnn', 'rnn', 'lstm', 'gan', 'transformer',
    'recommendation systems', 'data wrangling', 'data cleaning',
    # Cloud / DevOps
    'aws', 'azure', 'gcp', 'google cloud', 'oracle cloud', 'ibm cloud',
    'docker', 'kubernetes', 'helm', 'terraform', 'ansible', 'puppet', 'chef',
    'ci/cd', 'jenkins', 'circleci', 'travis ci', 'github actions', 'gitlab ci',
    'git', 'github', 'gitlab', 'bitbucket', 'svn',
    'linux', 'unix', 'ubuntu', 'centos', 'redhat',
    'devops', 'mlops', 'sre', 'site reliability',
    'prometheus', 'grafana', 'datadog', 'splunk', 'new relic', 'cloudwatch',
    # Big data
    'spark', 'pyspark', 'hadoop', 'hive', 'pig', 'kafka', 'rabbitmq',
    'airflow', 'prefect', 'dagster', 'dbt',
    'snowflake', 'databricks', 'bigquery', 'redshift', 'synapse',
    'etl', 'elt', 'data pipeline', 'data warehouse', 'data lake',
    # Security
    'cybersecurity', 'penetration testing', 'pen testing', 'network security',
    'firewalls', 'encryption', 'siem', 'soc',
    'iso 27001', 'nist', 'gdpr', 'hipaa', 'pci dss',
    'ethical hacking', 'vulnerability assessment',
    # Project management / Methodology
    'agile', 'scrum', 'kanban', 'waterfall', 'lean', 'six sigma',
    'pmp', 'prince2', 'safe', 'jira', 'confluence', 'asana',
    'trello', 'notion', 'monday.com', 'clickup', 'basecamp', 'smartsheet',
    'gantt charts', 'risk management',
    # Design / Creative
    'figma', 'sketch', 'adobe xd', 'invision', 'canva',
    'photoshop', 'illustrator', 'indesign', 'lightroom',
    'after effects', 'premiere pro', 'final cut', 'davinci resolve',
    'blender', 'maya', '3ds max', 'cinema 4d',
    'ui design', 'ux design', 'wireframing', 'prototyping',
    # Engineering / CAD
    'autocad', 'solidworks', 'revit', 'sketchup', 'fusion 360',
    'inventor', 'rhino', 'ansys', 'comsol', 'abaqus', 'catia',
    'simulink', 'labview', 'plc', 'scada',
    # Office / Business tools
    'microsoft office', 'word', 'powerpoint', 'outlook', 'sharepoint',
    'teams', 'slack', 'zoom', 'webex',
    'sap', 'oracle erp', 'workday', 'netsuite', 'quickbooks',
    'salesforce', 'hubspot', 'zoho', 'dynamics 365', 'pipedrive',
    # Healthcare
    'epic', 'cerner', 'meditech', 'allscripts', 'ehr', 'emr',
    'cpr', 'bls', 'acls', 'pals', 'icd-10', 'cpt', 'phlebotomy',
    'pharmacology', 'medical coding', 'medical billing', 'clinical research',
    # Finance / Accounting
    'gaap', 'ifrs', 'sox', 'sarbanes-oxley', 'audit', 'taxation',
    'bloomberg terminal', 'reuters', 'factset', 'capital iq',
    'financial modeling', 'dcf', 'lbo', 'm&a', 'venture capital',
    'fp&a', 'budgeting', 'forecasting', 'variance analysis',
    'accounts payable', 'accounts receivable', 'general ledger', 'reconciliation',
    # Marketing / Sales
    'seo', 'sem', 'google ads', 'facebook ads', 'linkedin ads', 'tiktok ads',
    'google analytics', 'google tag manager', 'mailchimp', 'sendgrid',
    'hootsuite', 'buffer', 'sprout social',
    'wordpress', 'shopify', 'squarespace', 'webflow', 'wix',
    'content marketing', 'email marketing', 'social media marketing',
    'crm', 'lead generation', 'cold calling', 'account management',
    # Statistics / Research
    'sas', 'spss', 'stata', 'eviews', 'jmp',
    'hypothesis testing', 'regression analysis', 'survey design',
    # Languages / Misc
    'api', 'microservices', 'object-oriented', 'functional programming',
    'design patterns', 'data structures', 'algorithms',
    'unit testing', 'integration testing', 'tdd', 'bdd',
    'selenium', 'cypress', 'playwright', 'pytest', 'junit', 'jest',
    'webpack', 'vite', 'babel', 'rollup',
    # Game dev
    'unity', 'unreal engine', 'godot', 'three.js', 'webgl',
    # Construction / trades
    'osha', 'blueprint reading', 'project estimation', 'cost analysis',
]), key=len, reverse=True)

# Skill weights — high-demand technical skills count more
SKILL_WEIGHTS = {
    # Top-tier (1.5x)
    'python': 1.5, 'sql': 1.5, 'machine learning': 1.5, 'deep learning': 1.5,
    'tensorflow': 1.5, 'pytorch': 1.5, 'aws': 1.5, 'kubernetes': 1.5,
    'spark': 1.5, 'snowflake': 1.5, 'databricks': 1.5, 'docker': 1.5,
    'react': 1.5, 'typescript': 1.5, 'go': 1.5, 'rust': 1.5,
    'llm': 1.5, 'transformers': 1.5, 'generative ai': 1.5, 'mlops': 1.5,
    'cybersecurity': 1.5, 'kafka': 1.5, 'airflow': 1.5,
    # Strong (1.2x)
    'java': 1.2, 'c++': 1.2, 'scala': 1.2, 'r': 1.2, 'azure': 1.2,
    'gcp': 1.2, 'terraform': 1.2, 'pandas': 1.2, 'numpy': 1.2,
    'scikit-learn': 1.2, 'nlp': 1.2, 'computer vision': 1.2,
    'graphql': 1.2, 'redis': 1.2, 'mongodb': 1.2, 'postgresql': 1.2,
    'angular': 1.2, 'vue': 1.2, 'next.js': 1.2, 'node.js': 1.2,
    # Standard (1.0x) — everything else defaults here
    # Basic / less differentiated (0.7x)
    'excel': 0.7, 'word': 0.7, 'powerpoint': 0.7, 'outlook': 0.7,
    'microsoft office': 0.7, 'google sheets': 0.7, 'html': 0.7, 'css': 0.7,
}

def skill_weight(s):
    return SKILL_WEIGHTS.get(s, 1.0)

# Industry classification — keyword -> industry tag
INDUSTRY_KEYWORDS = {
    'Technology / Software':   ['software', 'engineer', 'developer', 'programmer', 'devops', 'sre', 'full stack', 'frontend', 'backend', 'web ', 'mobile', 'qa ', 'sdet', 'cloud', 'platform'],
    'AI / Machine Learning':   ['machine learning', 'ml ', 'deep learning', 'data scientist', 'data science', 'ai ', 'artificial intelligence', 'mlops', 'nlp ', 'computer vision', 'research scientist'],
    'Data / Analytics':        ['data analyst', 'data engineer', 'analytics', 'business intelligence', 'bi ', 'reporting', 'tableau', 'power bi', 'database', 'etl'],
    'Finance / Banking':       ['finance', 'financial', 'bank', 'investment', 'credit', 'loan', 'mortgage', 'audit', 'tax', 'cfo', 'controller', 'treasurer', 'risk', 'actuary', 'underwrit'],
    'Accounting':              ['accountant', 'bookkeeper', 'accounts payable', 'accounts receivable', 'payroll'],
    'Healthcare / Medical':    ['nurse', 'rn ', 'lpn', 'physician', 'doctor', 'medical', 'clinical', 'pharmacy', 'pharmacist', 'health', 'patient', 'therapist', 'physical therapy', 'dental', 'dentist', 'radiolog', 'surgeon'],
    'Education / Teaching':    ['teacher', 'professor', 'tutor', 'instructor', 'lecturer', 'school', 'education', 'curriculum', 'principal', 'academic'],
    'Sales / Business Dev':    ['sales', 'account executive', 'business development', 'territory', 'inside sales', 'outside sales', 'bd '],
    'Marketing / Advertising': ['marketing', 'brand', 'seo', 'sem', 'social media', 'content', 'copywriter', 'public relations', 'pr ', 'advertising', 'demand gen', 'growth'],
    'Real Estate':             ['real estate', 'realtor', 'property manager', 'leasing', 'broker', 'appraiser'],
    'Construction / Trades':   ['construction', 'electrician', 'plumber', 'carpenter', 'welder', 'mechanic', 'hvac', 'foreman', 'mason', 'roofer'],
    'Engineering (Non-SW)':    ['mechanical engineer', 'electrical engineer', 'civil engineer', 'chemical engineer', 'industrial engineer', 'aerospace', 'manufacturing engineer', 'process engineer'],
    'Legal':                   ['attorney', 'lawyer', 'paralegal', 'legal counsel', 'compliance', 'contracts', 'litigation'],
    'HR / People Ops':         ['human resources', 'hr ', 'recruiter', 'talent acquisition', 'people operations', 'compensation', 'benefits'],
    'Operations / Supply':     ['operations', 'supply chain', 'logistics', 'warehouse', 'procurement', 'fulfillment', 'inventory', 'shipping'],
    'Customer Service':        ['customer service', 'customer support', 'call center', 'help desk', 'service desk', 'client success', 'customer success'],
    'Hospitality / Food':      ['chef', 'cook', 'server', 'bartender', 'restaurant', 'hotel', 'hospitality', 'barista', 'kitchen', 'food service'],
    'Arts / Design / Media':   ['designer', 'graphic design', 'ux ', 'ui ', 'creative', 'artist', 'animator', 'illustrator', 'photographer', 'editor', 'producer', 'video', 'music'],
    'Manufacturing':           ['production', 'assembly', 'machinist', 'operator', 'quality control', 'qc ', 'plant', 'factory'],
    'Transportation':          ['driver', 'pilot', 'dispatcher', 'fleet', 'truck', 'delivery'],
    'Government / Nonprofit':  ['government', 'public sector', 'nonprofit', 'social work', 'policy'],
    'Project / Program Mgmt':  ['project manager', 'program manager', 'product manager', 'scrum master', 'product owner'],
    'Cybersecurity':           ['security analyst', 'security engineer', 'cybersecurity', 'soc analyst', 'penetration test', 'infosec'],
}

def classify_industry(title):
    """Return list of industry tags that match this job title."""
    if not isinstance(title, str):
        return []
    t = title.lower()
    tags = []
    for industry, keywords in INDUSTRY_KEYWORDS.items():
        if any(kw in t for kw in keywords):
            tags.append(industry)
    return tags

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

def weighted_skill_score(resume_skills, job_skills):
    """Weighted overlap: top-tier skills (Python, AWS, ML, etc.) count more
    than basic ones (Excel, Word). Returns a score in [0, 1+]."""
    if not job_skills:
        return 0.0
    matched_weight = sum(skill_weight(s) for s in (resume_skills & job_skills))
    total_weight   = sum(skill_weight(s) for s in job_skills)
    return matched_weight / total_weight if total_weight > 0 else 0.0

# Common stop-words to ignore when extracting title keywords from a resume
_TITLE_STOP = {'the','a','an','and','or','of','for','in','to','at','on','with',
               'is','was','are','were','my','your','our','their','i','we','you',
               'experience','years','year','work','working','workplace'}

def extract_resume_title_keywords(text, top_n=15):
    """Pull likely job-title keywords from the resume (frequent meaningful
    words). Used for the title relevance signal."""
    if not isinstance(text, str):
        return set()
    words = re.findall(r'[a-z]{3,}', text.lower())
    words = [w for w in words if w not in _TITLE_STOP]
    return set(w for w, _ in Counter(words).most_common(top_n))

def title_relevance_score(resume_kw, job_title):
    """Fraction of job-title words that appear as resume keywords."""
    if not isinstance(job_title, str) or not job_title.strip():
        return 0.0
    title_words = set(re.findall(r'[a-z]{3,}', job_title.lower()))
    title_words = title_words - _TITLE_STOP
    if not title_words:
        return 0.0
    return len(title_words & resume_kw) / len(title_words)

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
    sal = float(sal)
    # normalized_salary is always the annualized equivalent in this dataset.
    # Convert back to the appropriate unit based on pay_period.
    if period == 'HOURLY':
        hourly = sal / 2080          # 52 weeks × 40 hrs
        return f"${hourly:,.0f}/hr"
    elif period == 'MONTHLY':
        monthly = sal / 12
        return f"${monthly:,.0f}/mo"
    else:                            # YEARLY, blank, or anything else
        return f"${int(sal):,}/yr"

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

# ── Session state ──────────────────────────────────────────────────────────
if 'hidden_jobs' not in st.session_state:
    st.session_state.hidden_jobs = set()
if 'match_results' not in st.session_state:
    st.session_state.match_results = None
if 'custom_jobs' not in st.session_state:
    st.session_state.custom_jobs = []          # list of dicts user added
if 'compare_selected' not in st.session_state:
    st.session_state.compare_selected = []     # list of j_idx selected for compare

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
        <div style='color:#374151; font-size:0.82rem; line-height:1.7;'>
            🤖 all-MiniLM-L6-v2<br>
            ⚖️ 30% Skills · 10% Title<br>
            &nbsp;&nbsp;&nbsp;&nbsp;20% Edu · 20% Exp<br>
            &nbsp;&nbsp;&nbsp;&nbsp;20% Semantic (BERT)
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Hero Banner ────────────────────────────────────────────────────────────
st.markdown("""
<div class='hero-banner'>
    <p class='hero-sub'>DATA-496 · Capstone Project</p>
    <div class='hero-title'>Smart Practicum</div>
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
            st.markdown("""
            <div style='background:#fef2f2; border:1px solid #fecaca; border-left:4px solid #dc2626;
                        border-radius:8px; padding:0.7rem 1rem; margin-bottom:0.8rem; font-size:0.85rem;
                        color:#7f1d1d; line-height:1.55;'>
                <b>⚠️ Supported file types:</b><br>
                ✅ Text-based PDF resumes only (exported from Word, Google Docs, Pages, etc.)<br>
                ❌ Scanned / image-based PDFs (won't extract text)<br>
                ❌ Word (.docx), images (.png/.jpg), or other formats<br>
                <span style='color:#9f1239; font-size:0.78rem;'>
                Tip: if your PDF was made by scanning paper, paste the text instead.</span>
            </div>
            """, unsafe_allow_html=True)
            uploaded = st.file_uploader("Upload your resume PDF", type=["pdf"])
            if uploaded:
                try:
                    import pdfplumber
                    with pdfplumber.open(uploaded) as pdf:
                        resume_text = "\n".join(p.extract_text() or "" for p in pdf.pages)
                    st.success(f"✅ PDF loaded — {len(resume_text):,} characters extracted")
                    if len(resume_text.strip()) < 200:
                        st.warning("⚠️ Very little text was extracted. This may be a scanned (image-based) PDF — the app can't read image PDFs. Try copying and pasting your resume text directly instead.")
                        resume_text = ""
                except ImportError:
                    st.error("pdfplumber not installed.")
                except Exception as e:
                    st.error(f"Could not read PDF: {e}")

        top_k = st.slider("Number of job matches to show", 3, 15, 5)

        # ── Filters ───────────────────────────────────────────────────────
        with st.expander("🔧 Filters & Search", expanded=False):
            st.markdown("**Filter the job database before matching:**")

            title_search = st.text_input(
                "🔍 Search title or company",
                placeholder="e.g. Data Scientist, Google, Meta, Software Engineer",
                help="Searches across both job titles and company names"
            )
            loc_search = st.text_input("📍 Location (city or state)", placeholder="e.g. Los Angeles, CA or New York")

            industry_filter = st.multiselect(
                "🏢 Industry / Department",
                list(INDUSTRY_KEYWORDS.keys()),
                default=[],
                help="Filter to jobs only in these industries (based on title)"
            )

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
            sort_by = st.selectbox("📊 Sort results by", ["Match Score", "Salary (highest first)"])

        # ── Add your own job ──────────────────────────────────────────────
        with st.expander("➕ Add Your Own Job (mix in jobs not in our database)", expanded=False):
            st.caption("Add a job listing you found elsewhere — it will be scored alongside the 124k jobs.")
            with st.form("custom_job_form", clear_on_submit=True):
                cj_title = st.text_input("Job Title*", placeholder="e.g. Data Analyst")
                cj_company = st.text_input("Company", placeholder="e.g. Airbnb")
                cj_desc = st.text_area("Job Description*", height=130,
                    placeholder="Paste the full job description here — required skills, responsibilities, etc.")
                cj_loc = st.text_input("Location", placeholder="e.g. Remote, San Francisco")
                cj_url = st.text_input("Job URL", placeholder="https://...")
                cj_sal = st.number_input("Yearly Salary (optional)", min_value=0, value=0, step=5000)
                cj_remote = st.checkbox("Remote")
                cj_submit = st.form_submit_button("➕ Add Job")
                if cj_submit:
                    if cj_title.strip() and cj_desc.strip():
                        try:
                            model_for_emb = load_model()
                            cj_clean = clean_text(cj_desc)
                            cj_vec = model_for_emb.encode(
                                [cj_clean[:1000]], normalize_embeddings=True,
                                show_progress_bar=False
                            )[0].astype(np.float32)
                            st.session_state.custom_jobs.append({
                                'title': cj_title.strip(),
                                'company_name': cj_company.strip() or 'Custom',
                                'description': cj_desc.strip(),
                                'location': cj_loc.strip(),
                                'job_posting_url': cj_url.strip() or '',
                                'normalized_salary': float(cj_sal) if cj_sal > 0 else None,
                                'pay_period': 'YEARLY',
                                'formatted_work_type': '',
                                'formatted_experience_level': '',
                                'remote_allowed': 1 if cj_remote else 0,
                                'edu_required': 0,
                                'exp_required': 'unknown',
                                'required_skills': extract_hard_skills(cj_clean),
                                'embedding': cj_vec,
                                'is_custom': True,
                            })
                            st.success(f"✅ Added: {cj_title}")
                        except Exception as e:
                            st.error(f"Could not encode job: {e}")
                    else:
                        st.warning("Title and Description are required.")
            if st.session_state.custom_jobs:
                st.markdown(f"**{len(st.session_state.custom_jobs)} custom jobs added:**")
                for i, cj in enumerate(st.session_state.custom_jobs):
                    cc1, cc2 = st.columns([5, 1])
                    cc1.markdown(f"• **{cj['title']}** — {cj['company_name']}")
                    if cc2.button("✕", key=f"rm_cj_{i}"):
                        st.session_state.custom_jobs.pop(i)
                        st.rerun()

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

        # ── Compute matches when button clicked ────────────────────────────
        if run_btn and resume_text.strip():
            st.session_state.hidden_jobs      = set()
            st.session_state.compare_selected = []
            try:
                jobs_df, job_embeddings, _ = load_all_data()
                model = load_model()
            except Exception as e:
                st.error(f"Failed to load data: {e}\n\nPlease refresh the page and try again.")
                st.stop()

            prog = st.progress(0, text="🔍 Applying filters to 124,000+ jobs...")

            clean  = clean_text(resume_text)
            skills = extract_hard_skills(clean)
            edu    = detect_education_level(clean)
            exp    = detect_experience_level(clean)
            resume_kw = extract_resume_title_keywords(clean)

            # ── Apply filters ──────────────────────────────────────────────
            mask = np.ones(len(jobs_df), dtype=bool)
            if title_search.strip():
                # Search BOTH title and company
                ts = title_search.strip().lower()
                title_mask   = jobs_df['title'].fillna('').str.lower().str.contains(ts, regex=False).values
                company_mask = jobs_df.get('company_name', pd.Series([''] * len(jobs_df))).fillna('').astype(str).str.lower().str.contains(ts, regex=False).values
                mask &= (title_mask | company_mask)
            if loc_search.strip():
                mask &= jobs_df['location'].fillna('').str.lower().str.contains(
                    loc_search.strip().lower(), regex=False).values
            if industry_filter:
                # Build mask: keep job if any of its industry tags is in the user's filter
                ind_mask = jobs_df['title'].fillna('').apply(
                    lambda t: bool(set(classify_industry(t)) & set(industry_filter))
                ).values
                mask &= ind_mask
            if work_types:
                mask &= jobs_df['formatted_work_type'].fillna('').isin(work_types).values
            if exp_levels:
                mask &= jobs_df['formatted_experience_level'].fillna('').isin(exp_levels).values
            if max_edu != "Any":
                mask &= (jobs_df['edu_required'].fillna(0) <= edu_options[max_edu]).values
            if remote_only:
                mask &= (jobs_df['remote_allowed'].fillna(0) == 1).values
            if salary_filter:
                mask &= (jobs_df['normalized_salary'].notna() & (jobs_df['normalized_salary'] > 0)).values

            filtered_df   = jobs_df[mask].reset_index(drop=True)
            filtered_embs = job_embeddings[mask]

            # ── Merge in custom jobs (if any) ─────────────────────────────
            if st.session_state.custom_jobs:
                custom_rows  = []
                custom_embs  = []
                for cj in st.session_state.custom_jobs:
                    custom_rows.append({
                        'title': cj['title'],
                        'company_name': cj['company_name'],
                        'location': cj['location'],
                        'job_posting_url': cj['job_posting_url'],
                        'normalized_salary': cj['normalized_salary'],
                        'pay_period': cj['pay_period'],
                        'formatted_work_type': cj['formatted_work_type'],
                        'formatted_experience_level': cj['formatted_experience_level'],
                        'remote_allowed': cj['remote_allowed'],
                        'edu_required': cj['edu_required'],
                        'exp_required': cj['exp_required'],
                        'required_skills': cj['required_skills'],
                        'is_custom': True,
                    })
                    custom_embs.append(cj['embedding'])
                custom_df  = pd.DataFrame(custom_rows)
                if 'is_custom' not in filtered_df.columns:
                    filtered_df['is_custom'] = False
                filtered_df   = pd.concat([custom_df, filtered_df], ignore_index=True)
                filtered_embs = np.vstack([np.array(custom_embs), filtered_embs])
            else:
                filtered_df['is_custom'] = False

            if len(filtered_df) == 0:
                prog.empty()
                st.warning("No jobs match your filters. Try relaxing some filter options.")
                st.stop()

            prog.progress(25, text=f"🤖 Encoding resume with BERT ({len(filtered_df):,} jobs to score)...")

            resume_vec = model.encode(
                [clean[:1000]], normalize_embeddings=True, show_progress_bar=False
            )[0].astype(np.float32)

            prog.progress(55, text="⚡ Computing match scores (5 signals)...")

            # ── Scoring ────────────────────────────────────────────────────
            r_skills    = set(skills)
            job_edu     = filtered_df['edu_required'].values.astype(np.float32)
            level_map   = {'entry':1,'mid':2,'senior':3,'unknown':0}
            job_exp_num = np.array([level_map.get(str(e).lower().split('-')[0].strip(), 0)
                                    for e in filtered_df['exp_required'].tolist()], dtype=np.float32)

            cos_scores = (filtered_embs @ resume_vec).astype(np.float32)

            job_skill_sets = [set(s) if isinstance(s, list) else set()
                              for s in filtered_df['required_skills']]

            # Weighted skill score — Python > Excel
            skill_scores = np.array([
                weighted_skill_score(r_skills, js)
                for js in job_skill_sets
            ], dtype=np.float32)

            # Title relevance score — does resume's vocabulary appear in the job title?
            title_scores = np.array([
                title_relevance_score(resume_kw, t)
                for t in filtered_df['title'].fillna('').tolist()
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

            # NEW formula: 30% skill + 10% title + 20% edu + 20% exp + 20% semantic
            final_scores = (skill_scores * 0.30 + title_scores * 0.10 +
                            edu_scores   * 0.20 + exp_scores   * 0.20 +
                            cos_scores   * 0.20)

            prog.progress(85, text="🏆 Ranking results...")

            min_score  = min_score_pct / 100.0
            score_mask = final_scores >= min_score
            if score_mask.sum() == 0:
                prog.empty()
                st.warning(f"No jobs scored above {min_score_pct}%. Try lowering the minimum score.")
                st.stop()

            n_candidates    = min(max(top_k * 8, 50), int(score_mask.sum()))
            eligible_scores = np.where(score_mask, final_scores, -1)
            candidate_idx   = np.argpartition(eligible_scores, -n_candidates)[-n_candidates:]
            candidate_idx   = candidate_idx[np.argsort(eligible_scores[candidate_idx])[::-1]]

            prog.progress(100, text="✅ Done!")
            prog.empty()

            st.session_state.match_results = {
                'filtered_df':    filtered_df,
                'candidate_idx':  candidate_idx.tolist(),
                'skill_scores':   skill_scores,
                'title_scores':   title_scores,
                'edu_scores':     edu_scores,
                'exp_scores':     exp_scores,
                'cos_scores':     cos_scores,
                'final_scores':   final_scores,
                'job_skill_sets': job_skill_sets,
                'r_skills':       r_skills,
            }

        # ── Render results from session state ─────────────────────────────
        if st.session_state.match_results is not None:
            res            = st.session_state.match_results
            filtered_df    = res['filtered_df']
            candidate_idx  = res['candidate_idx']
            skill_scores   = res['skill_scores']
            title_scores   = res.get('title_scores', np.zeros(len(filtered_df), dtype=np.float32))
            edu_scores     = res['edu_scores']
            exp_scores     = res['exp_scores']
            cos_scores     = res['cos_scores']
            final_scores   = res['final_scores']
            job_skill_sets = res['job_skill_sets']
            r_skills       = res['r_skills']

            # Filter hidden, apply sort, take top_k
            visible = [i for i in candidate_idx if i not in st.session_state.hidden_jobs]
            if sort_by == "Salary (highest first)":
                visible = sorted(visible,
                    key=lambda i: float(filtered_df.iloc[i].get('normalized_salary') or 0),
                    reverse=True)
            display_idx = visible[:top_k]

            hidden_count = len(st.session_state.hidden_jobs)
            suffix = f" · {hidden_count} hidden" if hidden_count else ""
            st.caption(f"Showing {len(display_idx)} matches from {len(filtered_df):,} jobs{suffix}")

            all_missing_skills = []

            for rank, j_idx in enumerate(display_idx, start=1):
                job_row = filtered_df.iloc[j_idx]
                score   = float(final_scores[j_idx])
                matched = sorted(r_skills & job_skill_sets[j_idx])
                missing = sorted(job_skill_sets[j_idx] - r_skills)[:5]
                all_missing_skills.extend(job_skill_sets[j_idx] - r_skills)
                color   = score_color(score)
                label   = score_label(score)
                pct     = int(score * 100)
                is_custom = bool(job_row.get('is_custom', False))

                work_type  = job_row.get('formatted_work_type', '')
                is_remote  = job_row.get('remote_allowed', 0) == 1
                salary_str = fmt_salary(job_row)
                job_url    = job_row.get('job_posting_url', '')

                badges = ""
                if is_custom:
                    badges += "<span class='badge' style='background:#ede9fe; color:#5b21b6; border:1px solid #c4b5fd;'>⭐ Your Job</span>"
                if work_type and str(work_type) != 'nan':
                    badges += f"<span class='badge badge-work'>{work_type}</span>"
                if is_remote:
                    badges += "<span class='badge badge-remote'>🏠 Remote</span>"
                if salary_str:
                    badges += f"<span class='badge badge-salary'>💰 {salary_str}</span>"
                else:
                    badges += "<span class='badge badge-salary-none'>Salary not listed</span>"

                matched_html = "".join(f"<span class='skill-tag'>✓ {s}</span>" for s in matched)
                missing_html = "".join(f"<span class='missing-tag'>✗ {s}</span>" for s in missing)

                # Why score is low
                insight = ""
                if score < 0.75:
                    weak = []
                    if skill_scores[j_idx] < 0.3:  weak.append("few matching skills")
                    if title_scores[j_idx] < 0.2:  weak.append("title doesn't match your background")
                    if edu_scores[j_idx]   < 0.5:  weak.append("education below requirement")
                    if exp_scores[j_idx]   < 0.5:  weak.append("experience level mismatch")
                    if cos_scores[j_idx]   < 0.25: weak.append("low semantic similarity")
                    if weak:
                        insight = f"<div style='color:#92400e; background:#fffbeb; border:1px solid #fde68a; border-radius:7px; padding:0.4rem 0.8rem; font-size:0.8rem; margin-top:0.5rem;'>💡 Score held back by: {', '.join(weak)}</div>"

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
                        <div style='font-family:Plus Jakarta Sans,sans-serif; font-weight:700;
                                    color:{color}; font-size:1.3rem; min-width:50px;'>{pct}%</div>
                    </div>
                    <div style='display:grid; grid-template-columns:repeat(4,1fr); gap:0.4rem; margin:0.8rem 0;'>
                        <div style='background:#f0f4f8; border:1px solid #dde3ea; border-radius:8px; padding:0.5rem; text-align:center;'>
                            <div style='color:#047857; font-size:1rem; font-weight:700; font-family:Plus Jakarta Sans,sans-serif;'>{int(skill_scores[j_idx]*100)}%</div>
                            <div style='color:#6b7280; font-size:0.7rem; text-transform:uppercase; font-weight:600; margin-top:0.1rem;'>Skills</div>
                        </div>
                        <div style='background:#f0f4f8; border:1px solid #dde3ea; border-radius:8px; padding:0.5rem; text-align:center;'>
                            <div style='color:#7c3aed; font-size:1rem; font-weight:700; font-family:Plus Jakarta Sans,sans-serif;'>{int(title_scores[j_idx]*100)}%</div>
                            <div style='color:#6b7280; font-size:0.7rem; text-transform:uppercase; font-weight:600; margin-top:0.1rem;'>Title</div>
                        </div>
                        <div style='background:#f0f4f8; border:1px solid #dde3ea; border-radius:8px; padding:0.5rem; text-align:center;'>
                            <div style='color:#0284c7; font-size:1rem; font-weight:700; font-family:Plus Jakarta Sans,sans-serif;'>{int(edu_scores[j_idx]*100)}%</div>
                            <div style='color:#6b7280; font-size:0.7rem; text-transform:uppercase; font-weight:600; margin-top:0.1rem;'>Education</div>
                        </div>
                        <div style='background:#f0f4f8; border:1px solid #dde3ea; border-radius:8px; padding:0.5rem; text-align:center;'>
                            <div style='color:#1a56db; font-size:1rem; font-weight:700; font-family:Plus Jakarta Sans,sans-serif;'>{int(cos_scores[j_idx]*100)}%</div>
                            <div style='color:#6b7280; font-size:0.7rem; text-transform:uppercase; font-weight:600; margin-top:0.1rem;'>Semantic</div>
                        </div>
                    </div>
                    {"<div style='margin:0.3rem 0 0.1rem 0; font-size:0.75rem; color:#6b7280; font-weight:600; text-transform:uppercase; letter-spacing:0.06em;'>Matched Skills</div><div style='margin-bottom:0.3rem;'>" + matched_html + "</div>" if matched else "<div style='color:#94a3b8; font-size:0.85rem; margin-bottom:0.3rem;'>No skill overlap detected</div>"}
                    {"<div style='margin:0.3rem 0 0.1rem 0; font-size:0.75rem; color:#991b1b; font-weight:600; text-transform:uppercase; letter-spacing:0.06em;'>Skills to Add</div><div style='margin-bottom:0.3rem;'>" + missing_html + "</div>" if missing else ""}
                    {insight}
                </div>
                """, unsafe_allow_html=True)

                # Action buttons (Link / Compare / Hide)
                btn_c1, btn_c2, btn_c3 = st.columns([2.4, 1.2, 1])
                with btn_c1:
                    if job_url and str(job_url) != 'nan':
                        st.link_button("🔗 View Job on LinkedIn", job_url)
                with btn_c2:
                    is_selected = j_idx in st.session_state.compare_selected
                    cmp_label = "✅ In Compare" if is_selected else "⚖️ Compare"
                    if st.button(cmp_label, key=f"cmp_{rank}_{j_idx}",
                                 help="Add to side-by-side comparison"):
                        if is_selected:
                            st.session_state.compare_selected.remove(j_idx)
                        elif len(st.session_state.compare_selected) < 3:
                            st.session_state.compare_selected.append(j_idx)
                        else:
                            st.warning("You can compare up to 3 jobs at once.")
                        st.rerun()
                with btn_c3:
                    if st.button("🚫 Hide", key=f"hide_{rank}_{j_idx}",
                                 help="Not interested — remove from results"):
                        st.session_state.hidden_jobs.add(int(j_idx))
                        st.rerun()

            # ── Download Results as CSV ───────────────────────────────────
            if display_idx:
                rows = []
                for rank, j_idx in enumerate(display_idx, start=1):
                    jr = filtered_df.iloc[j_idx]
                    rows.append({
                        'Rank': rank,
                        'Title': jr.get('title', ''),
                        'Company': jr.get('company_name', ''),
                        'Location': jr.get('location', ''),
                        'Final_Score_%': int(final_scores[j_idx] * 100),
                        'Skills_%':    int(skill_scores[j_idx] * 100),
                        'Title_%':     int(title_scores[j_idx] * 100),
                        'Education_%': int(edu_scores[j_idx] * 100),
                        'Experience_%':int(exp_scores[j_idx] * 100),
                        'Semantic_%':  int(cos_scores[j_idx] * 100),
                        'Matched_Skills': ', '.join(sorted(r_skills & job_skill_sets[j_idx])),
                        'Skills_To_Add':  ', '.join(sorted(job_skill_sets[j_idx] - r_skills)[:8]),
                        'Salary': fmt_salary(jr) or '',
                        'Job_URL': jr.get('job_posting_url', ''),
                    })
                csv_bytes = pd.DataFrame(rows).to_csv(index=False).encode('utf-8')
                st.download_button(
                    "💾 Download These Results as CSV",
                    data=csv_bytes,
                    file_name="smart_practicum_matches.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            # ── Side-by-side Compare ───────────────────────────────────────
            if st.session_state.compare_selected:
                st.markdown("<div class='section-header'>⚖️ Side-by-Side Comparison</div>",
                            unsafe_allow_html=True)
                cmp_idx = st.session_state.compare_selected
                cols = st.columns(len(cmp_idx))
                for col, j_idx in zip(cols, cmp_idx):
                    jr = filtered_df.iloc[j_idx]
                    sc = float(final_scores[j_idx])
                    matched_c = sorted(r_skills & job_skill_sets[j_idx])
                    missing_c = sorted(job_skill_sets[j_idx] - r_skills)[:6]
                    sal_c     = fmt_salary(jr) or 'Not listed'
                    rem_c     = '🏠 Remote' if jr.get('remote_allowed', 0) == 1 else 'On-site'
                    matched_str = ", ".join(matched_c) if matched_c else "—"
                    missing_str = ", ".join(missing_c) if missing_c else "—"
                    col.markdown(f"""
                    <div class='match-card' style='height:100%;'>
                        <div class='match-title' style='font-size:1.1rem;'>{jr.get('title','')}</div>
                        <div class='match-company'>{jr.get('company_name','')}</div>
                        <div style='margin:0.8rem 0; font-family:Plus Jakarta Sans,sans-serif;
                                    color:{score_color(sc)}; font-size:1.6rem; font-weight:800;'>
                            {int(sc*100)}%
                        </div>
                        <div style='font-size:0.85rem; line-height:1.9; color:#374151;'>
                            <b>📍 Location:</b> {jr.get('location','—')}<br>
                            <b>💼 Type:</b> {jr.get('formatted_work_type','—')}<br>
                            <b>🏠 Remote:</b> {rem_c}<br>
                            <b>💰 Salary:</b> {sal_c}<br>
                            <b>🎓 Edu match:</b> {int(edu_scores[j_idx]*100)}%<br>
                            <b>📈 Exp match:</b> {int(exp_scores[j_idx]*100)}%<br>
                            <b>🔧 Skill match:</b> {int(skill_scores[j_idx]*100)}%<br>
                            <b>🤖 Semantic:</b> {int(cos_scores[j_idx]*100)}%
                        </div>
                        <div style='margin-top:0.8rem; font-size:0.8rem;'>
                            <b style='color:#047857;'>✓ Matched:</b> {matched_str}<br>
                            <b style='color:#991b1b;'>✗ Missing:</b> {missing_str}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                if st.button("Clear Comparison", use_container_width=True):
                    st.session_state.compare_selected = []
                    st.rerun()

            # ── Skill Gap Analysis ─────────────────────────────────────────
            if all_missing_skills:
                gap = Counter(all_missing_skills).most_common(8)
                gap_tags = "".join(
                    f"<span style='background:#fef3c7; color:#92400e; border:1px solid #fde68a; "
                    f"border-radius:5px; padding:0.2rem 0.7rem; font-size:0.82rem; font-weight:600; "
                    f"margin:0.2rem; display:inline-block; font-family:Inter,sans-serif;'>"
                    f"✗ {skill} <span style='color:#d97706; font-size:0.75rem;'>×{count}</span></span>"
                    for skill, count in gap
                )
                st.markdown(f"""
                <div class='gap-analysis-box'>
                    <div style='font-family:Plus Jakarta Sans,sans-serif; font-weight:700;
                                color:#92400e; font-size:1rem; margin-bottom:0.4rem;'>
                        📈 Skill Gap — Add these to boost your matches
                    </div>
                    <div style='color:#78350f; font-size:0.82rem; margin-bottom:0.7rem;'>
                        Skills that appear in your top matches but aren't on your resume.
                        The number shows how many of your matches require it.
                    </div>
                    <div>{gap_tags}</div>
                </div>
                """, unsafe_allow_html=True)

        elif st.session_state.match_results is None:
            st.markdown("""
            <div style='text-align:center; padding:4rem 2rem;
                        border:2px dashed #cbd5e1; border-radius:16px; background:#ffffff;'>
                <div style='font-size:3rem; margin-bottom:1rem;'>📄</div>
                <div style='font-family:Plus Jakarta Sans,sans-serif; font-size:1.2rem;
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

    # ── Why Are Some Resumes Scoring Low? ──────────────────────────────
    st.markdown("<div class='section-header'>💡 Why Are Some Resumes Scoring Low?</div>",
                unsafe_allow_html=True)

    avg_score    = top1['Final_Score'].mean()
    weak_count   = int((top1['Final_Score'] < 0.55).sum())
    weak_pct     = weak_count / len(top1) * 100 if len(top1) else 0
    strong_count = int((top1['Final_Score'] >= 0.75).sum())
    n_unique_skills = len(set(s for sl in matches_df['Skills_Matched'] for s in sl))
    avg_skills_matched = matches_df['Skills_Matched'].apply(len).mean()

    # Identify lowest-scoring category
    bottom_cat = ""
    if 'Resume_Category' in top1.columns:
        cat_means = top1.groupby('Resume_Category')['Final_Score'].mean().sort_values()
        if len(cat_means):
            bottom_cat = f"<b>{cat_means.index[0]}</b> resumes scored lowest on average ({cat_means.iloc[0]*100:.0f}%)."

    # Aggregate top missing skills across all resumes (skills required in matches but not in Skills_Matched)
    insight_html = f"""
    <div class='info-box' style='background:#fffbeb; border-left:4px solid #f59e0b;'>
        <div style='font-family:Plus Jakarta Sans,sans-serif; font-weight:700; color:#92400e;
                    font-size:1.05rem; margin-bottom:0.6rem;'>📊 Key Insights</div>
        <div style='color:#451a03; font-size:0.95rem; line-height:1.95;'>
            • <b>{weak_count} resumes ({weak_pct:.0f}%)</b> scored below 55% on their best match — likely
              because their resume had few of the technical skills the system tracks.<br>
            • Average resume matched only <b>{avg_skills_matched:.1f} skills</b> per top job.
              Adding more concrete technical keywords (Python, SQL, AWS, Tableau) significantly improves scoring.<br>
            • <b>{strong_count} resumes</b> achieved Strong Matches (≥75%) — these resumes typically had
              many in-demand skills explicitly listed.<br>
            {f"• {bottom_cat}" if bottom_cat else ""}
        </div>
        <div style='color:#78350f; font-size:0.85rem; margin-top:0.7rem; font-style:italic;'>
            How to score higher: list specific, measurable skills (tools, languages, frameworks)
            rather than soft skills, and align your education / experience claims with the role you target.
        </div>
    </div>
    """
    st.markdown(insight_html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════
# PAGE 3: HOW IT WORKS
# ══════════════════════════════════════════════════════════════════════════
elif page == "ℹ️ How It Works":
    st.markdown("<div class='section-header'>How the Matching Engine Works</div>", unsafe_allow_html=True)

    steps = [
        ("1. Resume Processing", "Your resume is cleaned (HTML removed, lowercased, normalized) then analyzed to extract hard technical skills from a database of 300+ skills, detect your education level (None → PhD), and detect your experience level (Entry / Mid / Senior)."),
        ("2. BERT Embeddings", "The cleaned resume text is encoded using all-MiniLM-L6-v2, a BERT-based sentence transformer. This converts your resume into a 384-dimensional vector that captures the semantic meaning of your experience — not just keywords."),
        ("3. Matching Against 124k+ Jobs", "Your resume vector is compared against pre-computed embeddings for every job posting using cosine similarity. Four additional signals are computed: weighted skill overlap, job-title relevance, education alignment, and experience level match."),
        ("4. Weighted Final Score", "All five signals are combined into one final score:\nFinal Score = 30% Weighted Skill Overlap + 10% Title Relevance + 20% Education + 20% Experience + 20% Cosine Similarity\n\nNote: skills are weighted by demand — Python, ML, AWS count more than Excel or Word."),
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
                <td style='padding:0.8rem 0.6rem; color:#111827; font-weight:500;'>Weighted Skill Overlap</td>
                <td style='padding:0.8rem 0.6rem; text-align:center; color:#047857; font-weight:700; font-size:1.1rem;'>30%</td>
                <td style='padding:0.8rem 0.6rem; color:#374151;'>Skill match weighted by demand (Python &gt; Excel)</td>
            </tr>
            <tr style='border-bottom:1px solid #f0f4f8;'>
                <td style='padding:0.8rem 0.6rem; color:#111827; font-weight:500;'>Title Relevance</td>
                <td style='padding:0.8rem 0.6rem; text-align:center; color:#7c3aed; font-weight:700; font-size:1.1rem;'>10%</td>
                <td style='padding:0.8rem 0.6rem; color:#374151;'>How much the job title overlaps with your resume's vocabulary</td>
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
                <td style='padding:0.8rem 0.6rem; color:#111827; font-weight:500;'>Cosine Similarity (BERT)</td>
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
