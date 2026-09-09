import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import os
import re

st.set_page_config(
    page_title="MPLADS AI Monitoring",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SANCTIONED_FILE = DATA_DIR / "Works Sanctioned (1).csv"
COMPLETED_FILE = DATA_DIR / "Works Completed (1).csv"


def find_column(df, names):
    columns = {str(c).strip().lower(): c for c in df.columns}
    for name in names:
        key = name.strip().lower()
        if key in columns:
            return columns[key]
    for name in names:
        key = name.strip().lower()
        for col in df.columns:
            if key in str(col).strip().lower():
                return col
    return None


def clean_series(series):
    return series.fillna("").astype(str).str.strip()



# ============================================================
# MPLADS AI MONITOR — FINAL UI / NAVIGATION SHELL
# ============================================================

st.markdown(r'''
<style>
[data-testid="stAppViewContainer"] { background:#f6f8fb; }
[data-testid="stHeader"] { background:rgba(255,255,255,.96); border-bottom:1px solid #e7ebf0; }
.block-container { max-width:1400px; padding-top:1.2rem; padding-bottom:3rem; }
.gov-topbar { background:#fff; border:1px solid #e4e8ee; border-radius:16px; padding:18px 22px; margin-top:30px; margin-bottom:8px; overflow:visible; box-shadow:0 4px 16px rgba(20,40,70,.05); }
.gov-brand { display:flex; align-items:center; gap:12px; }
.gov-mark { width:48px; height:48px; border-radius:50%; display:flex; align-items:center; justify-content:center; background:linear-gradient(145deg,#ff9933 0 31%,#fff 31% 67%,#138808 67%); border:1px solid #d7dce3; box-shadow:inset 0 0 0 3px rgba(255,255,255,.75); font-size:21px; color:#102a43; }
.gov-name { font-weight:850; font-size:1.02rem; color:#172b4d; line-height:1.25; display:block; white-space:nowrap; }
.gov-sub { color:#6b778c; font-size:.72rem; margin-top:4px; line-height:1.35; display:block; white-space:nowrap; }
.portal-kicker { color:#526581; font-size:.73rem; font-weight:800; letter-spacing:.08em; text-transform:uppercase; }
.public-nav { margin-top:10px; }
.public-hero { margin-top:18px; border-radius:24px; overflow:hidden; background:linear-gradient(110deg,#092b4c 0%,#123e63 54%,#173f5f 100%); box-shadow:0 18px 45px rgba(15,35,60,.16); }
.public-hero-grid { display:grid; grid-template-columns:1.05fr .95fr; min-height:440px; }
.public-copy { padding:58px 48px; color:#fff; }
.public-title { font-size:3rem; line-height:1.04; font-weight:900; margin-top:10px; letter-spacing:-.03em; }
.public-lead { margin-top:18px; color:rgba(255,255,255,.84); font-size:1rem; line-height:1.7; max-width:650px; }
.public-photo { min-height:440px; background-size:cover; background-position:center; position:relative; }
.public-photo:after { content:""; position:absolute; inset:0; background:linear-gradient(90deg,rgba(9,43,76,.55),rgba(9,43,76,.05)); }
.trust-strip { margin-top:16px; background:#fff; border:1px solid #e4e8ee; border-radius:16px; padding:16px 20px; box-shadow:0 4px 15px rgba(20,40,70,.04); }
.info-card { background:#fff; border:1px solid #e4e8ee; border-radius:18px; padding:22px; min-height:145px; box-shadow:0 4px 15px rgba(20,40,70,.04); }
.info-title { font-weight:850; color:#172b4d; font-size:1rem; }
.info-text { color:#68778d; font-size:.83rem; line-height:1.55; margin-top:7px; }
.login-page { max-width:1050px; margin:32px auto 0; }
.login-page-title { max-width:1050px; margin:26px auto 10px; color:#526581; font-size:.72rem; font-weight:850; letter-spacing:.10em; }
.login-visual { min-height:500px; border-radius:24px; overflow:hidden; background-size:cover; background-position:center; position:relative; box-shadow:0 20px 55px rgba(20,40,70,.14); }
.login-visual:after { content:""; position:absolute; inset:0; background:linear-gradient(145deg,rgba(7,38,67,.20),rgba(7,38,67,.05)); pointer-events:none; }
.login-visual-copy { position:absolute; z-index:2; left:34px; right:34px; bottom:34px; color:#fff; }

.login-card { background:#fff; border:1px solid #e2e7ee; border-radius:24px; overflow:hidden; box-shadow:0 20px 55px rgba(20,40,70,.14); }
.login-grid { display:grid; grid-template-columns:1fr 1fr; min-height:500px; }
.login-photo { background-size:cover; background-position:center; position:relative; }
.login-photo:after { content:""; position:absolute; inset:0; background:linear-gradient(145deg,rgba(7,38,67,.88),rgba(7,38,67,.30)); }
.login-photo-copy { position:absolute; z-index:2; left:34px; right:34px; bottom:34px; color:#fff; }
.login-form { padding:46px 42px; }
[data-testid="stVerticalBlockBorderWrapper"] { border-radius:24px !important; border-color:#e2e7ee !important; box-shadow:0 20px 55px rgba(20,40,70,.10); background:#fff; }

.login-title { font-size:2rem; font-weight:900; color:#172b4d; letter-spacing:-.02em; }
.login-sub { color:#6b778c; font-size:.88rem; line-height:1.55; margin:8px 0 24px; }
.demo-box { margin-top:14px; padding:12px 14px; background:#f7f9fc; border:1px solid #e4e8ee; border-radius:12px; color:#58677d; font-size:.78rem; }
.dashboard-title { font-size:2.15rem; font-weight:900; color:#172b4d; letter-spacing:-.025em; }
.dashboard-sub { color:#6b778c; margin-top:4px; }
.metric-card { background:#fff; border:1px solid #e3e8ef; border-radius:16px; padding:17px 18px; box-shadow:0 4px 15px rgba(20,40,70,.04); }
.metric-label { color:#738198; font-size:.76rem; font-weight:750; text-transform:uppercase; letter-spacing:.04em; }
.metric-value { color:#172b4d; font-size:1.65rem; font-weight:900; margin-top:4px; }
.module-section-title { font-size:1.25rem; font-weight:900; color:#172b4d; margin:28px 0 12px; }
.module-card { background:#fff; border:1px solid #e2e7ee; border-radius:18px; padding:19px; min-height:155px; box-shadow:0 4px 16px rgba(20,40,70,.04); }
.module-icon { font-size:1.35rem; }
.module-title { font-size:1rem; font-weight:850; color:#172b4d; margin-top:7px; }
.module-desc { color:#718096; font-size:.78rem; line-height:1.45; margin:5px 0 12px; min-height:34px; }
.snapshot-card { background:#fff; border:1px solid #e2e7ee; border-radius:18px; padding:18px; box-shadow:0 4px 16px rgba(20,40,70,.04); }
.stButton > button { border-radius:10px !important; font-weight:750 !important; border:1px solid #dce3ec !important; min-height:40px !important; }
.stButton > button[kind="primary"] { background:#0b5cab !important; border-color:#0b5cab !important; color:#fff !important; }
.stButton > button:hover { border-color:#0b5cab !important; }
section[data-testid="stSidebar"] {
  background:
    radial-gradient(circle at 15% 8%, rgba(56,189,248,.20), transparent 24%),
    radial-gradient(circle at 90% 42%, rgba(37,99,235,.18), transparent 28%),
    linear-gradient(165deg,#0b2440 0%,#103b61 48%,#071d35 100%) !important;
  border-right:1px solid rgba(112,176,225,.28);
  box-shadow:8px 0 28px rgba(7,29,53,.12);
  position:relative;
}
section[data-testid="stSidebar"]:before {
  content:"";
  display:block;
  height:4px;
  position:absolute;
  top:0; left:0; right:0;
  background:linear-gradient(90deg,#ff9933 0 33%,#ffffff 33% 66%,#138808 66% 100%);
  opacity:.95;
}
section[data-testid="stSidebar"] * { color:#eef6ff !important; }
section[data-testid="stSidebar"] .stButton { margin:3px 0 !important; }
section[data-testid="stSidebar"] .stButton > button {
  background:rgba(255,255,255,.035) !important;
  border:1px solid transparent !important;
  color:#eef6ff !important;
  text-align:left !important;
  border-radius:12px !important;
  min-height:42px !important;
  padding:8px 12px !important;
  font-weight:650 !important;
  box-shadow:none !important;
  transition:all .18s ease !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
  background:linear-gradient(90deg,rgba(61,160,230,.24),rgba(255,255,255,.07)) !important;
  border-color:rgba(125,201,255,.28) !important;
  transform:translateX(2px);
}
section[data-testid="stSidebar"] .stButton > button:focus {
  border-color:rgba(125,201,255,.45) !important;
  box-shadow:0 0 0 2px rgba(56,189,248,.10) !important;
}
section[data-testid="stSidebar"] hr { border-color:rgba(191,219,254,.14) !important; margin:14px 0 !important; }
section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] { color:#9fb8ce !important; }
.side-brand {
  padding:15px 14px 16px;
  margin:8px 0 8px;
  border:1px solid rgba(165,214,255,.16);
  border-radius:16px;
  background:linear-gradient(135deg,rgba(255,255,255,.09),rgba(255,255,255,.025));
  box-shadow:inset 0 1px 0 rgba(255,255,255,.07), 0 8px 24px rgba(0,0,0,.10);
}
.side-title { font-size:1.02rem; font-weight:900; letter-spacing:-.01em; }
.side-sub { font-size:.7rem; color:#b9cde0 !important; margin-top:5px; }
.side-label {
  color:#8fc1e7 !important;
  font-size:.67rem;
  font-weight:900;
  letter-spacing:.14em;
  margin:16px 8px 7px;
  padding-bottom:5px;
  border-bottom:1px solid rgba(143,193,231,.14);
}

@media (max-width:900px) { .public-hero-grid,.login-grid { grid-template-columns:1fr; } .public-photo { min-height:280px; } .public-title { font-size:2.2rem; } }

/* ===== FINAL POLISH ===== */
html, body, [data-testid="stAppViewContainer"] { overflow-x:hidden !important; }
.block-container { max-width:1500px !important; padding-left:2.2rem !important; padding-right:2.2rem !important; }
.public-hero { margin-top:22px !important; }
.public-hero-grid { grid-template-columns:1.08fr .92fr !important; min-height:500px !important; }
.public-copy { padding:64px 58px !important; }
.public-title { font-size:3.35rem !important; }
.public-photo { min-height:500px !important; }
.trust-strip { padding:17px 20px !important; }
.module-card { min-height:180px !important; display:flex; flex-direction:column; }
.dashboard-title { font-size:clamp(1.55rem,2.5vw,2.15rem) !important; line-height:1.2 !important; font-weight:900 !important; color:#163b60 !important; letter-spacing:-.025em; max-width:100% !important; overflow:visible !important; overflow-wrap:anywhere !important; display:block !important; padding:8px 0 4px !important; margin:0 !important; clip-path:none !important; }
.dashboard-sub { font-size:.98rem !important; color:#66788e !important; margin-top:8px !important; margin-bottom:20px !important; line-height:1.55 !important; max-width:100% !important; white-space:normal !important; overflow:visible !important; }
.ai-engine-card { background:linear-gradient(135deg,#eef6ff,#ffffff); border:1px solid #cfe0f2; border-radius:18px; padding:18px 20px; margin:6px 0 22px; }
.ai-engine-title { color:#0b5cab; font-weight:900; font-size:1rem; }
.ai-engine-text { color:#5f7187; font-size:.84rem; line-height:1.5; margin-top:4px; }
.section-note { color:#6d7d90; font-size:.82rem; margin:-5px 0 12px; }
.info-card { min-height:150px; }
@media (max-width:1100px) { .public-hero-grid { grid-template-columns:1fr !important; } .public-photo { min-height:320px !important; } .public-copy { padding:44px 34px !important; } .public-title { font-size:2.5rem !important; } }
@media (max-width:1200px) {
  .block-container { padding-left:1.35rem !important; padding-right:1.35rem !important; }
  .dashboard-title { font-size:1.85rem !important; }
}
@media (max-width:850px) {
  .dashboard-title { font-size:1.55rem !important; }
  .dashboard-sub { font-size:.9rem !important; }
  .gov-name, .gov-sub { white-space:normal !important; }
}

/* ===== FULL-WIDTH PUBLIC LAYOUT ===== */
/* Streamlit can keep an inner main wrapper at a fixed max-width. Remove that constraint
   so the public portal uses the full browser width instead of leaving a large blank strip. */
[data-testid="stMain"] > div,
[data-testid="stMainBlockContainer"],
section.main > div,
section[data-testid="stMain"] .block-container {
  width:100% !important;
  max-width:none !important;
  margin-left:0 !important;
  margin-right:0 !important;
  box-sizing:border-box !important;
}
.public-hero,
.gov-topbar,
.trust-strip {
  width:100% !important;
  box-sizing:border-box !important;
}

/* ===== LAPTOP / VIEWPORT FIT FIX ===== */
@media (min-width:851px) {
  section[data-testid="stSidebar"] {
    width:260px !important;
    min-width:260px !important;
    max-width:260px !important;
  }
  section[data-testid="stSidebar"] > div:first-child {
    width:260px !important;
  }
  /* Streamlit already reserves sidebar space when the sidebar exists.
     Do not subtract 260px here: public pages have no sidebar and would
     otherwise lose a large strip of usable width on the right. */
  [data-testid="stMain"] {
    width:100% !important;
    max-width:100% !important;
    min-width:0 !important;
  }
  [data-testid="stMainBlockContainer"], .block-container {
    width:100% !important;
    max-width:none !important;
    min-width:0 !important;
    box-sizing:border-box !important;
    overflow-x:visible !important;
  }
  .dashboard-title, .dashboard-sub, .ai-engine-card, .ai-engine-text, .metric-card, .module-card, .snapshot-card {
    max-width:100% !important;
    box-sizing:border-box !important;
  }
  .dashboard-sub, .ai-engine-text {
    white-space:normal !important;
    overflow-wrap:break-word !important;
    word-break:normal !important;
  }
}


  .feature1-status-chart {
    background:linear-gradient(145deg,#ffffff 0%,#f7f9fc 100%);
    border:1px solid #e3e8ef;
    border-radius:18px;
    padding:24px;
    box-shadow:0 7px 20px rgba(20,45,75,.06);
    margin:8px 0 18px 0;
  }
  .feature1-status-chart .status-row { margin:0 0 20px 0; }
  .feature1-status-chart .status-row:last-child { margin-bottom:0; }
  .feature1-status-chart .status-head {
    display:flex; justify-content:space-between; align-items:center;
    gap:12px; color:#26384b; font-size:.95rem; margin-bottom:8px;
  }
  .feature1-status-chart .status-dot {
    display:inline-block; width:9px; height:9px; border-radius:50%; margin-right:9px;
  }
  .feature1-status-chart .status-pct { color:#7b8794; font-weight:600; margin-left:6px; }
  .feature1-status-chart .status-track {
    height:13px; background:#e9edf2; border-radius:999px; overflow:hidden;
  }
  .feature1-status-chart .status-fill { height:100%; border-radius:999px; }
  .feature1-status-chart .status-note { margin-top:6px; color:#7b8794; font-size:.78rem; }
</style>
''', unsafe_allow_html=True)

PARLIAMENT_IMAGE = "https://opinionexpress.in/assets/images/article/constitutional-and-bureaucratic-reformsthe-urgent-necessity-in-india.jpg"

if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "show_login" not in st.session_state: st.session_state.show_login = False
if "public_section" not in st.session_state: st.session_state.public_section = "Home"
if "page" not in st.session_state: st.session_state.page = "Dashboard"


def public_header():
    st.markdown('''<div class="gov-topbar"><div class="gov-brand"><div class="gov-mark">☸</div><div><div class="gov-name">Government of India</div><div class="gov-sub">Ministry of Statistics &amp; Programme Implementation (MoSPI) • Programme Implementation Wing • MPLADS Monitoring</div></div></div></div>''', unsafe_allow_html=True)
    n1,n2,n3,n4 = st.columns([1.0,1.35,1.2,1.05])
    with n1:
        if st.button("Home", width="stretch", key="pub_home"):
            st.session_state.public_section="Home"; st.session_state.show_login=False; st.rerun()
    with n2:
        if st.button("About MPLADS", width="stretch", key="pub_about"):
            st.session_state.public_section="About"; st.session_state.show_login=False; st.rerun()
    with n3:
        if st.button("Transparency", width="stretch", key="pub_transparency"):
            st.session_state.public_section="Transparency"; st.session_state.show_login=False; st.rerun()
    with n4:
        if st.button("🔐  Login", type="primary", width="stretch", key="pub_login"):
            st.session_state.show_login=True; st.rerun()


def show_login_page():
    public_header()
    st.markdown('<div class="login-page-title">AUTHORIZED MONITORING ACCESS</div>', unsafe_allow_html=True)
    left, right = st.columns([1, 1], gap="large")

    with left:
        st.markdown(f'''<div class="login-visual" style="background-image:linear-gradient(145deg,rgba(7,38,67,.90),rgba(7,38,67,.30)),url('{PARLIAMENT_IMAGE}');">
            <div class="login-visual-copy">
                <div class="portal-kicker" style="color:#d9e8f5">MPLADS AI MONITOR</div>
                <div style="font-size:2rem;font-weight:900;margin-top:8px">Intelligent Monitoring &amp; Decision Support</div>
                <div style="margin-top:10px;color:rgba(255,255,255,.86);line-height:1.6;font-size:.9rem">AI-assisted anomaly screening, compliance monitoring and early-warning intelligence for MPLADS implementation.</div>
            </div>
        </div>''', unsafe_allow_html=True)

    with right:
        with st.container(border=True):
            st.markdown('<div class="portal-kicker">MINISTRY OF STATISTICS &amp; PROGRAMME IMPLEMENTATION</div><div class="login-title">Sign in</div><div class="login-sub">Authorized users can access the complete monitoring workspace and analytical modules.</div>', unsafe_allow_html=True)
            username = st.text_input("Official ID / Username", placeholder="Enter username", key="login_username_v2")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="login_password_v2")
            if st.button("Sign in to monitoring portal", type="primary", width="stretch", key="login_submit_v2"):
                if username == "admin" and password == "mplads123":
                    st.session_state.logged_in = True
                    st.session_state.show_login = False
                    st.session_state.public_section = "Home"
                    st.session_state.page = "Dashboard"
                    st.rerun()
                else:
                    st.error("Invalid demo credentials.")
            if st.button("← Back to public page", width="stretch", key="login_back_v2"):
                st.session_state.show_login = False
                st.rerun()
            st.markdown('<div class="demo-box"><b>Prototype access</b><br>Username: <b>admin</b> &nbsp; Password: <b>mplads123</b></div>', unsafe_allow_html=True)

def show_public_home():
    if st.session_state.show_login:
        show_login_page()
        return

    public_header()
    section = st.session_state.public_section

    if section == "About":
        st.markdown('''<div class="info-card" style="margin-top:24px;padding:30px 34px;">
            <div class="portal-kicker">ABOUT MPLADS</div>
            <div style="font-size:2.15rem;font-weight:900;color:#172b4d;margin-top:8px;line-height:1.15;">
                Members of Parliament Local Area Development Scheme (MPLADS)
            </div>
            <div class="info-text" style="font-size:.98rem;margin-top:16px;line-height:1.75;">
                MPLADS is a <b>Central Sector Scheme of the Government of India</b>, announced on
                <b>23 December 1993</b>. Its objective is to enable Members of Parliament to
                recommend developmental works that create durable community assets and respond to
                locally felt needs. Administration of the scheme has been with the
                <b>Ministry of Statistics &amp; Programme Implementation (MoSPI)</b> since October 1994.
                The current MPLADS Guidelines were released on <b>22 February 2023</b> and came into
                effect on <b>1 April 2023</b>.
            </div>
        </div>''', unsafe_allow_html=True)

        st.markdown('<div class="module-section-title">How the scheme works</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-note">The MP has a recommendatory role; sanction, execution and completion are handled by the responsible District Authorities.</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        steps = [
            ("01", "MP recommendation", "The MP recommends eligible developmental works based on locally felt needs."),
            ("02", "District-level action", "The District Authority sanctions and arranges execution under applicable administrative, technical and financial rules."),
            ("03", "Execution & monitoring", "Implementing authorities execute and monitor the works and their completion."),
        ]
        for c, (num, title, text) in zip(cols, steps):
            with c:
                st.markdown(f'''<div class="info-card" style="min-height:175px;"><div class="portal-kicker">{num}</div><div class="info-title" style="margin-top:8px;">{title}</div><div class="info-text">{text}</div></div>''', unsafe_allow_html=True)

        st.markdown('<div class="trust-strip" style="margin-top:20px;"><b style="color:#17365d;">About the scheme:</b><span style="color:#68778d;"> MPLADS enables locally felt developmental needs to be addressed through recommended works that create durable community assets.</span></div>', unsafe_allow_html=True)
        st.markdown('<div style="color:#7a8798;font-size:.72rem;margin-top:14px;">Source: Ministry of Statistics &amp; Programme Implementation, Government of India — MPLADS Annual Report 2023–24 and Programme Implementation material.</div>', unsafe_allow_html=True)
        return

    if section == "Transparency":
        st.markdown('''<div class="info-card" style="margin-top:24px;padding:30px 34px;"><div class="portal-kicker">TRANSPARENCY &amp; DATA USE</div><div style="font-size:2.15rem;font-weight:900;color:#172b4d;margin-top:8px;">Evidence-led monitoring</div><div class="info-text" style="font-size:.96rem;margin-top:14px;line-height:1.7;">The prototype analyses the supplied MPLADS implementation datasets and surfaces patterns that may require administrative review. The system distinguishes unavailable or masked values from genuine zero values wherever possible.</div></div>''', unsafe_allow_html=True)
        cols = st.columns(3)
        items = [("Source datasets", "Recommended, sanctioned, completed and expenditure/payment datasets supplied for the hackathon prototype."), ("Data limitations", "The supplied snapshot contains unavailable or masked financial fields and separate dataset coverage. The system does not invent missing values."), ("Review principle", "Every alert is a review indicator. Final administrative decisions remain with the competent authority.")]
        for c, (title, text) in zip(cols, items):
            with c:
                st.markdown(f'''<div class="info-card"><div class="info-title">{title}</div><div class="info-text">{text}</div></div>''', unsafe_allow_html=True)
        return

    # Clean public home: only the product hero and navigation actions.
    st.markdown(f'''<div class="public-hero"><div class="public-hero-grid"><div class="public-copy"><div class="portal-kicker" style="color:#bcd2e6;">MEMBERS OF PARLIAMENT LOCAL AREA DEVELOPMENT SCHEME</div><div class="public-title">MPLADS AI Monitor</div><div style="margin-top:10px;color:#d7e5f2;font-size:1.05rem;font-weight:650;">Intelligent Monitoring &amp; Decision Support System</div><div class="public-lead">A focused monitoring platform for identifying unusual patterns, prioritising review cases and providing explainable early-warning insights across MPLADS implementation.</div></div><div class="public-photo" style="background-image:url('{PARLIAMENT_IMAGE}')"></div></div></div>''', unsafe_allow_html=True)

    # Navigation is already provided in the government-style top bar above.
    # Keep the Home page focused on the hero; avoid duplicating the same actions below.

if not st.session_state.logged_in:
    show_public_home(); st.stop()

with st.sidebar:
    st.markdown('<div class="side-brand"><div class="side-title">🇮🇳 MPLADS AI Monitor</div><div class="side-sub">Programme Implementation • DIID</div></div>', unsafe_allow_html=True)
    st.divider()
    if st.button("🏠  Overview",width="stretch",key="side_overview"): st.session_state.page="Dashboard"; st.rerun()
    if st.button("🔎  Search Work",width="stretch",key="side_search"): st.session_state.page="Work Search"; st.rerun()
    st.markdown('<div class="side-label">MONITORING</div>', unsafe_allow_html=True)
    monitoring={"⏳  Delayed Projects":"Delayed Projects","💰  Financial Anomalies":"Financial Anomalies","📈  Cost Deviation":"Cost Deviation","🔁  Similar Works":"Similar Works","💳  Payment & Vendor":"Payment & Vendor","📋  Compliance":"Compliance"}
    for label,value in monitoring.items():
        if st.button(label,width="stretch",key=f"side_{value}"): st.session_state.page=value; st.rerun()
    st.markdown('<div class="side-label">INTELLIGENCE</div>',unsafe_allow_html=True)
    intelligence={"🧠  AI Risk Assessment":"AI Risk Assessment","📊  Trend Analysis":"Trend Analysis","🔮  Early Warning":"Early Warning"}
    for label,value in intelligence.items():
        if st.button(label,width="stretch",key=f"side_{value}"): st.session_state.page=value; st.rerun()
    st.divider(); st.caption("Decision-support prototype")
    if st.button("🚪  Sign Out",width="stretch",key="side_signout"):
        st.session_state.logged_in=False; st.session_state.page="Dashboard"; st.session_state.show_login=False; st.rerun()

def load_portal_data():
    df = pd.read_csv(SANCTIONED_FILE, low_memory=False)
    df.columns = df.columns.astype(str).str.strip()
    return df


@st.cache_data(show_spinner=False)
def get_portal_summary():
    df = load_portal_data()
    state_col = find_column(df, ["State"])
    status_col = find_column(df, ["Work Status"])
    sanction_col = find_column(df, ["Sanction Date", "Sanction date"])
    if sanction_col:
        dates = pd.to_datetime(df[sanction_col], errors="coerce")
        days = (pd.Timestamp.today().normalize() - dates).dt.days
    else:
        days = pd.Series(np.nan, index=df.index)
    status = df[status_col].fillna("").astype(str).str.lower() if status_col else pd.Series("", index=df.index)
    completed = status.str.contains(r"\bcompleted\b", regex=True, na=False)
    overdue = days.gt(365) & ~completed
    upcoming = days.between(275, 364, inclusive="both") & ~completed
    return {
        "df": df,
        "total": len(df),
        "completed": int(completed.sum()),
        "overdue": int(overdue.sum()),
        "upcoming": int(upcoming.sum()),
        "states": int(df[state_col].replace("", np.nan).dropna().nunique()) if state_col else 0,
        "state_col": state_col,
        "status_col": status_col,
        "sanction_col": sanction_col,
        "days": days,
        "completed_mask": completed,
        "overdue_mask": overdue,
    }



def show_dashboard():
    summary = get_portal_summary()
    df = summary["df"]

    st.markdown('<div class="dashboard-title">MPLADS AI Monitor</div>', unsafe_allow_html=True)
    st.markdown('<div class="dashboard-sub"><b>National Oversight Dashboard</b> &nbsp;•&nbsp; Monitoring, anomaly screening, compliance and AI-assisted early warning.</div>', unsafe_allow_html=True)

    st.markdown('''<div class="ai-engine-card">
        <div class="ai-engine-title">● AI ENGINE ACTIVE</div>
        <div class="ai-engine-text"><b>AI/ML layer:</b> Isolation Forest detects unusual combinations of available work-level signals. It is fused with rule-based indicators, peer deviation and text-similarity signals to create an explainable review priority. The system flags <b>review candidates</b> — it does not declare fraud.</div>
    </div>''', unsafe_allow_html=True)

    cards = [
        ("Works monitored", summary["total"], "Sanctioned-work snapshot"),
        ("Marked completed", summary["completed"], "Status-based evidence"),
        ("Beyond 1-year benchmark", summary["overdue"], "Requires attention"),
        ("Approaching benchmark", summary["upcoming"], "Early-warning window"),
    ]
    for row in range(2):
        cols = st.columns(2)
        for col, (label, value, note) in zip(cols, cards[row*2:(row+1)*2]):
            with col:
                st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value:,}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="module-section-title">Monitoring modules</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-note">Operational checks — each module opens the full existing analytical workflow.</div>', unsafe_allow_html=True)
    monitoring = [
        ("⏳", "Delayed Projects", "Completion-age monitoring and delayed-work investigation.", "Delayed Projects"),
        ("💰", "Financial Anomalies", "Fund-disbursement and utilization-pattern screening.", "Financial Anomalies"),
        ("📈", "Cost Deviation", "Peer-based comparison of amounts by State and work type.", "Cost Deviation"),
        ("🔁", "Similar Works", "Exact-description and high-similarity work screening.", "Similar Works"),
        ("💳", "Payment & Vendor", "Payment-status and vendor-concentration review.", "Payment & Vendor"),
        ("📋", "Compliance", "Recommendation-to-sanction and completion benchmarks.", "Compliance"),
    ]
    for row in range(2):
        cols = st.columns(3)
        for j, c in enumerate(cols):
            icon, title, desc, value = monitoring[row*3+j]
            with c:
                st.markdown(f'<div class="module-card"><div class="module-icon">{icon}</div><div class="module-title">{title}</div><div class="module-desc">{desc}</div></div>', unsafe_allow_html=True)
                if st.button("Open module →", width="stretch", key=f"dash_mod_{value}"):
                    st.session_state.page = value
                    st.rerun()

    st.markdown('<div class="module-section-title">Intelligence modules</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-note">Where the analytical and AI layers turn signals into explainable priorities and forecasts.</div>', unsafe_allow_html=True)
    intelligence = [
        ("🧠", "AI Risk Assessment", "Actual ML anomaly detection + explainable signals for work-level review prioritization.", "AI Risk Assessment"),
        ("📊", "Trend Analysis", "Year-wise and State-wise activity patterns from the supplied datasets.", "Trend Analysis"),
        ("🔮", "Early Warning", "Forward-looking timeline alerts for works nearing the one-year benchmark.", "Early Warning"),
    ]
    cols = st.columns(3)
    for c, (icon, title, desc, value) in zip(cols, intelligence):
        with c:
            st.markdown(f'<div class="module-card ai-module"><div class="module-icon">{icon}</div><div class="module-title">{title}</div><div class="module-desc">{desc}</div></div>', unsafe_allow_html=True)
            if st.button("Open module →", width="stretch", key=f"dash_int_{value}"):
                st.session_state.page = value
                st.rerun()

    st.markdown('<div class="module-section-title">At-a-glance evidence</div>', unsafe_allow_html=True)
    left, right = st.columns(2)
    status_col = summary["status_col"]
    state_col = summary["state_col"]
    with left:
        st.markdown('<div class="snapshot-card"><div class="info-title">Work status snapshot</div><div class="info-text">Current status distribution in the sanctioned-work dataset.</div></div>', unsafe_allow_html=True)
        if status_col:
            counts = df[status_col].fillna("Unknown").astype(str).replace("", "Unknown").value_counts().head(8).rename_axis("Status").reset_index(name="Works")
            st.dataframe(counts, width="stretch", hide_index=True, height=310)
        else:
            st.info("Work status data unavailable.")
    with right:
        st.markdown('<div class="snapshot-card"><div class="info-title">State activity snapshot</div><div class="info-text">States with the largest record counts in the sanctioned-work dataset.</div></div>', unsafe_allow_html=True)
        if state_col:
            counts = df[state_col].fillna("Unknown").astype(str).replace("", "Unknown").value_counts().head(10).rename_axis("State").reset_index(name="Works")
            st.dataframe(counts, width="stretch", hide_index=True, height=310)
        else:
            st.info("State data unavailable.")

    st.caption("Review indicators support administrative decision-making; they do not establish fraud, misuse or wrongdoing.")

def show_work_search():
    st.title("🔎 Work Search & Investigation")
    st.caption("Search the sanctioned-works dataset by Work ID, work description, state or constituency.")
    df = load_portal_data()
    work_col = find_column(df, ["Work"])
    desc_col = find_column(df, ["Work Description"])
    state_col = find_column(df, ["State"])
    const_col = find_column(df, ["Constituency"])
    status_col = find_column(df, ["Work Status"])
    sanction_col = find_column(df, ["Sanction Date", "Sanction date"])
    mp_col = find_column(df, ["Hon’ble Member", "Hon'ble Member", "Hon’ble Members of Parliament", "Hon'ble Members of Parliament"])

    query = st.text_input("🔍 Search", placeholder="Enter Work ID, work description, state or constituency...")
    if query.strip():
        q = query.strip().lower()
        mask = pd.Series(False, index=df.index)
        for col in [work_col, desc_col, state_col, const_col, mp_col]:
            if col:
                mask = mask | df[col].fillna("").astype(str).str.lower().str.contains(q, na=False)
        results = df.loc[mask].copy()
    else:
        results = df.head(0).copy()

    st.write(f"**{len(results):,} matching works**")
    display_cols = [c for c in [work_col, state_col, const_col, mp_col, sanction_col, status_col] if c]
    if not results.empty:
        st.dataframe(results[display_cols].head(100), width="stretch", hide_index=True)

        options = results.index.tolist()
        labels = []
        lookup = {}
        for idx in options:
            work = str(results.loc[idx, work_col]) if work_col else "Work unavailable"
            state = str(results.loc[idx, state_col]) if state_col else "Unknown"
            label = f"{state} | {work[:110]}"
            labels.append(label)
            lookup[label] = idx

        selected = st.selectbox("Select a work to investigate", labels, key="global_work_search_select")
        row = df.loc[lookup[selected]]

        st.divider()
        st.subheader("Work Details")
        a,b,c = st.columns(3)
        with a:
            st.write("**State**", row[state_col] if state_col else "Unavailable")
            st.write("**Constituency**", row[const_col] if const_col else "Unavailable")
            st.write("**MP**", row[mp_col] if mp_col else "Unavailable")
        with b:
            st.write("**Work**", row[work_col] if work_col else "Unavailable")
            st.write("**Sanction Date**", row[sanction_col] if sanction_col else "Unavailable")
            st.write("**Work Status**", row[status_col] if status_col else "Unavailable")
        with c:
            if desc_col:
                st.write("**Work Description**", row[desc_col] if str(row[desc_col]).strip() else "Description Unavailable")
    else:
        st.info("Enter a search term to find a work.")


# ============================================================
# FEATURE FUNCTIONS — ORIGINAL ANALYTICS
# ============================================================


def feature_1():
    # ============================================================
    # LOAD DATA — CACHED
    # ============================================================

    @st.cache_data(show_spinner=False)
    def load_feature1():

        sanctioned = pd.read_csv(
            SANCTIONED_FILE,
            low_memory=False
        )

        completed = pd.read_csv(
            COMPLETED_FILE,
            low_memory=False
        )

        sanctioned.columns = (
            sanctioned.columns
            .astype(str)
            .str.strip()
        )

        completed.columns = (
            completed.columns
            .astype(str)
            .str.strip()
        )

        return sanctioned, completed


    # ============================================================
    # PROCESS DATA — CACHED
    # ============================================================

    @st.cache_data(show_spinner=False)
    def process_feature1(sanctioned, completed):

        # --------------------------------------------------------
        # FIND COLUMNS
        # --------------------------------------------------------

        state_col = find_column(
            sanctioned,
            ["State"]
        )

        constituency_col = find_column(
            sanctioned,
            ["Constituency"]
        )

        work_col = find_column(
            sanctioned,
            ["Work"]
        )

        description_col = find_column(
            sanctioned,
            ["Work Description"]
        )

        sanction_col = find_column(
            sanctioned,
            ["Sanction Date"]
        )

        status_col = find_column(
            sanctioned,
            ["Work Status", "Status"]
        )

        completed_work_col = find_column(
            completed,
            ["Work"]
        )

        # --------------------------------------------------------
        # CREATE DATAFRAME
        # --------------------------------------------------------

        df = pd.DataFrame(index=sanctioned.index)

        if state_col:
            df["State"] = clean_series(
                sanctioned[state_col]
            )
        else:
            df["State"] = "Not Available"

        if constituency_col:
            df["Constituency"] = clean_series(
                sanctioned[constituency_col]
            )
        else:
            df["Constituency"] = "Not Available"

        if work_col:
            df["Work ID"] = clean_series(
                sanctioned[work_col]
            )
        else:
            df["Work ID"] = ""

        # --------------------------------------------------------
        # DESCRIPTION + CORRUPTION CLEANUP
        # --------------------------------------------------------

        if description_col:

            df["Work Description"] = clean_series(
                sanctioned[description_col]
            )

            text = df["Work Description"]

            # Detect strings containing repeated ?
            corrupted = (
                text.str.contains(
                    r"\?{2,}",
                    regex=True,
                    na=False
                )
            )

            # Detect descriptions made mostly from ?
            mostly_question_marks = (
                text.str.replace(
                    "?",
                    "",
                    regex=False
                )
                .str.replace(
                    " ",
                    "",
                    regex=False
                )
                .str.len()
                == 0
            )

            df.loc[
                corrupted | mostly_question_marks,
                "Work Description"
            ] = "Description Unavailable"

            # Blank descriptions
            df.loc[
                df["Work Description"] == "",
                "Work Description"
            ] = "Description Unavailable"

        else:

            df["Work Description"] = (
                "Description Unavailable"
            )

        # --------------------------------------------------------
        # SANCTION DATE
        # --------------------------------------------------------

        if sanction_col:

            df["Sanction Date"] = pd.to_datetime(
                sanctioned[sanction_col],
                errors="coerce",
                dayfirst=True
            )

        else:

            df["Sanction Date"] = pd.NaT

        # --------------------------------------------------------
        # WORK STATUS
        # --------------------------------------------------------

        if status_col:

            df["Work Status"] = clean_series(
                sanctioned[status_col]
            )

        else:

            df["Work Status"] = ""

        # --------------------------------------------------------
        # COMPLETED WORK IDS
        # --------------------------------------------------------

        if completed_work_col:

            completed_ids = set(
                clean_series(
                    completed[completed_work_col]
                )
            )

            completed_ids.discard("")

        else:

            completed_ids = set()

        # --------------------------------------------------------
        # COMPLETION FROM STATUS
        # --------------------------------------------------------

        status_lower = (
            df["Work Status"]
            .str.lower()
        )

        status_completed = (
            status_lower.str.contains(
                "completed",
                regex=False,
                na=False
            )
            &
            ~status_lower.str.contains(
                "not completed",
                regex=False,
                na=False
            )
        )

        # --------------------------------------------------------
        # COMPLETION FROM COMPLETED FILE
        # --------------------------------------------------------

        id_completed = (
            df["Work ID"].isin(
                completed_ids
            )
            &
            (df["Work ID"] != "")
        )

        df["Completed"] = (
            status_completed |
            id_completed
        )

        # --------------------------------------------------------
        # DAYS SINCE SANCTION
        # --------------------------------------------------------

        today = pd.Timestamp.now().normalize()

        df["Days Since Sanction"] = (
            today -
            df["Sanction Date"]
        ).dt.days

        df["Days Since Sanction"] = (
            df["Days Since Sanction"]
            .clip(lower=0)
        )

        # --------------------------------------------------------
        # RISK LEVEL
        # --------------------------------------------------------

        df["Risk Level"] = "Insufficient Data"

        # Completed
        df.loc[
            df["Completed"],
            "Risk Level"
        ] = "Completed"

        # Valid unfinished records
        valid = (
            df["Sanction Date"].notna()
            &
            ~df["Completed"]
        )

        # Low
        df.loc[
            valid &
            (df["Days Since Sanction"] < 270),
            "Risk Level"
        ] = "Low"

        # Medium
        df.loc[
            valid &
            (df["Days Since Sanction"] >= 270) &
            (df["Days Since Sanction"] <= 365),
            "Risk Level"
        ] = "Medium"

        # High
        df.loc[
            valid &
            (df["Days Since Sanction"] > 365),
            "Risk Level"
        ] = "High"

        # --------------------------------------------------------
        # REASON
        # --------------------------------------------------------

        df["Reason"] = (
            "Sanction date unavailable."
        )

        df.loc[
            df["Completed"],
            "Reason"
        ] = (
            "Completion evidence available."
        )

        df.loc[
            valid &
            (df["Days Since Sanction"] < 270),
            "Reason"
        ] = (
            "Work is within the monitoring period."
        )

        df.loc[
            valid &
            (df["Days Since Sanction"] >= 270) &
            (df["Days Since Sanction"] <= 365),
            "Reason"
        ] = (
            "Work is approaching the one-year "
            "completion benchmark."
        )

        df.loc[
            valid &
            (df["Days Since Sanction"] > 365),
            "Reason"
        ] = (
            "More than one year has passed since sanction."
        )

        return df


    # ============================================================
    # HEADER
    # ============================================================

    st.title(
        "🇮🇳 MPLADS AI Monitoring Platform"
    )

    st.subheader(
        "⏳ Delayed Project & Completion Detection"
    )

    st.caption(
        "Transparent monitoring of sanctioned works using completion evidence and elapsed time."
    )


    # ============================================================
    # LOAD + PROCESS
    # ============================================================

    try:

        sanctioned_data, completed_data = (
            load_feature1()
        )

        df = process_feature1(
            sanctioned_data,
            completed_data
        )

    except FileNotFoundError:

        st.error(
            "❌ Required MPLADS CSV files were not found."
        )

        st.info(
            "Make sure both CSV files are inside the data folder."
        )

        st.stop()

    except Exception as e:

        st.error(
            "❌ Error while processing MPLADS data."
        )

        st.exception(e)

        st.stop()


    # ============================================================
    # KPI COUNTS
    # ============================================================

    total_count = len(df)

    completed_count = int(
        (df["Risk Level"] == "Completed").sum()
    )

    high_count = int(
        (df["Risk Level"] == "High").sum()
    )

    medium_count = int(
        (df["Risk Level"] == "Medium").sum()
    )

    low_count = int(
        (df["Risk Level"] == "Low").sum()
    )

    insufficient_count = int(
        (df["Risk Level"] == "Insufficient Data").sum()
    )


    # ============================================================
    # KPI SECTION
    # ============================================================

    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric("Works Analyzed", f"{total_count:,}")
    with k2:
        st.metric("Completion Evidence", f"{completed_count:,}")
    with k3:
        st.metric("High Delay", f"{high_count:,}")

    k4, k5, k6 = st.columns(3)
    with k4:
        st.metric("Medium", f"{medium_count:,}")
    with k5:
        st.metric("Low", f"{low_count:,}")
    with k6:
        st.metric("Data Review", f"{insufficient_count:,}")


    # ============================================================
    # GRAPH — CLEAN NATIVE STREAMLIT STATUS DISTRIBUTION
    # ============================================================

    st.divider()
    st.subheader("📊 Project Monitoring Overview")
    st.caption("Number of sanctioned works in each monitoring category.")

    chart_df = pd.DataFrame(
        {
            "Works": [
                completed_count,
                high_count,
                medium_count,
                low_count,
                insufficient_count,
            ]
        },
        index=[
            "Completed",
            "High Delay",
            "Medium",
            "Low",
            "Data Review",
        ],
    )

    st.bar_chart(
        chart_df,
        use_container_width=True,
        height=380,
    )

    # Compact legend beneath the chart so the meaning of each category is
    # immediately clear during a presentation.
    legend_cols = st.columns(5)
    legend_items = [
        ("Completed", completed_count, "Completion evidence available"),
        ("High Delay", high_count, ">365 days since sanction"),
        ("Medium", medium_count, "270–365 days since sanction"),
        ("Low", low_count, "<270 days since sanction"),
        ("Data Review", insufficient_count, "Sanction date unavailable"),
    ]
    for col, (label, count, note) in zip(legend_cols, legend_items):
        with col:
            pct = (count / total_count * 100) if total_count else 0
            st.markdown(f"**{label}**  \n{count:,} works · {pct:.1f}%")
            st.caption(note)


    # ============================================================
    # SUMMARY
    # ============================================================

    attention_count = (
        high_count +
        medium_count
    )

    st.divider()

    s1, s2, s3 = st.columns(3)

    with s1:

        st.info(
            f"📌 **{attention_count:,} works** "
            "are currently in Medium or High monitoring categories."
        )

    with s2:

        st.success(
            f"✅ **{completed_count:,} works** "
            "have completion evidence."
        )

    with s3:

        st.warning(
            f"⚠️ **{insufficient_count:,} records** "
            "need better date information."
        )


    # ============================================================
    # FILTERS
    # ============================================================

    st.divider()

    st.subheader(
        "🔎 Monitor Works"
    )

    f1, f2, f3 = st.columns(3)

    states = sorted(
        [
            x for x in df["State"].unique()
            if x
        ]
    )

    with f1:

        state_filter = st.selectbox(
            "State",
            ["All States"] + states,
            key="feature1_state"
        )

    with f2:

        risk_filter = st.selectbox(
            "Risk Level",
            [
                "All Risk Levels",
                "High",
                "Medium",
                "Low",
                "Completed",
                "Insufficient Data"
            ],
            key="feature1_risk"
        )

    with f3:

        search = st.text_input(
            "Search Work",
            placeholder="Work ID or description...",
            key="feature1_search"
        )


    # ============================================================
    # APPLY FILTERS
    # ============================================================

    view = df

    if state_filter != "All States":

        view = view[
            view["State"] == state_filter
        ]

    if risk_filter != "All Risk Levels":

        view = view[
            view["Risk Level"] == risk_filter
        ]

    if search.strip():

        search_value = (
            search
            .strip()
            .lower()
        )

        mask = (
            view["Work ID"]
            .str.lower()
            .str.contains(
                search_value,
                regex=False,
                na=False
            )
            |
            view["Work Description"]
            .str.lower()
            .str.contains(
                search_value,
                regex=False,
                na=False
            )
        )

        view = view[mask]


    # ============================================================
    # TABLE
    # ============================================================

    display = view[
        [
            "State",
            "Constituency",
            "Work ID",
            "Work Description",
            "Sanction Date",
            "Days Since Sanction",
            "Risk Level",
            "Reason"
        ]
    ].copy()

    display["Sanction Date"] = (
        display["Sanction Date"]
        .dt.strftime("%d-%m-%Y")
        .fillna("Not Available")
    )

    display["Days Since Sanction"] = (
        display["Days Since Sanction"]
        .fillna(0)
        .astype(int)
    )

    st.write(
        f"Showing **{len(display):,}** works"
    )

    st.dataframe(
        display,
        width="stretch",
        height=480,
        hide_index=True
    )


    # ============================================================
    # INVESTIGATION VIEW
    # ============================================================

    st.divider()

    st.subheader(
        "🔍 Investigation View"
    )

    if len(view) > 0:

        selected_index = st.selectbox(
            "Select a work",
            view.index,
            format_func=lambda i:
                f"{view.loc[i, 'Work ID']} — "
                f"{view.loc[i, 'Risk Level']}",
            key="feature1_investigation"
        )

        record = view.loc[
            selected_index
        ]

        x1, x2, x3 = st.columns(3)

        x1.metric(
            "Risk Level",
            record["Risk Level"]
        )

        if pd.notna(
            record["Days Since Sanction"]
        ):

            x2.metric(
                "Days Since Sanction",
                f"{int(record['Days Since Sanction'])}"
            )

        else:

            x2.metric(
                "Days Since Sanction",
                "Not Available"
            )

        x3.metric(
            "Completion Evidence",
            "Yes"
            if record["Completed"]
            else "No"
        )

        st.info(
            f"**Assessment:** {record['Reason']}"
        )

        st.write(
            "**State:**",
            record["State"]
            if record["State"]
            else "Not Available"
        )

        st.write(
            "**Constituency:**",
            record["Constituency"]
            if record["Constituency"]
            else "Not Available"
        )

        st.write(
            "**Work Description:**",
            record["Work Description"]
            if record["Work Description"]
            else "Description Unavailable"
        )

    else:

        st.info(
            "No works match the selected filters."
        )


    # ============================================================
    # METHODOLOGY
    # ============================================================

    with st.expander(
        "📘 How Feature 1 Works"
    ):

        st.markdown(
            """
    ### Completion detection

    A work is treated as having completion evidence when:

    - the **Work Status** indicates completion, OR
    - its **Work ID** appears in the Works Completed dataset.

    ### Monitoring classification

    | Category | Condition |
    |---|---|
    | 🟢 Completed | Completion evidence available |
    | 🔵 Low | Less than 270 days since sanction |
    | 🟡 Medium | 270–365 days since sanction |
    | 🔴 High | More than 365 days since sanction |
    | ⚪ Insufficient Data | Sanction date unavailable |

    ### Data quality

    Unreadable descriptions containing corrupted `???` values are
    shown as **Description Unavailable** instead of displaying
    corrupted source text.

    ### Important

    The one-year period is used as a **monitoring benchmark**.

    A High result is an indicator requiring review. It is **not
    proof of fraud or non-compliance**.
            """
        )


    # ============================================================
    # FOOTER
    # ============================================================

    st.divider()

    st.caption(
        "MPLADS AI Monitoring Platform • Feature 1 • "
        "Transparent monitoring indicator"
    )


    # ============================================================

def feature_2():
    # FEATURE 2 — FINANCIAL & FUND UTILIZATION ANOMALY DETECTION
    # FAST + PRESENTATION READY
    # ============================================================

    EXPENDITURE_FILE = (
        DATA_DIR /
        "Expenditure on Completed and On-going Works as on Date.csv"
    )


    # ============================================================
    # LOAD FEATURE 2 DATA — CACHED
    # ============================================================

    @st.cache_data(show_spinner=False)
    def load_feature2_data():

        df = pd.read_csv(
            EXPENDITURE_FILE,
            low_memory=False
        )

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
        )

        return df


    # ============================================================
    # MONEY CONVERSION
    # ============================================================

    def convert_money(series):

        return pd.to_numeric(
            series
            .astype(str)
            .str.replace("₹", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
            .replace(
                [
                    "",
                    "*****",
                    "nan",
                    "None",
                    "none",
                    "null",
                    "N/A",
                    "n/a"
                ],
                np.nan
            ),
            errors="coerce"
        )


    # ============================================================
    # PROCESS FEATURE 2 — CACHED
    # ============================================================

    @st.cache_data(show_spinner=False)
    def process_feature2(raw):

        # --------------------------------------------------------
        # FIND COLUMNS
        # --------------------------------------------------------

        state_col = find_column(
            raw,
            ["State"]
        )

        constituency_col = find_column(
            raw,
            ["Constituency"]
        )

        work_col = find_column(
            raw,
            ["Work"]
        )

        work_id_col = find_column(
            raw,
            ["Work ID"]
        )

        member_col = find_column(
            raw,
            ["Hon'ble Member", "Hon’ble Member"]
        )

        vendor_col = find_column(
            raw,
            ["Vendor Name"]
        )

        payment_col = find_column(
            raw,
            ["Payment Status"]
        )

        fund_col = find_column(
            raw,
            ["Fund Disbursed Amount"]
        )

        expenditure_col = find_column(
            raw,
            ["Expenditure"]
        )

        # --------------------------------------------------------
        # CREATE CLEAN DATAFRAME
        # --------------------------------------------------------

        df = pd.DataFrame(index=raw.index)

        # State
        if state_col:
            df["State"] = clean_series(
                raw[state_col]
            )
        else:
            df["State"] = "Not Available"

        # Constituency
        if constituency_col:
            df["Constituency"] = clean_series(
                raw[constituency_col]
            )
        else:
            df["Constituency"] = "Not Available"

        # Work
        if work_col:
            df["Work"] = clean_series(
                raw[work_col]
            )
        else:
            df["Work"] = ""

        # Work ID
        if work_id_col:
            df["Work ID"] = clean_series(
                raw[work_id_col]
            )
        else:
            df["Work ID"] = ""

        # Member
        if member_col:
            df["Hon'ble Member"] = clean_series(
                raw[member_col]
            )
        else:
            df["Hon'ble Member"] = ""

        # Vendor
        if vendor_col:
            df["Vendor Name"] = clean_series(
                raw[vendor_col]
            )
        else:
            df["Vendor Name"] = "Not Available"

        # Payment status
        if payment_col:
            df["Payment Status"] = clean_series(
                raw[payment_col]
            )
        else:
            df["Payment Status"] = "Not Available"

        # --------------------------------------------------------
        # FUND DISBURSED
        # --------------------------------------------------------

        if fund_col:

            df["Fund Disbursed Amount"] = (
                convert_money(
                    raw[fund_col]
                )
            )

        else:

            df["Fund Disbursed Amount"] = np.nan

        # --------------------------------------------------------
        # EXPENDITURE
        # --------------------------------------------------------

        if expenditure_col:

            df["Expenditure"] = (
                convert_money(
                    raw[expenditure_col]
                )
            )

        else:

            df["Expenditure"] = np.nan

        # --------------------------------------------------------
        # DATA AVAILABILITY
        # --------------------------------------------------------

        df["Fund Available"] = (
            df["Fund Disbursed Amount"].notna()
        )

        df["Expenditure Available"] = (
            df["Expenditure"].notna()
        )

        # --------------------------------------------------------
        # UTILIZATION
        # --------------------------------------------------------

        df["Utilization %"] = np.nan

        valid_utilization = (
            df["Fund Disbursed Amount"].notna()
            &
            df["Expenditure"].notna()
            &
            (df["Fund Disbursed Amount"] > 0)
        )

        df.loc[
            valid_utilization,
            "Utilization %"
        ] = (
            df.loc[
                valid_utilization,
                "Expenditure"
            ]
            /
            df.loc[
                valid_utilization,
                "Fund Disbursed Amount"
            ]
            * 100
        )

        # --------------------------------------------------------
        # STATE-LEVEL STATISTICS
        # --------------------------------------------------------

        usable = df[
            df["Fund Disbursed Amount"].notna()
            &
            (df["Fund Disbursed Amount"] >= 0)
        ]

        if len(usable) > 0:

            state_group = (
                usable
                .groupby("State")[
                    "Fund Disbursed Amount"
                ]
            )

            q1 = state_group.transform(
                "quantile",
                0.25
            )

            q3 = state_group.transform(
                "quantile",
                0.75
            )

            median = state_group.transform(
                "median"
            )

            iqr = q3 - q1

            upper_fence = (
                q3 +
                (1.5 * iqr)
            )

            df["State Median"] = np.nan
            df["State Upper Fence"] = np.nan

            df.loc[
                usable.index,
                "State Median"
            ] = median.values

            df.loc[
                usable.index,
                "State Upper Fence"
            ] = upper_fence.values

        else:

            df["State Median"] = np.nan
            df["State Upper Fence"] = np.nan

        # --------------------------------------------------------
        # ABOVE MEDIAN %
        # --------------------------------------------------------

        df["Above State Median %"] = np.nan

        valid_median = (
            df["Fund Disbursed Amount"].notna()
            &
            df["State Median"].notna()
            &
            (df["State Median"] > 0)
        )

        df.loc[
            valid_median,
            "Above State Median %"
        ] = (
            (
                df.loc[
                    valid_median,
                    "Fund Disbursed Amount"
                ]
                -
                df.loc[
                    valid_median,
                    "State Median"
                ]
            )
            /
            df.loc[
                valid_median,
                "State Median"
            ]
            * 100
        )

        # --------------------------------------------------------
        # RISK LEVEL
        # --------------------------------------------------------

        df["Risk Level"] = "Insufficient Data"

        amount_available = (
            df["Fund Disbursed Amount"].notna()
        )

        # Extreme statistical outlier
        high = (
            amount_available
            &
            df["State Upper Fence"].notna()
            &
            (
                df["Fund Disbursed Amount"]
                >
                df["State Upper Fence"]
            )
        )

        # 50%+ above state median
        medium = (
            amount_available
            &
            df["State Median"].notna()
            &
            (df["State Median"] > 0)
            &
            (df["Above State Median %"] >= 50)
            &
            ~high
        )

        # Normal
        df.loc[
            amount_available,
            "Risk Level"
        ] = "Normal"

        df.loc[
            medium,
            "Risk Level"
        ] = "Medium"

        df.loc[
            high,
            "Risk Level"
        ] = "High"

        # --------------------------------------------------------
        # REASON
        # --------------------------------------------------------

        df["Reason"] = (
            "Fund disbursement is within the observed "
            "state-level range."
        )

        df.loc[
            medium,
            "Reason"
        ] = (
            "Fund disbursement is substantially above "
            "the state-level median."
        )

        df.loc[
            high,
            "Reason"
        ] = (
            "Fund disbursement is an extreme statistical "
            "outlier within the state."
        )

        df.loc[
            ~amount_available,
            "Reason"
        ] = (
            "Fund disbursement amount is unavailable."
        )

        return df


    # ============================================================
    # FEATURE 2 HEADER
    # ============================================================

    st.divider()

    st.title(
        "💰 Financial & Fund-Utilization Monitoring"
    )

    st.caption(
        "Detects unusual fund-disbursement patterns using "
        "state-level statistical analysis."
    )


    # ============================================================
    # LOAD + PROCESS
    # ============================================================

    try:

        financial_raw = load_feature2_data()

        financial_df = process_feature2(
            financial_raw
        )

    except FileNotFoundError:

        st.error(
            "❌ Financial expenditure dataset was not found."
        )

        st.info(
            "Check that the CSV is inside the data folder."
        )

        st.stop()

    except Exception as e:

        st.error(
            "❌ Error while processing financial data."
        )

        st.exception(e)

        st.stop()


    # ============================================================
    # KPI CALCULATIONS
    # ============================================================

    financial_total = len(
        financial_df
    )

    fund_available = int(
        financial_df["Fund Available"].sum()
    )

    expenditure_available = int(
        financial_df["Expenditure Available"].sum()
    )

    expenditure_unavailable = (
        financial_total -
        expenditure_available
    )

    financial_high = int(
        (
            financial_df["Risk Level"] ==
            "High"
        ).sum()
    )

    financial_medium = int(
        (
            financial_df["Risk Level"] ==
            "Medium"
        ).sum()
    )

    financial_normal = int(
        (
            financial_df["Risk Level"] ==
            "Normal"
        ).sum()
    )


    # ============================================================
    # DATA QUALITY SECTION
    # ============================================================

    st.subheader(
        "📊 Financial Data Quality"
    )

    q1, q2, q3, q4 = st.columns(4)

    q1.metric(
        "Financial Records",
        f"{financial_total:,}"
    )

    q2.metric(
        "Usable Fund Amounts",
        f"{fund_available:,}"
    )

    q3.metric(
        "Usable Expenditure",
        f"{expenditure_available:,}"
    )

    q4.metric(
        "Expenditure Unavailable",
        f"{expenditure_unavailable:,}"
    )


    if expenditure_unavailable > 0:

        st.warning(
            f"⚠️ Expenditure is unavailable for "
            f"**{expenditure_unavailable:,} records** "
            "because the source contains masked values such as "
            "`*****`. These values are not treated as zero."
        )


    # ============================================================
    # RISK KPIs
    # ============================================================

    st.subheader(
        "🚨 Financial Monitoring Indicators"
    )

    k1, k2, k3 = st.columns(3)

    k1.metric(
        "High Anomaly Indicators",
        f"{financial_high:,}"
    )

    k2.metric(
        "Medium Anomaly Indicators",
        f"{financial_medium:,}"
    )

    k3.metric(
        "Normal",
        f"{financial_normal:,}"
    )


    # ============================================================
    # RISK DISTRIBUTION GRAPH
    # ============================================================

    st.subheader(
        "📈 Financial Anomaly Distribution"
    )

    financial_chart = pd.DataFrame(
        {
            "Risk Level": [
                "High",
                "Medium",
                "Normal",
                "Insufficient Data"
            ],
            "Records": [
                financial_high,
                financial_medium,
                financial_normal,
                int(
                    (
                        financial_df["Risk Level"] ==
                        "Insufficient Data"
                    ).sum()
                )
            ]
        }
    )

    st.bar_chart(
        financial_chart.set_index(
            "Risk Level"
        ),
        width="stretch"
    )


    # ============================================================
    # MONITORING SUMMARY
    # ============================================================

    financial_attention = (
        financial_high +
        financial_medium
    )

    s1, s2, s3 = st.columns(3)

    with s1:

        st.error(
            f"🔴 **{financial_high:,}** "
            "high statistical anomaly indicators."
        )

    with s2:

        st.warning(
            f"🟡 **{financial_medium:,}** "
            "medium anomaly indicators."
        )

    with s3:

        st.info(
            f"📌 **{financial_attention:,}** "
            "records require closer financial review."
        )


    # ============================================================
    # FILTERS
    # ============================================================

    st.divider()

    st.subheader(
        "🔎 Financial Monitoring"
    )

    f1, f2, f3 = st.columns(3)

    financial_states = sorted(
        [
            x
            for x in financial_df["State"].unique()
            if x
        ]
    )

    with f1:

        selected_financial_state = st.selectbox(
            "State",
            ["All States"] +
            financial_states,
            key="feature2_state"
        )

    with f2:

        selected_financial_risk = st.selectbox(
            "Risk Level",
            [
                "All Risk Levels",
                "High",
                "Medium",
                "Normal",
                "Insufficient Data"
            ],
            key="feature2_risk"
        )

    with f3:

        financial_search = st.text_input(
            "Search Work / Work ID",
            placeholder="Enter work or ID...",
            key="feature2_search"
        )


    # ============================================================
    # APPLY FILTERS
    # ============================================================

    financial_view = financial_df

    if selected_financial_state != "All States":

        financial_view = financial_view[
            financial_view["State"] ==
            selected_financial_state
        ]

    if selected_financial_risk != "All Risk Levels":

        financial_view = financial_view[
            financial_view["Risk Level"] ==
            selected_financial_risk
        ]

    if financial_search.strip():

        search_value = (
            financial_search
            .strip()
            .lower()
        )

        mask = (
            financial_view["Work"]
            .str.lower()
            .str.contains(
                search_value,
                regex=False,
                na=False
            )
            |
            financial_view["Work ID"]
            .str.lower()
            .str.contains(
                search_value,
                regex=False,
                na=False
            )
        )

        financial_view = financial_view[
            mask
        ]


    # ============================================================
    # TABLE
    # ============================================================

    financial_display = financial_view[
        [
            "State",
            "Constituency",
            "Work ID",
            "Work",
            "Fund Disbursed Amount",
            "Expenditure",
            "State Median",
            "Above State Median %",
            "Payment Status",
            "Risk Level",
            "Reason"
        ]
    ].copy()


    financial_display[
        "Fund Disbursed Amount"
    ] = (
        financial_display[
            "Fund Disbursed Amount"
        ]
        .map(
            lambda x:
            f"₹{x:,.2f}"
            if pd.notna(x)
            else "Not Available"
        )
    )


    financial_display[
        "Expenditure"
    ] = (
        financial_display[
            "Expenditure"
        ]
        .map(
            lambda x:
            f"₹{x:,.2f}"
            if pd.notna(x)
            else "Not Available"
        )
    )


    financial_display[
        "State Median"
    ] = (
        financial_display[
            "State Median"
        ]
        .map(
            lambda x:
            f"₹{x:,.2f}"
            if pd.notna(x)
            else "Not Available"
        )
    )


    financial_display[
        "Above State Median %"
    ] = (
        financial_display[
            "Above State Median %"
        ]
        .map(
            lambda x:
            f"{x:.1f}%"
            if pd.notna(x)
            else "Not Available"
        )
    )


    st.write(
        f"Showing **{len(financial_display):,}** records"
    )

    st.dataframe(
        financial_display,
        width="stretch",
        height=500,
        hide_index=True
    )


    # ============================================================
    # INVESTIGATION VIEW
    # ============================================================

    st.divider()

    st.subheader(
        "🔍 Financial Investigation View"
    )

    if len(financial_view) > 0:

        selected_financial_index = st.selectbox(
            "Select a financial record",
            financial_view.index,
            format_func=lambda i:
                f"{financial_view.loc[i, 'Work ID']} — "
                f"{financial_view.loc[i, 'Risk Level']}",
            key="feature2_investigation"
        )

        record = financial_view.loc[
            selected_financial_index
        ]

        x1, x2, x3, x4 = st.columns(4)

        x1.metric(
            "Risk Level",
            record["Risk Level"]
        )

        if pd.notna(
            record["Fund Disbursed Amount"]
        ):

            x2.metric(
                "Fund Disbursed",
                f"₹{record['Fund Disbursed Amount']:,.2f}"
            )

        else:

            x2.metric(
                "Fund Disbursed",
                "Not Available"
            )

        if pd.notna(
            record["State Median"]
        ):

            x3.metric(
                "State Median",
                f"₹{record['State Median']:,.2f}"
            )

        else:

            x3.metric(
                "State Median",
                "Not Available"
            )

        if pd.notna(
            record["Above State Median %"]
        ):

            x4.metric(
                "Above State Median",
                f"{record['Above State Median %']:.1f}%"
            )

        else:

            x4.metric(
                "Above State Median",
                "Not Available"
            )


        st.info(
            f"**Assessment:** {record['Reason']}"
        )

        st.write(
            "**Payment Status:**",
            record["Payment Status"]
            if record["Payment Status"]
            else "Not Available"
        )

        st.write(
            "**Vendor:**",
            record["Vendor Name"]
            if record["Vendor Name"]
            else "Not Available"
        )

        if pd.notna(
            record["Expenditure"]
        ):

            st.write(
                "**Expenditure:**",
                f"₹{record['Expenditure']:,.2f}"
            )

        else:

            st.write(
                "**Expenditure:**",
                "Not Available in source data"
            )

    else:

        st.info(
            "No financial records match the selected filters."
        )


    # ============================================================
    # METHODOLOGY
    # ============================================================

    with st.expander(
        "📘 How Feature 2 Works"
    ):

        st.markdown(
            """
    ### What does this feature detect?

    Feature 2 identifies **unusual fund-disbursement patterns**
    that differ significantly from other works within the same
    State.

    ### Statistical method

    For each State:

    **Q1** = 25th percentile

    **Q3** = 75th percentile

    **IQR** = Q3 − Q1

    **Upper Fence** = Q3 + 1.5 × IQR

    A fund-disbursement amount above the upper fence is classified
    as a **High statistical anomaly indicator**.

    A value at least 50% above the state median, but not beyond
    the upper fence, is classified as **Medium**.

    ### Why State-level comparison?

    Project costs can naturally differ between States because of
    local conditions, material costs, geography and project mix.

    Therefore, comparing a work against its State-level peers is
    more meaningful than applying one national threshold.

    ### Important data limitation

    The downloaded **Expenditure** field contains masked values
    such as `*****`.

    Therefore:

    **`*****` ≠ ₹0**

    The system treats those values as **Unavailable**.

    Actual utilization percentage is calculated only when both
    Fund Disbursed Amount and Expenditure are available.

    ### Payment status

    Payment Status is displayed separately.

    A successful payment does not automatically mean the amount
    is normal, and a payment in progress does not automatically
    mean there is an anomaly.

    ### Important

    A statistical anomaly is **not proof of fraud**.

    It is a candidate for administrative review. Legitimate reasons
    such as project scope, location, materials, technical
    requirements or other circumstances may explain an unusual
    amount.
            """
        )


    # ============================================================
    # FOOTER
    # ============================================================

    st.divider()

    st.caption(
        "MPLADS AI Monitoring Platform • Feature 2 • "
        "Transparent financial anomaly indicator"
    )

    # ============================================================

def feature_3():
    # FEATURE 3 — UNUSUAL COST / PEER COST DEVIATION DETECTION

    # Feature 3 previously received financial_df from Feature 2.
    # In the final navigable portal each module must work independently,
    # so we prepare the small financial dataset locally here.
    F3_EXPENDITURE_FILE = DATA_DIR / "Expenditure on Completed and On-going Works as on Date.csv"

    @st.cache_data(show_spinner=False)
    def f3_load_financial_data():
        raw_f3 = pd.read_csv(F3_EXPENDITURE_FILE, low_memory=False)
        raw_f3.columns = raw_f3.columns.astype(str).str.strip()

        work_col_f3 = find_column(raw_f3, ["Work"])
        work_id_col_f3 = find_column(raw_f3, ["Work ID"])
        state_col_f3 = find_column(raw_f3, ["State"])
        constituency_col_f3 = find_column(raw_f3, ["Constituency"])
        fund_col_f3 = find_column(raw_f3, ["Fund Disbursed Amount"])

        financial_f3 = pd.DataFrame(index=raw_f3.index)
        financial_f3["Work"] = (
            raw_f3[work_col_f3].fillna("").astype(str).str.strip()
            if work_col_f3 else ""
        )
        financial_f3["State"] = (
            raw_f3[state_col_f3].fillna("").astype(str).str.strip()
            if state_col_f3 else "Not Available"
        )
        financial_f3["Constituency"] = (
            raw_f3[constituency_col_f3].fillna("").astype(str).str.strip()
            if constituency_col_f3 else "Not Available"
        )

        def f3_extract_work_id(value):
            text = str(value).strip()
            match = re.match(r"^(WS/[^/]+/\d{4}-\d{4}/\d+)(?:-|$)", text, flags=re.IGNORECASE)
            return match.group(1).strip() if match else ""

        # Prefer the authoritative Work ID column when the source provides it.
        # Fall back to the embedded ID inside the Work text for older snapshots.
        if work_id_col_f3:
            financial_f3["Work ID"] = (
                raw_f3[work_id_col_f3]
                .fillna("")
                .astype(str)
                .str.strip()
            )
            missing_id = financial_f3["Work ID"].eq("") | financial_f3["Work ID"].isin(["nan", "None"])
            if missing_id.any():
                financial_f3.loc[missing_id, "Work ID"] = financial_f3.loc[missing_id, "Work"].apply(f3_extract_work_id)
        else:
            financial_f3["Work ID"] = financial_f3["Work"].apply(f3_extract_work_id)

        if fund_col_f3:
            financial_f3["Fund Disbursed Amount"] = pd.to_numeric(
                raw_f3[fund_col_f3].astype(str)
                .str.replace("₹", "", regex=False)
                .str.replace(",", "", regex=False)
                .str.strip()
                .replace(["", "*****", "nan", "None", "none", "null", "N/A", "n/a"], np.nan),
                errors="coerce"
            )
        else:
            financial_f3["Fund Disbursed Amount"] = np.nan

        return financial_f3

    financial_df = f3_load_financial_data()
    # FAST + PRESENTATION READY
    # ============================================================


    # ============================================================
    # WORK TYPE CLASSIFICATION
    # ============================================================

    def classify_work_type(series):

        text = (
            series
            .fillna("")
            .astype(str)
            .str.lower()
        )

        result = pd.Series(
            "Other",
            index=series.index
        )

        # Roads / transport
        road_mask = text.str.contains(
            "road|street|bridge|culvert|pathway|transport|"
            "pcc|bitumen|construction of link road|"
            "drain",
            regex=True,
            na=False
        )

        result.loc[road_mask] = "Road / Transport"

        # Education
        education_mask = text.str.contains(
            "school|classroom|college|education|"
            "laboratory|library|smart class",
            regex=True,
            na=False
        )

        result.loc[education_mask] = "Education"

        # Health
        health_mask = text.str.contains(
            "hospital|health|clinic|dispensary|"
            "medical|ambulance|health centre",
            regex=True,
            na=False
        )

        result.loc[health_mask] = "Health"

        # Water
        water_mask = text.str.contains(
            "water|tank|pipeline|drinking water|"
            "borewell|tanker|harvesting",
            regex=True,
            na=False
        )

        result.loc[water_mask] = "Water"

        # Lighting
        lighting_mask = text.str.contains(
            "street light|solar light|led light|"
            "lighting|high mast|lamp",
            regex=True,
            na=False
        )

        result.loc[lighting_mask] = "Lighting"

        # Community buildings
        community_mask = text.str.contains(
            "community hall|community centre|"
            "panchayat|anganwadi|public hall|"
            "multipurpose hall",
            regex=True,
            na=False
        )

        result.loc[community_mask] = "Community Infrastructure"

        # Sports
        sports_mask = text.str.contains(
            "sports|stadium|playground|"
            "gymnasium|football ground|"
            "cricket ground",
            regex=True,
            na=False
        )

        result.loc[sports_mask] = "Sports"

        # Sanitation
        sanitation_mask = text.str.contains(
            "toilet|sanitation|sewerage|"
            "waste management|solid waste",
            regex=True,
            na=False
        )

        result.loc[sanitation_mask] = "Sanitation"

        # Agriculture
        agriculture_mask = text.str.contains(
            "agriculture|irrigation|"
            "farm|farming|agricultural",
            regex=True,
            na=False
        )

        result.loc[agriculture_mask] = "Agriculture"

        return result


    # ============================================================
    # PREPARE FEATURE 3 — CACHED
    # ============================================================

    @st.cache_data(show_spinner=False)
    def prepare_feature3(financial_data):

        df = financial_data.copy()

        # --------------------------------------------------------
        # WORK TYPE
        # --------------------------------------------------------

        df["Work Type"] = classify_work_type(
            df["Work"]
        )

        # --------------------------------------------------------
        # ONLY RECORDS WITH USABLE FUND AMOUNT
        # --------------------------------------------------------

        usable = df[
            df["Fund Disbursed Amount"].notna()
            &
            (df["Fund Disbursed Amount"] >= 0)
        ].copy()

        if len(usable) == 0:

            df["Peer Median"] = np.nan
            df["Peer Q1"] = np.nan
            df["Peer Q3"] = np.nan
            df["Peer Upper Fence"] = np.nan
            df["Peer Records"] = 0
            df["Above Peer Median %"] = np.nan
            df["Cost Risk"] = "Insufficient Data"
            df["Cost Reason"] = (
                "Fund disbursed amount unavailable."
            )

            return df

        # --------------------------------------------------------
        # PEER GROUP
        # --------------------------------------------------------
        #
        # State + Work Type
        #
        # Example:
        #
        # Maharashtra + Road / Transport
        # Uttar Pradesh + Education
        #
        # This avoids comparing completely different projects.
        # --------------------------------------------------------

        group_cols = [
            "State",
            "Work Type"
        ]

        grouped = (
            usable
            .groupby(group_cols)["Fund Disbursed Amount"]
        )

        # --------------------------------------------------------
        # PEER STATISTICS
        # --------------------------------------------------------

        peer_median = grouped.transform(
            "median"
        )

        peer_q1 = grouped.transform(
            "quantile",
            0.25
        )

        peer_q3 = grouped.transform(
            "quantile",
            0.75
        )

        peer_count = grouped.transform(
            "count"
        )

        peer_iqr = (
            peer_q3 -
            peer_q1
        )

        peer_upper = (
            peer_q3 +
            (1.5 * peer_iqr)
        )

        # --------------------------------------------------------
        # ADD STATISTICS
        # --------------------------------------------------------

        df["Peer Median"] = np.nan
        df["Peer Q1"] = np.nan
        df["Peer Q3"] = np.nan
        df["Peer Upper Fence"] = np.nan
        df["Peer Records"] = 0

        df.loc[
            usable.index,
            "Peer Median"
        ] = peer_median.values

        df.loc[
            usable.index,
            "Peer Q1"
        ] = peer_q1.values

        df.loc[
            usable.index,
            "Peer Q3"
        ] = peer_q3.values

        df.loc[
            usable.index,
            "Peer Upper Fence"
        ] = peer_upper.values

        df.loc[
            usable.index,
            "Peer Records"
        ] = peer_count.values

        # --------------------------------------------------------
        # ABOVE PEER MEDIAN %
        # --------------------------------------------------------

        df["Above Peer Median %"] = np.nan

        valid_median = (
            df["Fund Disbursed Amount"].notna()
            &
            df["Peer Median"].notna()
            &
            (df["Peer Median"] > 0)
        )

        df.loc[
            valid_median,
            "Above Peer Median %"
        ] = (
            (
                df.loc[
                    valid_median,
                    "Fund Disbursed Amount"
                ]
                -
                df.loc[
                    valid_median,
                    "Peer Median"
                ]
            )
            /
            df.loc[
                valid_median,
                "Peer Median"
            ]
            * 100
        )

        # --------------------------------------------------------
        # IMPORTANT:
        # Require at least 5 peer records
        # --------------------------------------------------------

        enough_peers = (
            df["Peer Records"] >= 5
        )

        # --------------------------------------------------------
        # HIGH = STATISTICAL OUTLIER
        # --------------------------------------------------------

        high = (
            df["Fund Disbursed Amount"].notna()
            &
            enough_peers
            &
            df["Peer Upper Fence"].notna()
            &
            (
                df["Fund Disbursed Amount"]
                >
                df["Peer Upper Fence"]
            )
        )

        # --------------------------------------------------------
        # MEDIUM = 40%+ ABOVE PEER MEDIAN
        # --------------------------------------------------------

        medium = (
            df["Fund Disbursed Amount"].notna()
            &
            enough_peers
            &
            df["Peer Median"].notna()
            &
            (df["Peer Median"] > 0)
            &
            (
                df["Above Peer Median %"] >= 40
            )
            &
            ~high
        )

        # --------------------------------------------------------
        # RISK
        # --------------------------------------------------------

        df["Cost Risk"] = "Insufficient Data"

        # Not enough peers
        not_enough_peers = (
            df["Fund Disbursed Amount"].notna()
            &
            ~enough_peers
        )

        df.loc[
            not_enough_peers,
            "Cost Risk"
        ] = "Insufficient Peer Data"

        # Normal
        normal = (
            df["Fund Disbursed Amount"].notna()
            &
            enough_peers
            &
            ~medium
            &
            ~high
        )

        df.loc[
            normal,
            "Cost Risk"
        ] = "Normal"

        # Medium
        df.loc[
            medium,
            "Cost Risk"
        ] = "Medium"

        # High
        df.loc[
            high,
            "Cost Risk"
        ] = "High"

        # --------------------------------------------------------
        # REASONS
        # --------------------------------------------------------

        df["Cost Reason"] = (
            "Fund amount unavailable."
        )

        df.loc[
            not_enough_peers,
            "Cost Reason"
        ] = (
            "Not enough comparable peer works "
            "for a reliable comparison."
        )

        df.loc[
            normal,
            "Cost Reason"
        ] = (
            "Amount is within the observed "
            "peer range."
        )

        df.loc[
            medium,
            "Cost Reason"
        ] = (
            "Amount is substantially above "
            "the peer median."
        )

        df.loc[
            high,
            "Cost Reason"
        ] = (
            "Amount is an extreme statistical "
            "outlier among peer works."
        )

        return df


    # ============================================================
    # FEATURE 3 HEADER
    # ============================================================

    st.divider()

    st.title(
        "📈 Cost Deviation & Peer Analysis"
    )

    st.caption(
        "Identifies works whose fund-disbursed amounts differ "
        "substantially from comparable works in the same State "
        "and Work Type."
    )


    # ============================================================
    # PROCESS
    # ============================================================

    try:

        cost_df = prepare_feature3(
            financial_df
        )

        # Defensive schema guarantee for the supplied snapshot.
        if "Constituency" not in cost_df.columns:
            cost_df["Constituency"] = "Not Available"
        if "Work ID" not in cost_df.columns:
            def _safe_work_id(value):
                text = str(value).strip()
                m = re.match(r"^(WS/[^/]+/\d{4}-\d{4}/\d+)-", text, flags=re.IGNORECASE)
                return m.group(1) if m else ""
            cost_df["Work ID"] = cost_df["Work"].apply(_safe_work_id) if "Work" in cost_df.columns else ""

    except Exception as e:

        st.error(
            "❌ Unable to calculate peer-based cost indicators."
        )

        st.exception(e)

        st.stop()


    # ============================================================
    # KPI COUNTS
    # ============================================================

    cost_total = len(cost_df)

    cost_high = int(
        (
            cost_df["Cost Risk"] ==
            "High"
        ).sum()
    )

    cost_medium = int(
        (
            cost_df["Cost Risk"] ==
            "Medium"
        ).sum()
    )

    cost_normal = int(
        (
            cost_df["Cost Risk"] ==
            "Normal"
        ).sum()
    )

    cost_insufficient = int(
        (
            cost_df["Cost Risk"] ==
            "Insufficient Data"
        ).sum()
    )

    cost_peer_insufficient = int(
        (
            cost_df["Cost Risk"] ==
            "Insufficient Peer Data"
        ).sum()
    )


    # ============================================================
    # KPI SECTION
    # ============================================================

    st.subheader(
        "📊 Cost Monitoring Overview"
    )

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Records Analyzed",
        f"{cost_total:,}"
    )

    c2.metric(
        "High",
        f"{cost_high:,}"
    )

    c3.metric(
        "Medium",
        f"{cost_medium:,}"
    )

    c4.metric(
        "Normal",
        f"{cost_normal:,}"
    )

    c5.metric(
        "Insufficient Peer Data",
        f"{cost_peer_insufficient:,}"
    )


    # ============================================================
    # GRAPH
    # ============================================================

    st.subheader(
        "📈 Cost Deviation Distribution"
    )

    cost_chart = pd.DataFrame(
        {
            "Risk Level": [
                "High",
                "Medium",
                "Normal",
                "Insufficient Peer Data",
                "Insufficient Data"
            ],
            "Records": [
                cost_high,
                cost_medium,
                cost_normal,
                cost_peer_insufficient,
                cost_insufficient
            ]
        }
    )

    st.bar_chart(
        cost_chart.set_index(
            "Risk Level"
        ),
        width="stretch"
    )


    # ============================================================
    # SUMMARY
    # ============================================================

    cost_attention = (
        cost_high +
        cost_medium
    )

    s1, s2, s3 = st.columns(3)

    with s1:

        st.error(
            f"🔴 **{cost_high:,}** works are "
            "statistical cost outlier candidates."
        )

    with s2:

        st.warning(
            f"🟡 **{cost_medium:,}** works are "
            "substantially above their peer median."
        )

    with s3:

        st.info(
            f"📌 **{cost_attention:,}** works "
            "require closer cost review."
        )


    # ============================================================
    # FILTERS
    # ============================================================

    st.divider()

    st.subheader(
        "🔎 Cost Monitoring"
    )

    f1, f2, f3, f4 = st.columns(4)

    cost_states = sorted(
        [
            x
            for x in cost_df["State"].unique()
            if x
        ]
    )

    work_types = sorted(
        [
            x
            for x in cost_df["Work Type"].unique()
            if x
        ]
    )

    with f1:

        selected_cost_state = st.selectbox(
            "State",
            ["All States"] +
            cost_states,
            key="feature3_state"
        )

    with f2:

        selected_work_type = st.selectbox(
            "Work Type",
            ["All Work Types"] +
            work_types,
            key="feature3_work_type"
        )

    with f3:

        selected_cost_risk = st.selectbox(
            "Cost Risk",
            [
                "All Risk Levels",
                "High",
                "Medium",
                "Normal",
                "Insufficient Peer Data",
                "Insufficient Data"
            ],
            key="feature3_risk"
        )

    with f4:

        cost_search = st.text_input(
            "Search Work / ID",
            placeholder="Enter work or ID...",
            key="feature3_search"
        )


    # ============================================================
    # APPLY FILTERS
    # ============================================================

    cost_view = cost_df

    if selected_cost_state != "All States":

        cost_view = cost_view[
            cost_view["State"] ==
            selected_cost_state
        ]

    if selected_work_type != "All Work Types":

        cost_view = cost_view[
            cost_view["Work Type"] ==
            selected_work_type
        ]

    if selected_cost_risk != "All Risk Levels":

        cost_view = cost_view[
            cost_view["Cost Risk"] ==
            selected_cost_risk
        ]

    if cost_search.strip():

        search_value = (
            cost_search
            .strip()
            .lower()
        )

        mask = (
            cost_view["Work"]
            .str.lower()
            .str.contains(
                search_value,
                regex=False,
                na=False
            )
            |
            cost_view["Work ID"]
            .str.lower()
            .str.contains(
                search_value,
                regex=False,
                na=False
            )
        )

        cost_view = cost_view[
            mask
        ]


    # ============================================================
    # DISPLAY TABLE
    # ============================================================

    cost_display = cost_view[
        [
            "State",
            "Constituency",
            "Work ID",
            "Work",
            "Work Type",
            "Fund Disbursed Amount",
            "Peer Median",
            "Above Peer Median %",
            "Peer Records",
            "Cost Risk",
            "Cost Reason"
        ]
    ].copy()


    # ------------------------------------------------------------
    # FORMAT MONEY
    # ------------------------------------------------------------

    for col in [
        "Fund Disbursed Amount",
        "Peer Median"
    ]:

        cost_display[col] = (
            cost_display[col]
            .map(
                lambda x:
                f"₹{x:,.2f}"
                if pd.notna(x)
                else "Not Available"
            )
        )


    # ------------------------------------------------------------
    # FORMAT DEVIATION
    # ------------------------------------------------------------

    cost_display[
        "Above Peer Median %"
    ] = (
        cost_display[
            "Above Peer Median %"
        ]
        .map(
            lambda x:
            f"{x:.1f}%"
            if pd.notna(x)
            else "Not Available"
        )
    )


    st.write(
        f"Showing **{len(cost_display):,}** records"
    )

    st.dataframe(
        cost_display,
        width="stretch",
        height=500,
        hide_index=True
    )


    # ============================================================
    # INVESTIGATION VIEW
    # ============================================================

    st.divider()

    st.subheader(
        "🔍 Cost Investigation View"
    )

    if len(cost_view) > 0:

        def cost_investigation_label(i):
            row = cost_view.loc[i]
            work_id = str(row.get("Work ID", "")).strip()
            work_type = str(row.get("Work Type", "")).strip()
            work_desc = str(row.get("Work", "")).strip()
            risk = str(row.get("Cost Risk", "")).strip()

            if not work_id or work_id.lower() in {"nan", "none"}:
                work_id = "Work ID unavailable"
            if not work_type or work_type.lower() in {"nan", "none"}:
                work_type = "Work type unavailable"
            if not work_desc or work_desc.lower() in {"nan", "none"}:
                work_desc = "Work description unavailable"

            # Keep the selector readable while still giving the reviewer enough
            # context to know exactly which record is being investigated.
            if len(work_desc) > 72:
                work_desc = work_desc[:69].rstrip() + "..."

            return f"{work_id}  |  {work_type}  |  {work_desc}  |  {risk}"

        selected_cost_index = st.selectbox(
            "Select a work",
            cost_view.index,
            format_func=cost_investigation_label,
            key="feature3_investigation"
        )

        record = cost_view.loc[
            selected_cost_index
        ]

        x1, x2, x3, x4 = st.columns(4)

        x1.metric(
            "Cost Risk",
            record["Cost Risk"]
        )

        if pd.notna(
            record["Fund Disbursed Amount"]
        ):

            x2.metric(
                "Fund Disbursed",
                f"₹{record['Fund Disbursed Amount']:,.2f}"
            )

        else:

            x2.metric(
                "Fund Disbursed",
                "Not Available"
            )

        if pd.notna(
            record["Peer Median"]
        ):

            x3.metric(
                "Peer Median",
                f"₹{record['Peer Median']:,.2f}"
            )

        else:

            x3.metric(
                "Peer Median",
                "Not Available"
            )

        if pd.notna(
            record["Above Peer Median %"]
        ):

            x4.metric(
                "Above Peer Median",
                f"{record['Above Peer Median %']:.1f}%"
            )

        else:

            x4.metric(
                "Above Peer Median",
                "Not Available"
            )


        st.info(
            f"**Assessment:** "
            f"{record['Cost Reason']}"
        )

        st.write(
            "**State:**",
            record["State"]
            if record["State"]
            else "Not Available"
        )

        st.write(
            "**Work Type:**",
            record["Work Type"]
        )

        st.write(
            "**Peer Records:**",
            int(record["Peer Records"])
        )

        st.write(
            "**Work:**",
            record["Work"]
            if record["Work"]
            else "Not Available"
        )


        # --------------------------------------------------------
        # REVIEW GUIDANCE
        # --------------------------------------------------------

        if record["Cost Risk"] in [
            "High",
            "Medium"
        ]:

            st.warning(
                "⚠️ This is a statistical cost-deviation "
                "indicator. Administrative review may consider "
                "project scope, location, technical requirements, "
                "materials, estimates and other supporting records."
            )

    else:

        st.info(
            "No works match the selected filters."
        )


    # ============================================================
    # METHODOLOGY
    # ============================================================

    with st.expander(
        "📘 How Feature 3 Works"
    ):

        st.markdown(
            """
    ### What does this feature detect?

    Feature 3 identifies **unusual fund-disbursement amounts**
    relative to comparable peer works.

    It does **not** attempt to determine the market price of a
    project because market-price information is not available in
    the supplied dataset.

    ### Peer comparison

    Works are grouped by:

    **State + Work Type**

    Examples:

    - Maharashtra + Road / Transport
    - Uttar Pradesh + Education
    - Bihar + Water

    For each peer group, the system calculates:

    **Peer Median**

    **Q1**

    **Q3**

    **IQR = Q3 − Q1**

    **Upper Fence = Q3 + 1.5 × IQR**

    ### Risk classification

    🔴 **High**

    Amount is above the statistical upper fence.

    🟡 **Medium**

    Amount is at least 40% above the peer median but is not
    beyond the statistical upper fence.

    🟢 **Normal**

    Amount is within the observed peer pattern.

    ⚪ **Insufficient Peer Data**

    Fewer than 5 comparable peer records are available.

    ### Why this is useful

    A project that costs substantially more than similar works
    may deserve additional review.

    However, higher cost can be completely legitimate because of:

    - project size
    - location
    - material costs
    - technical requirements
    - site conditions
    - scope differences

    Therefore, this feature produces a **cost deviation indicator**,
    not a finding of fraud, overpricing or wrongdoing.

    ### Data limitation

    Work Type is assigned using transparent keyword-based
    classification of the available work text. It is therefore a
    peer-grouping heuristic rather than an official project
    classification.
            """
        )


    # ============================================================
    # FOOTER
    # ============================================================

    st.divider()

    st.caption(
        "MPLADS AI Monitoring Platform • Feature 3 • "
        "Peer-based cost deviation indicator"
    )


    # ============================================================

def feature_4():
    # FEATURE 4 — DUPLICATE & HIGH-SIMILARITY WORK DETECTION
    # ============================================================

    import re
    import pandas as pd
    import streamlit as st
    from pathlib import Path
    from rapidfuzz import process, fuzz


    # ============================================================
    # FILES
    # ============================================================

    F4_FILE = Path(DATA_DIR) / "Works Sanctioned (1).csv"
    F4_CACHE_FILE = Path(DATA_DIR) / "f4_high_similarity_cache.csv"


    # ============================================================
    # HELPERS
    # ============================================================

    def f4_find_col(df, names):
        for name in names:
            for col in df.columns:
                if str(col).strip().lower() == name.strip().lower():
                    return col
        return None


    def f4_clean(value):

        if pd.isna(value):
            return ""

        text = str(value).strip()

        if "??" in text:
            return ""

        return re.sub(r"\s+", " ", text)


    def f4_extract_work(value):

        text = f4_clean(value)

        if not text:
            return "", ""

        match = re.match(
            r"^(WS/.+/\d+)\s*[-–—]\s*(.+)$",
            text,
            flags=re.IGNORECASE
        )

        if match:
            return (
                match.group(1).strip(),
                match.group(2).strip()
            )

        return text, ""


    def f4_normalize(text):

        text = f4_clean(text).lower()

        if not text:
            return ""

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        ).strip()

        return text


    def f4_words(text):

        stop_words = {
            "the",
            "and",
            "of",
            "for",
            "at",
            "in",
            "to",
            "a",
            "an",
            "work",
            "construction",
            "providing",
            "supply",
            "installation",
            "development"
        }

        return {
            word
            for word in f4_normalize(text).split()
            if len(word) > 1
            and word not in stop_words
        }


    def f4_strength(score):

        if score >= 98:
            return "Extremely High"

        if score >= 95:
            return "Very High"

        return "High"


    def f4_similarity(a, b):

        a = f4_normalize(a)
        b = f4_normalize(b)

        if not a or not b:
            return 0.0

        if a == b:
            return 100.0

        char_score = fuzz.ratio(
            a,
            b
        )

        words_a = f4_words(a)
        words_b = f4_words(b)

        if words_a or words_b:

            word_score = (
                len(words_a & words_b)
                /
                len(words_a | words_b)
            ) * 100

        else:

            word_score = 0

        score = (
            0.60 * char_score
            +
            0.40 * word_score
        )

        return min(
            round(score, 1),
            99.9
        )


    # ============================================================
    # LOAD SANCTIONED DATA
    # ============================================================

    @st.cache_data(show_spinner=False)
    def f4_load_data():

        df = pd.read_csv(
            F4_FILE,
            low_memory=False
        )

        state_col = f4_find_col(
            df,
            ["State"]
        )

        constituency_col = f4_find_col(
            df,
            ["Constituency"]
        )

        category_col = f4_find_col(
            df,
            ["Work Category"]
        )

        work_col = f4_find_col(
            df,
            ["Work"]
        )

        description_col = f4_find_col(
            df,
            ["Work Description"]
        )

        mp_col = f4_find_col(
            df,
            [
                "Hon'ble Member",
                "Hon’ble Member",
                "Hon'ble Members of Parliament"
            ]
        )

        sanction_col = f4_find_col(
            df,
            ["Sanction Date"]
        )

        status_col = f4_find_col(
            df,
            ["Work Status"]
        )

        result = pd.DataFrame()

        # State
        result["State"] = (
            df[state_col]
            .fillna("")
            .astype(str)
            .str.strip()
            if state_col else ""
        )

        # Constituency
        result["Constituency"] = (
            df[constituency_col]
            .fillna("")
            .astype(str)
            .str.strip()
            if constituency_col else ""
        )

        # Work Category
        result["Work Category"] = (
            df[category_col]
            .fillna("")
            .astype(str)
            .str.strip()
            if category_col else ""
        )

        # Work ID + fallback description
        if work_col:

            extracted = df[work_col].apply(
                f4_extract_work
            )

            result["Work ID"] = extracted.apply(
                lambda x: x[0]
            )

            fallback_description = extracted.apply(
                lambda x: x[1]
            )

        else:

            result["Work ID"] = ""
            fallback_description = ""

        # Description
        if description_col:

            explicit_description = (
                df[description_col]
                .apply(f4_clean)
            )

            result["Description"] = (
                explicit_description
                .where(
                    explicit_description.str.len() > 0,
                    fallback_description
                )
            )

        else:

            result["Description"] = fallback_description

        # MP
        result["MP"] = (
            df[mp_col]
            .fillna("")
            .astype(str)
            .str.strip()
            if mp_col else ""
        )

        # Sanction Date
        result["Sanction Date"] = (
            df[sanction_col]
            .fillna("")
            .astype(str)
            .str.strip()
            if sanction_col else ""
        )

        # Status
        result["Work Status"] = (
            df[status_col]
            .fillna("")
            .astype(str)
            .str.strip()
            if status_col else ""
        )

        # Normalized description
        result["Normalized"] = (
            result["Description"]
            .apply(f4_normalize)
        )

        # Remove corrupted / empty descriptions
        result = result[
            result["Normalized"].str.len() > 0
        ].copy()

        return result.reset_index(drop=True)


    df4 = f4_load_data()


    # ============================================================
    # HEADER
    # ============================================================

    st.markdown(
        "## 🔁 Duplicate & Similar Work Detection"
    )

    st.caption(
        "AI-assisted NLP screening for duplicate and highly similar "
        "sanctioned works."
    )


    # ============================================================
    # EXACT DESCRIPTION MATCHES
    # ============================================================

    st.markdown(
        "### 1. Exact Description Matches"
    )


    exact = (
        df4
        .groupby(
            [
                "State",
                "Constituency",
                "Work Category",
                "Normalized"
            ],
            dropna=False
        )
        .agg(
            Works=("Work ID", "count"),
            Description=("Description", "first")
        )
        .reset_index()
    )


    exact = exact[
        exact["Works"] >= 2
    ].copy()


    if exact.empty:

        st.info(
            "No exact description-match groups found."
        )

    else:

        exact.insert(
            0,
            "Group",
            [
                f"DG-{i + 1:04d}"
                for i in range(len(exact))
            ]
        )

        st.dataframe(
            exact[
                [
                    "Group",
                    "State",
                    "Constituency",
                    "Work Category",
                    "Description",
                    "Works"
                ]
            ],
            width="stretch",
            hide_index=True
        )


        selected_group = st.selectbox(
            "Inspect a matching group",
            exact["Group"].tolist(),
            key="f4_exact_group"
        )


        selected = exact[
            exact["Group"] == selected_group
        ].iloc[0]


        members = df4[
            (df4["State"] == selected["State"])
            &
            (df4["Constituency"] == selected["Constituency"])
            &
            (df4["Work Category"] == selected["Work Category"])
            &
            (df4["Normalized"] == selected["Normalized"])
        ].copy()


        st.markdown(
            "#### Works in Selected Group"
        )


        st.dataframe(
            members[
                [
                    "Work ID",
                    "MP",
                    "State",
                    "Constituency",
                    "Work Category",
                    "Description",
                    "Sanction Date",
                    "Work Status"
                ]
            ],
            width="stretch",
            hide_index=True
        )


    # ============================================================
    # HIGH-SIMILARITY CACHE
    # ============================================================

    def f4_create_cache():

        # If cache already exists, DON'T calculate again
        if F4_CACHE_FILE.exists():

            try:

                cached = pd.read_csv(
                    F4_CACHE_FILE,
                    low_memory=False
                )

                if not cached.empty:
                    return cached

            except Exception:
                pass


        # --------------------------------------------------------
        # First-time preparation
        # --------------------------------------------------------

        rows = df4[
            [
                "State",
                "Constituency",
                "Work Category",
                "Work ID",
                "Description",
                "MP",
                "Normalized"
            ]
        ].to_dict("records")


        results = []

        # Process constituency by constituency
        grouped = df4.groupby(
            [
                "State",
                "Constituency"
            ],
            sort=False
        )


        for (state, constituency), group in grouped:

            group = group.reset_index(drop=True)

            if len(group) < 2:
                continue


            # Unique descriptions
            descriptions = (
                group["Normalized"]
                .dropna()
                .unique()
                .tolist()
            )


            if len(descriptions) < 2:
                continue


            # ----------------------------------------------------
            # RapidFuzz directly finds 92%+ matches
            # ----------------------------------------------------

            for query in descriptions:

                matches = process.extract(
                    query,
                    descriptions,
                    scorer=fuzz.ratio,
                    score_cutoff=92,
                    limit=10
                )


                for matched, raw_score, _ in matches:

                    if query == matched:
                        continue


                    score = f4_similarity(
                        query,
                        matched
                    )


                    if score < 92:
                        continue


                    # Prevent duplicate A/B combinations
                    pair = tuple(
                        sorted(
                            [
                                query,
                                matched
                            ]
                        )
                    )


                    results.append(
                        (
                            state,
                            constituency,
                            pair[0],
                            pair[1],
                            score
                        )
                    )


        # --------------------------------------------------------
        # Remove duplicate pairs
        # --------------------------------------------------------

        unique_pairs = {}

        for (
            state,
            constituency,
            desc_a,
            desc_b,
            score
        ) in results:

            key = (
                state,
                constituency,
                desc_a,
                desc_b
            )

            if key not in unique_pairs:

                unique_pairs[key] = score

            else:

                unique_pairs[key] = max(
                    unique_pairs[key],
                    score
                )


        final = []


        # --------------------------------------------------------
        # Map descriptions back to actual works
        # --------------------------------------------------------

        for (
            state,
            constituency,
            desc_a,
            desc_b
        ), score in unique_pairs.items():

            group_a = df4[
                (df4["State"] == state)
                &
                (df4["Constituency"] == constituency)
                &
                (df4["Normalized"] == desc_a)
            ]


            group_b = df4[
                (df4["State"] == state)
                &
                (df4["Constituency"] == constituency)
                &
                (df4["Normalized"] == desc_b)
            ]


            if group_a.empty or group_b.empty:
                continue


            a = group_a.iloc[0]
            b = group_b.iloc[0]


            final.append(
                {
                    "State": state,
                    "Constituency": constituency,
                    "Work Category": a["Work Category"],
                    "Work ID A": a["Work ID"],
                    "Description A": a["Description"],
                    "MP A": a["MP"],
                    "Work ID B": b["Work ID"],
                    "Description B": b["Description"],
                    "MP B": b["MP"],
                    "Similarity": score,
                    "Match Strength": f4_strength(score)
                }
            )


        final_df = pd.DataFrame(final)


        # --------------------------------------------------------
        # SAVE CACHE
        # --------------------------------------------------------

        if not final_df.empty:

            final_df.to_csv(
                F4_CACHE_FILE,
                index=False
            )


        return final_df


    # ============================================================
    # LOAD PRECOMPUTED RESULTS
    # ============================================================

    similar_df = f4_create_cache()


    # ============================================================
    # HIGH-SIMILARITY CANDIDATES
    # ============================================================

    st.markdown(
        "### 2. High-Similarity Work Candidates"
    )


    search_text = st.text_input(
        "🔎 Search high-similarity candidates",
        placeholder=(
            "Search by Work ID, description, State, "
            "Constituency or Work Category..."
        ),
        key="f4_high_similarity_search"
    )


    results = similar_df.copy()


    # ============================================================
    # SEARCH
    # ============================================================

    if search_text.strip():

        query = search_text.strip().lower()

        searchable_columns = [
            "State",
            "Constituency",
            "Work Category",
            "Work ID A",
            "Description A",
            "MP A",
            "Work ID B",
            "Description B",
            "MP B"
        ]

        mask = pd.Series(
            False,
            index=results.index
        )

        for col in searchable_columns:

            mask = mask | (
                results[col]
                .astype(str)
                .str.lower()
                .str.contains(
                    query,
                    regex=False,
                    na=False
                )
            )

        results = results[
            mask
        ].copy()


    # ============================================================
    # DISPLAY
    # ============================================================

    if results.empty:

        if search_text.strip():

            st.info(
                f"No high-similarity candidates found for "
                f"'{search_text}'."
            )

        else:

            st.info(
                "No high-similarity work candidates found."
            )

    else:

        st.dataframe(
            results[
                [
                    "State",
                    "Constituency",
                    "Work Category",
                    "Work ID A",
                    "Description A",
                    "Work ID B",
                    "Description B",
                    "Similarity",
                    "Match Strength"
                ]
            ],
            width="stretch",
            hide_index=True
        )


    # ============================================================
    # HOW IT WORKS
    # ============================================================

    with st.expander(
        "How this feature works"
    ):

        st.markdown(
            """
    ### NLP-based high-similarity screening

    The system:

    - Cleans and normalizes sanctioned work descriptions.
    - Identifies exact description matches.
    - Uses NLP-style RapidFuzz text matching for similar descriptions.
    - Restricts comparison to the **same State and Constituency**.
    - Displays only **92%+ similarity** cases.

    A high similarity score is a screening indicator only. It does not establish
    physical duplication or wrongdoing. Administrative verification should
    consider actual locations, beneficiaries, supporting records and other evidence.
    """
        )


    st.caption(
        "Duplicate & Similar Work Detection • "
        "AI-assisted NLP screening • Decision support"
    )


    # ============================================================

def feature_5():
    # FEATURE 5 — PAYMENT & VENDOR ANOMALY DETECTION
    # ============================================================

    import pandas as pd
    import numpy as np
    import streamlit as st
    from pathlib import Path


    # ============================================================
    # FILE
    # ============================================================

    F5_FILE = Path(DATA_DIR) / (
        "Expenditure on Completed and On-going Works as on Date.csv"
    )


    # ============================================================
    # HELPERS
    # ============================================================

    def f5_find_col(df, names):

        for name in names:

            for col in df.columns:

                if str(col).strip().lower() == name.strip().lower():
                    return col

        return None


    def f5_clean(value):

        if pd.isna(value):
            return ""

        text = str(value).strip()

        if text in ["", "nan", "None", "*****", "????", "???"]:
            return ""

        if "??" in text:
            return ""

        return text


    def f5_amount(value):

        text = f5_clean(value)

        if not text:
            return np.nan

        # Remove currency symbols, commas and spaces
        text = (
            text.replace("₹", "")
            .replace(",", "")
            .replace(" ", "")
        )

        try:
            return float(text)
        except:
            return np.nan


    # ============================================================
    # LOAD DATA
    # ============================================================

    @st.cache_data(show_spinner=False)
    def f5_load_data():

        df = pd.read_csv(
            F5_FILE,
            low_memory=False
        )

        state_col = f5_find_col(
            df,
            ["State"]
        )

        work_col = f5_find_col(
            df,
            ["Work"]
        )

        work_id_col = f5_find_col(
            df,
            ["Work ID"]
        )

        mp_col = f5_find_col(
            df,
            [
                "Hon'ble Member",
                "Hon’ble Member"
            ]
        )

        constituency_col = f5_find_col(
            df,
            ["Constituency"]
        )

        expenditure_col = f5_find_col(
            df,
            ["Expenditure"]
        )

        vendor_col = f5_find_col(
            df,
            ["Vendor Name"]
        )

        payment_col = f5_find_col(
            df,
            ["Payment Status"]
        )

        fund_col = f5_find_col(
            df,
            ["Fund Disbursed Amount"]
        )


        result = pd.DataFrame()

        # --------------------------------------------------------
        # Basic fields
        # --------------------------------------------------------

        result["State"] = (
            df[state_col]
            .apply(f5_clean)
            if state_col else ""
        )

        result["Work ID"] = (
            df[work_id_col]
            .apply(f5_clean)
            if work_id_col else ""
        )

        result["Work"] = (
            df[work_col]
            .apply(f5_clean)
            if work_col else ""
        )

        result["MP"] = (
            df[mp_col]
            .apply(f5_clean)
            if mp_col else ""
        )

        result["Constituency"] = (
            df[constituency_col]
            .apply(f5_clean)
            if constituency_col else ""
        )

        result["Vendor Name"] = (
            df[vendor_col]
            .apply(f5_clean)
            if vendor_col else ""
        )

        result["Payment Status"] = (
            df[payment_col]
            .apply(f5_clean)
            if payment_col else ""
        )

        # --------------------------------------------------------
        # Financial fields
        # --------------------------------------------------------

        result["Expenditure Amount"] = (
            df[expenditure_col]
            .apply(f5_amount)
            if expenditure_col else np.nan
        )

        result["Fund Disbursed"] = (
            df[fund_col]
            .apply(f5_amount)
            if fund_col else np.nan
        )

        return result


    df5 = f5_load_data()


    # ============================================================
    # HEADER
    # ============================================================

    st.markdown(
        "## 💳 Payment & Vendor Anomaly Detection"
    )

    st.caption(
        "Screening payment-status and vendor patterns to identify "
        "cases requiring administrative review."
    )


    # ============================================================
    # DATA QUALITY
    # ============================================================

    st.markdown(
        "### Financial & Payment Data Quality"
    )


    total_records = len(df5)

    usable_expenditure = (
        df5["Expenditure Amount"]
        .notna()
        .sum()
    )

    usable_fund = (
        df5["Fund Disbursed"]
        .notna()
        .sum()
    )

    vendor_records = (
        df5["Vendor Name"]
        .astype(str)
        .str.strip()
        .ne("")
        .sum()
    )

    payment_records = (
        df5["Payment Status"]
        .astype(str)
        .str.strip()
        .ne("")
        .sum()
    )


    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Payment Records",
        f"{total_records:,}"
    )

    c2.metric(
        "Vendor Records",
        f"{vendor_records:,}"
    )

    c3.metric(
        "Payment Status Available",
        f"{payment_records:,}"
    )

    c4.metric(
        "Usable Expenditure",
        f"{usable_expenditure:,}"
    )

    c5.metric(
        "Usable Fund Amount",
        f"{usable_fund:,}"
    )


    # ============================================================
    # PAYMENT STATUS ANALYSIS
    # ============================================================

    st.markdown(
        "### 1. Payment Status Analysis"
    )


    if payment_records == 0:

        st.warning(
            "Payment status information is unavailable in the "
            "current dataset snapshot."
        )

        payment_summary = pd.DataFrame(
            columns=[
                "Payment Status",
                "Records",
                "Share (%)"
            ]
        )

    else:

        payment_summary = (
            df5[
                df5["Payment Status"] != ""
            ]
            .groupby("Payment Status")
            .size()
            .reset_index(
                name="Records"
            )
        )

        payment_summary["Share (%)"] = (
            payment_summary["Records"]
            /
            payment_summary["Records"].sum()
            *
            100
        ).round(1)


        st.dataframe(
            payment_summary,
            width="stretch",
            hide_index=True
        )


    # ============================================================
    # VENDOR CONCENTRATION
    # ============================================================

    st.markdown(
        "### 2. Vendor Concentration Screening"
    )


    vendor_df = df5[
        df5["Vendor Name"] != ""
    ].copy()


    if vendor_df.empty:

        st.warning(
            "Vendor information is unavailable in the "
            "current dataset snapshot."
        )

    else:

        vendor_counts = (
            vendor_df
            .groupby("Vendor Name")
            .size()
            .reset_index(
                name="Works"
            )
            .sort_values(
                "Works",
                ascending=False
            )
        )


        total_vendor_works = (
            vendor_counts["Works"].sum()
        )


        vendor_counts["Share (%)"] = (
            vendor_counts["Works"]
            /
            total_vendor_works
            *
            100
        ).round(1)


        # --------------------------------------------------------
        # Flag unusually concentrated vendors
        # --------------------------------------------------------

        vendor_median = (
            vendor_counts["Works"]
            .median()
        )

        vendor_q3 = (
            vendor_counts["Works"]
            .quantile(0.75)
        )

        vendor_q1 = (
            vendor_counts["Works"]
            .quantile(0.25)
        )

        vendor_iqr = (
            vendor_q3 - vendor_q1
        )

        vendor_upper = (
            vendor_q3
            +
            1.5 * vendor_iqr
        )


        def vendor_risk(count):

            if count > vendor_upper and count >= 5:
                return "High Review Priority"

            if (
                count > vendor_median * 2
                and count >= 5
            ):
                return "Medium Review Priority"

            return "Normal"


        vendor_counts["Screening Status"] = (
            vendor_counts["Works"]
            .apply(vendor_risk)
        )


        st.dataframe(
            vendor_counts.head(25),
            width="stretch",
            hide_index=True
        )


    # ============================================================
    # STATE-LEVEL VENDOR CONCENTRATION
    # ============================================================

    st.markdown(
        "### 3. State-Level Vendor Concentration"
    )


    if vendor_df.empty:

        st.info(
            "No usable vendor records available."
        )

    else:

        state_vendor = (
            vendor_df
            .groupby(
                [
                    "State",
                    "Vendor Name"
                ]
            )
            .size()
            .reset_index(
                name="Works"
            )
        )


        state_vendor["State Total Works"] = (
            state_vendor
            .groupby("State")["Works"]
            .transform("sum")
        )


        state_vendor["Vendor Share (%)"] = (
            state_vendor["Works"]
            /
            state_vendor["State Total Works"]
            *
            100
        ).round(1)


        # Flag vendors with unusually high state share
        state_vendor["Screening Status"] = np.where(
            (
                (state_vendor["Vendor Share (%)"] >= 25)
                &
                (state_vendor["Works"] >= 5)
            ),
            "Review Concentration",
            "Normal"
        )


        state_vendor = state_vendor.sort_values(
            [
                "Vendor Share (%)",
                "Works"
            ],
            ascending=False
        )


        st.dataframe(
            state_vendor.head(30),
            width="stretch",
            hide_index=True
        )


    # ============================================================
    # PAYMENT + VENDOR CASE SCREENING
    # ============================================================

    st.markdown(
        "### 4. Review Cases"
    )

    # Review Cases use the SAME vendor and state-level screening
    # thresholds displayed above. This keeps the dashboard traceable:
    # vendor signal -> individual work -> review status.
    review_df = df5.copy()
    review_df = review_df[
        review_df["Work ID"].astype(str).str.strip().ne("")
    ].copy()

    # Rebuild the exact vendor-level lookup used for the table above.
    vendor_counts_review = (
        review_df[review_df["Vendor Name"] != ""]
        .groupby("Vendor Name")
        .size()
    )

    if len(vendor_counts_review):
        vq1 = vendor_counts_review.quantile(0.25)
        vq3 = vendor_counts_review.quantile(0.75)
        viqr = vq3 - vq1
        vupper = vq3 + 1.5 * viqr
        vmedian = vendor_counts_review.median()
    else:
        vupper = np.inf
        vmedian = 0

    def f5_vendor_screening_signal(vendor):
        if not vendor:
            return "Normal"
        count = vendor_counts_review.get(vendor, 0)
        if count > vupper and count >= 5:
            return "High Review Priority"
        if count > vmedian * 2 and count >= 5:
            return "Medium Review Priority"
        return "Normal"

    review_df["Vendor Screening Signal"] = (
        review_df["Vendor Name"].apply(f5_vendor_screening_signal)
    )

    # Exact same State + Vendor concentration rule used above.
    state_vendor_counts_review = (
        review_df[review_df["Vendor Name"] != ""]
        .groupby(["State", "Vendor Name"])
        .size()
        .reset_index(name="Works")
    )

    if not state_vendor_counts_review.empty:
        state_vendor_counts_review["State Total Works"] = (
            state_vendor_counts_review
            .groupby("State")["Works"]
            .transform("sum")
        )
        state_vendor_counts_review["Vendor Share (%)"] = (
            state_vendor_counts_review["Works"]
            / state_vendor_counts_review["State Total Works"]
            * 100
        )
        state_vendor_counts_review["State Vendor Signal"] = np.where(
            (
                (state_vendor_counts_review["Vendor Share (%)"] >= 25)
                & (state_vendor_counts_review["Works"] >= 5)
            ),
            "Review Concentration",
            "Normal"
        )
        state_signal_lookup = {
            (row["State"], row["Vendor Name"]): row["State Vendor Signal"]
            for _, row in state_vendor_counts_review.iterrows()
        }
    else:
        state_signal_lookup = {}

    review_df["State Vendor Signal"] = [
        state_signal_lookup.get(
            (row["State"], row["Vendor Name"]),
            "Normal"
        )
        for _, row in review_df.iterrows()
    ]

    # Financial exception is only evaluated when both numeric values exist.
    review_df["Financial Data Check"] = np.where(
        (
            review_df["Fund Disbursed"].notna()
            & review_df["Expenditure Amount"].notna()
            & (review_df["Expenditure Amount"] > review_df["Fund Disbursed"])
        ),
        "Expenditure Above Disbursed Fund",
        "No Financial Exception"
    )

    def f5_review(row):
        if (
            row["Financial Data Check"] == "Expenditure Above Disbursed Fund"
            or row["Vendor Screening Signal"] == "High Review Priority"
            or row["State Vendor Signal"] == "Review Concentration"
        ):
            return "High Review Priority"

        if row["Vendor Screening Signal"] == "Medium Review Priority":
            return "Review Recommended"

        return "Normal"

    review_df["Review Status"] = review_df.apply(f5_review, axis=1)

    # ============================================================
    # FILTERS
    # ============================================================

    st.markdown(
        "### Filter Review Cases"
    )


    fc1, fc2, fc3 = st.columns(3)


    with fc1:

        state_options = sorted(
            [
                x for x in review_df["State"].unique()
                if x
            ]
        )

        selected_state = st.selectbox(
            "State",
            ["All"] + state_options,
            key="f5_state"
        )


    with fc2:

        # Review Status is a derived screening outcome for this feature.
        # It is intentionally separate from source fields such as Payment Status.
        status_options = [
            "Attention Cases (High + Recommended)",
            "High Review Priority",
            "Review Recommended",
            "Normal"
        ]

        # Default to actual review candidates. Normal records remain available
        # as an explicit filter, but should not populate the attention queue.
        selected_status = st.selectbox(
            "Review Status",
            status_options,
            index=0,
            key="f5_status_v2"
        )


    with fc3:

        vendor_search = st.text_input(
            "Search Vendor",
            key="f5_vendor_search"
        )


    filtered_f5 = review_df.copy()


    if selected_state != "All":

        filtered_f5 = filtered_f5[
            filtered_f5["State"] == selected_state
        ]


    if selected_status == "Attention Cases (High + Recommended)":

        filtered_f5 = filtered_f5[
            filtered_f5["Review Status"].isin(
                ["High Review Priority", "Review Recommended"]
            )
        ]

    elif selected_status in ["High Review Priority", "Review Recommended", "Normal"]:

        filtered_f5 = filtered_f5[
            filtered_f5["Review Status"] == selected_status
        ]


    if vendor_search.strip():

        filtered_f5 = filtered_f5[
            filtered_f5["Vendor Name"]
            .str.lower()
            .str.contains(
                vendor_search.lower(),
                regex=False,
                na=False
            )
        ]


    # ============================================================
    # REVIEW TABLE
    # ============================================================

    st.markdown(
        "### Cases Requiring Attention"
    )

    # Give the reviewer immediate feedback when a filter combination
    # has no matching records instead of rendering an apparently blank table.
    matching_cases = len(filtered_f5)

    if matching_cases == 0:

        st.info(
            "No review cases match the selected filters. "
            "Try another State, Review Status, or Vendor search."
        )

    else:

        if selected_status == "Attention Cases (High + Recommended)":
            st.caption(
                f"{matching_cases:,} review candidate(s) • showing up to 200"
            )
        else:
            st.caption(
                f"{matching_cases:,} matching record(s) • showing up to 200"
            )

        display_review = filtered_f5[
            [
                "Work ID",
                "State",
                "Constituency",
                "MP",
                "Work",
                "Vendor Name",
                "Payment Status",
                "Fund Disbursed",
                "Expenditure Amount",
                "Financial Data Check",
                "Review Status"
            ]
        ].head(200).copy()

        # Make missing values presentation-friendly without changing
        # the underlying analytical data.
        display_review["Vendor Name"] = display_review["Vendor Name"].replace(
            "", "Unavailable"
        )
        display_review["Payment Status"] = display_review["Payment Status"].replace(
            "", "Unavailable"
        )
        display_review["Fund Disbursed"] = display_review["Fund Disbursed"].apply(
            lambda x: f"₹{x:,.2f}" if pd.notna(x) else "Unavailable"
        )
        display_review["Expenditure Amount"] = display_review["Expenditure Amount"].apply(
            lambda x: f"₹{x:,.2f}" if pd.notna(x) else "Unavailable"
        )

        st.dataframe(
            display_review,
            width="stretch",
            hide_index=True
        )


    # ============================================================
    # INVESTIGATION
    # ============================================================

    st.markdown(
        "### 🔎 Investigation"
    )


    if not filtered_f5.empty:

        selected_work = st.selectbox(
            "Select a work to inspect",
            filtered_f5["Work ID"].astype(str).tolist(),
            key="f5_selected_work"
        )


        selected_row = filtered_f5[
            filtered_f5["Work ID"].astype(str)
            == str(selected_work)
        ].iloc[0]


        st.write(
            f"**Work ID:** {selected_row['Work ID']}"
        )

        st.write(
            f"**State:** {selected_row['State']}"
        )

        st.write(
            f"**Constituency:** {selected_row['Constituency']}"
        )

        st.write(
            f"**MP:** {selected_row['MP']}"
        )

        st.write(
            f"**Work:** {selected_row['Work']}"
        )

        st.write(
            f"**Vendor:** "
            f"{selected_row['Vendor Name'] or 'Unavailable'}"
        )

        st.write(
            f"**Payment Status:** "
            f"{selected_row['Payment Status'] or 'Unavailable'}"
        )

        st.write(
            f"**Fund Disbursed:** "
            f"{selected_row['Fund Disbursed'] if pd.notna(selected_row['Fund Disbursed']) else 'Unavailable'}"
        )

        st.write(
            f"**Expenditure:** "
            f"{selected_row['Expenditure Amount'] if pd.notna(selected_row['Expenditure Amount']) else 'Unavailable'}"
        )

        st.write(
            f"**Review Status:** "
            f"{selected_row['Review Status']}"
        )


    # ============================================================
    # METHODOLOGY
    # ============================================================

    with st.expander(
        "How this feature works"
    ):

        st.markdown(
            """
    ### Payment & Vendor Anomaly Screening

    The system examines:

    - Payment status patterns
    - Vendor frequency across works
    - Vendor concentration within states
    - Availability of vendor and payment information
    - Financial consistency where both expenditure and fund values are available

    ### Review Status logic

    **High Review Priority**
    - A strong screening signal is present, such as a statistical
      vendor-concentration outlier, unusually high state-level vendor
      concentration, or a financial inconsistency where both amounts
      are available.

    **Review Recommended**
    - A moderate vendor-concentration signal is present and merits
      closer administrative examination.

    **Normal**
    - No review signal is triggered by the current screening rules.

    Review Status is a derived analytical indicator, not a field from
    the MPLADS source data. These indicators do not establish fraud,
    misconduct, or wrongdoing and should be verified using official
    records and administrative review.
    """
        )


    # ============================================================
    # FOOTER
    # ============================================================

    st.caption(
        "Payment & Vendor Anomaly Detection • "
        "AI-assisted analytical screening • Decision support"
    )


    # ============================================================

def feature_6():
    # FEATURE 6 — AUTOMATED COMPLIANCE MONITORING
    # ============================================================

    import re
    import pandas as pd
    import numpy as np
    import streamlit as st
    from pathlib import Path


    # ============================================================
    # FILE PATH
    # ============================================================

    F6_FILE = Path(DATA_DIR) / "Works Sanctioned (1).csv"


    # ============================================================
    # HELPER FUNCTIONS
    # ============================================================

    def f6_clean(value):
        if pd.isna(value):
            return ""
        return str(value).strip()


    def f6_parse_work_id_and_description(value):
        """
        Extract the actual MPLADS Work ID from the Work field.

        Example:
        WS/MP187/2023-2024/1199-Construction of rooms and halls...

        Output:
        Work ID:
        WS/MP187/2023-2024/1199

        Description:
        Construction of rooms and halls...
        """

        text = f6_clean(value)

        if not text:
            return "", ""

        # Correct MPLADS Work ID pattern
        match = re.match(
            r"^(WS/[^/]+/\d{4}-\d{4}/\d+)-(.*)$",
            text,
            flags=re.IGNORECASE
        )

        if match:
            actual_id = match.group(1).strip()
            description = match.group(2).strip()

            return actual_id, description

        return "", text


    def f6_parse_date(series):
        return pd.to_datetime(
            series,
            errors="coerce",
            dayfirst=False
        )


    def f6_recommendation_status(days):

        if pd.isna(days):
            return "Data Unavailable"

        if days <= 75:
            return "Within 75 Days"

        return "Beyond 75 Days"


    # ============================================================
    # LOAD DATA
    # ============================================================

    @st.cache_data
    def f6_load_data():

        df = pd.read_csv(
            F6_FILE,
            low_memory=False
        )

        df.columns = [
            str(c).strip()
            for c in df.columns
        ]

        return df


    # ============================================================
    # PROCESS DATA
    # ============================================================

    @st.cache_data
    def f6_process_data(df):

        san = df.copy()

        # --------------------------------------------------------
        # CLEAN TEXT COLUMNS
        # --------------------------------------------------------

        for col in san.columns:

            if san[col].dtype == "object":

                san[col] = san[col].apply(
                    f6_clean
                )

        # --------------------------------------------------------
        # ACTUAL WORK ID + DESCRIPTION
        # --------------------------------------------------------

        parsed = san["Work"].apply(
            f6_parse_work_id_and_description
        )

        san["Actual Work ID"] = parsed.apply(
            lambda x: x[0]
        )

        san["Parsed Work Description"] = parsed.apply(
            lambda x: x[1]
        )

        # --------------------------------------------------------
        # IF A REAL WORK ID COLUMN EXISTS,
        # PREFER IT
        # --------------------------------------------------------

        possible_id_columns = [
            "Work ID",
            "WORK ID",
            "WorkID",
            "WORK_ID"
        ]

        for col in possible_id_columns:

            if col in san.columns:

                existing_ids = san[col].apply(
                    f6_clean
                )

                san["Actual Work ID"] = np.where(
                    existing_ids != "",
                    existing_ids,
                    san["Actual Work ID"]
                )

                break

        # ========================================================
        # RECOMMENDED DATE
        # ========================================================

        recommended_column = None

        for col in [
            "Recommended Date",
            "Recommended date",
            "Recommendation Date",
            "Recommendation date"
        ]:

            if col in san.columns:

                recommended_column = col
                break

        if recommended_column:

            san["Recommended Date Parsed"] = (
                f6_parse_date(
                    san[recommended_column]
                )
            )

        else:

            san["Recommended Date Parsed"] = pd.NaT

        # ========================================================
        # SANCTION DATE
        # ========================================================

        if "Sanction Date" in san.columns:

            san["Sanction Date Parsed"] = (
                f6_parse_date(
                    san["Sanction Date"]
                )
            )

        else:

            san["Sanction Date Parsed"] = pd.NaT

        # ========================================================
        # RECOMMENDATION → SANCTION DAYS
        # ========================================================

        san["Recommendation to Sanction Days"] = (
            san["Sanction Date Parsed"]
            -
            san["Recommended Date Parsed"]
        ).dt.days

        san["Sanction Timeline"] = (
            san["Recommendation to Sanction Days"]
            .apply(
                f6_recommendation_status
            )
        )

        # ========================================================
        # COMPLETION EVIDENCE
        # ========================================================

        if "Work Status" in san.columns:

            status_text = (
                san["Work Status"]
                .fillna("")
                .astype(str)
                .str.lower()
            )

        else:

            status_text = pd.Series(
                "",
                index=san.index
            )

        san["Completion Evidence"] = (
            status_text.apply(
                lambda x:
                "Marked Completed"
                if "completed" in x
                else "Not Marked Completed"
            )
        )

        san["Is Completed"] = (
            san["Completion Evidence"]
            ==
            "Marked Completed"
        )

        # ========================================================
        # DAYS SINCE SANCTION
        # ========================================================

        today = pd.Timestamp.today().normalize()

        san["Days Since Sanction"] = (
            today
            -
            san["Sanction Date Parsed"]
        ).dt.days

        # ========================================================
        # COMPLETION TIMELINE
        # ========================================================

        def completion_status(row):

            if row["Is Completed"]:
                return "Completed"

            days = row["Days Since Sanction"]

            if pd.isna(days):
                return "Data Review"

            if days <= 365:
                return "Within 1 Year"

            return "Beyond 1 Year"

        san["Completion Timeline"] = (
            san.apply(
                completion_status,
                axis=1
            )
        )

        # ========================================================
        # OVERALL COMPLIANCE STATUS
        # ========================================================

        def overall_status(row):

            recommendation_status = (
                row["Sanction Timeline"]
            )

            completion_status_value = (
                row["Completion Timeline"]
            )

            if (
                recommendation_status
                ==
                "Data Unavailable"
                or
                completion_status_value
                ==
                "Data Review"
            ):

                return "Data Review"

            if (
                recommendation_status
                ==
                "Beyond 75 Days"
                or
                completion_status_value
                ==
                "Beyond 1 Year"
            ):

                return "Compliance Exception"

            return "Within Benchmark"

        san["Overall Status"] = (
            san.apply(
                overall_status,
                axis=1
            )
        )

        # ========================================================
        # DATA QUALITY
        # ========================================================

        san["Data Quality"] = np.where(
            (
                san["Recommended Date Parsed"].notna()
                &
                san["Sanction Date Parsed"].notna()
            ),
            "Sufficient",
            "Review Required"
        )

        # ========================================================
        # INTERNAL SELECTION ID
        #
        # Used ONLY internally by Streamlit.
        # It will NOT be displayed to the user.
        # ========================================================

        san["Internal ID"] = [
            f"F6-{i:06d}"
            for i in range(
                1,
                len(san) + 1
            )
        ]

        return san


    # ============================================================
    # RUN FEATURE 6
    # ============================================================

    try:

        # --------------------------------------------------------
        # LOAD + PROCESS
        # --------------------------------------------------------

        f6_raw = f6_load_data()

        f6 = f6_process_data(
            f6_raw
        )

        # ========================================================
        # TITLE
        # ========================================================

        st.title(
            "📋 Automated Compliance Monitoring"
        )

        st.caption(
            "Automated screening of recommendation, sanction "
            "and completion timelines to identify cases "
            "requiring administrative review."
        )

        # ========================================================
        # COMPLIANCE OVERVIEW
        # ========================================================

        st.subheader(
            "Compliance Overview"
        )

        total_works = len(f6)

        within_75 = (
            f6["Sanction Timeline"]
            ==
            "Within 75 Days"
        ).sum()

        beyond_75 = (
            f6["Sanction Timeline"]
            ==
            "Beyond 75 Days"
        ).sum()

        beyond_year = (
            f6["Completion Timeline"]
            ==
            "Beyond 1 Year"
        ).sum()

        data_review = (
            f6["Overall Status"]
            ==
            "Data Review"
        ).sum()

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Works Monitored",
            f"{total_works:,}"
        )

        c2.metric(
            "Within 75 Days",
            f"{within_75:,}"
        )

        c3.metric(
            "Beyond 75 Days",
            f"{beyond_75:,}"
        )

        c4.metric(
            "Beyond 1 Year",
            f"{beyond_year:,}"
        )

        c5.metric(
            "Data Review",
            f"{data_review:,}"
        )

        # ========================================================
        # COMPLIANCE STATUS DISTRIBUTION
        # ========================================================

        st.subheader(
            "Compliance Status Distribution"
        )

        status_counts = (
            f6["Overall Status"]
            .value_counts()
            .rename_axis("Status")
            .reset_index(
                name="Works"
            )
        )

        st.bar_chart(
            status_counts.set_index(
                "Status"
            )
        )

        # ========================================================
        # RECOMMENDATION → SANCTION
        # ========================================================

        st.subheader(
            "Recommendation → Sanction Timeline"
        )

        rec_counts = (
            f6["Sanction Timeline"]
            .value_counts()
            .reindex(
                [
                    "Within 75 Days",
                    "Beyond 75 Days",
                    "Data Unavailable"
                ],
                fill_value=0
            )
            .rename_axis(
                "Timeline Status"
            )
            .reset_index(
                name="Works"
            )
        )

        st.dataframe(
            rec_counts,
            width="stretch",
            hide_index=True
        )

        # ========================================================
        # SANCTION → COMPLETION
        # ========================================================

        st.subheader(
            "Sanction → Completion Timeline"
        )

        comp_counts = (
            f6["Completion Timeline"]
            .value_counts()
            .reindex(
                [
                    "Within 1 Year",
                    "Beyond 1 Year",
                    "Completed",
                    "Data Review"
                ],
                fill_value=0
            )
            .rename_axis(
                "Timeline Status"
            )
            .reset_index(
                name="Works"
            )
        )

        st.dataframe(
            comp_counts,
            width="stretch",
            hide_index=True
        )

        # ========================================================
        # FILTERS
        # ========================================================

        st.subheader(
            "Filter Compliance Cases"
        )

        fc1, fc2, fc3 = st.columns(3)

        with fc1:

            state_options = (
                ["All"]
                +
                sorted(
                    [
                        x
                        for x in
                        f6["State"]
                        .dropna()
                        .unique()
                        if str(x).strip()
                    ]
                )
            )

            selected_state = st.selectbox(
                "State",
                state_options,
                key="f6_state"
            )

        with fc2:

            status_options = [
                "All",
                "Compliance Exception",
                "Within Benchmark"
            ]

            selected_status = st.selectbox(
                "Compliance Status",
                status_options,
                key="f6_status"
            )

        with fc3:

            search_text = st.text_input(
                "Search Work / Work ID",
                key="f6_search"
            )

        # --------------------------------------------------------
        # APPLY FILTERS
        # --------------------------------------------------------

        filtered = f6.copy()

        if selected_state != "All":

            filtered = filtered[
                filtered["State"]
                ==
                selected_state
            ]

        if selected_status != "All":

            filtered = filtered[
                filtered["Overall Status"]
                ==
                selected_status
            ]

        if search_text.strip():

            q = search_text.strip().lower()

            filtered = filtered[
                filtered["Actual Work ID"]
                .str.lower()
                .str.contains(
                    q,
                    na=False
                )
                |
                filtered["Work"]
                .str.lower()
                .str.contains(
                    q,
                    na=False
                )
                |
                filtered[
                    "Parsed Work Description"
                ]
                .str.lower()
                .str.contains(
                    q,
                    na=False
                )
            ]

        # ========================================================
        # FILTERED COMPLIANCE CASES
        # ========================================================

        # Show the records matching the selected compliance status.
        # This is important because selecting "Within Benchmark"
        # or "Data Review" should display those records too,
        # rather than applying a second hidden exception-only filter.
        if selected_status == "All":
            section_title = "Compliance Cases"
        elif selected_status == "Compliance Exception":
            section_title = "Compliance Exceptions"
        else:
            section_title = "Within Benchmark Cases"

        st.subheader(section_title)

        cases = filtered.copy()

        display_cols = [
            "State",
            "Constituency",
            "Actual Work ID",
            "Parsed Work Description",
            "Recommended Date Parsed",
            "Sanction Date Parsed",
            "Recommendation to Sanction Days",
            "Sanction Timeline",
            "Completion Timeline",
            "Overall Status"
        ]

        display_cols = [
            c
            for c in display_cols
            if c in cases.columns
        ]

        exception_display = (
            cases[display_cols]
            .copy()
        )

        # --------------------------------------------------------
        # FORMAT DATES
        # --------------------------------------------------------

        if (
            "Recommended Date Parsed"
            in exception_display.columns
        ):

            exception_display[
                "Recommended Date Parsed"
            ] = (
                exception_display[
                    "Recommended Date Parsed"
                ]
                .dt.strftime(
                    "%Y-%m-%d"
                )
            )

        if (
            "Sanction Date Parsed"
            in exception_display.columns
        ):

            exception_display[
                "Sanction Date Parsed"
            ] = (
                exception_display[
                    "Sanction Date Parsed"
                ]
                .dt.strftime(
                    "%Y-%m-%d"
                )
            )

        # --------------------------------------------------------
        # RENAME FOR UI
        # --------------------------------------------------------

        exception_display = (
            exception_display.rename(
                columns={

                    "Actual Work ID":
                        "Work ID",

                    "Parsed Work Description":
                        "Work Description",

                    "Recommended Date Parsed":
                        "Recommended Date",

                    "Sanction Date Parsed":
                        "Sanction Date"
                }
            )
        )

        st.dataframe(
            exception_display.head(200),
            width="stretch",
            hide_index=True
        )

        # ========================================================
        # INDIVIDUAL INVESTIGATION
        # ========================================================

        st.subheader(
            "🔎 Individual Investigation"
        )

        if len(filtered) > 0:

            # ----------------------------------------------------
            # FAST LOOKUP
            #
            # Build dictionary ONCE instead of repeatedly
            # searching the entire dataframe.
            # ----------------------------------------------------

            investigation_lookup = {}

            for _, investigation_row in filtered.iterrows():

                internal_id = (
                    investigation_row[
                        "Internal ID"
                    ]
                )

                investigation_lookup[
                    internal_id
                ] = investigation_row

            investigation_options = list(
                investigation_lookup.keys()
            )

            # ----------------------------------------------------
            # SHOW ACTUAL WORK ID IN DROPDOWN
            # ----------------------------------------------------

            def f6_display_work_id(
                internal_id
            ):

                row = investigation_lookup.get(
                    internal_id
                )

                if row is not None:

                    actual_id = row[
                        "Actual Work ID"
                    ]

                    if actual_id:

                        return actual_id

                return "Work ID Unavailable"

            # Use a filter-specific widget key so Streamlit cannot
            # retain a selection from a previous compliance filter.
            # This keeps the displayed Work ID and investigation row
            # synchronized when switching between All / Exception /
            # Data Review / Within Benchmark.
            investigation_widget_key = (
                "f6_investigation_"
                + str(selected_state)
                + "_"
                + str(selected_status)
                + "_"
                + str(search_text).strip().lower()
            )

            selected_internal = st.selectbox(
                "Select a work for investigation",
                investigation_options,
                format_func=f6_display_work_id,
                key=investigation_widget_key
            )

            # ----------------------------------------------------
            # INSTANT ROW RETRIEVAL
            # ----------------------------------------------------

            selected_row = investigation_lookup.get(
                selected_internal
            )

            # Defensive fallback: the selected row must come from
            # the currently filtered dataframe, never from an older
            # selection.
            if selected_row is None:
                selected_internal = investigation_options[0]
                selected_row = investigation_lookup[
                    selected_internal
                ]

            # ====================================================
            # WORK DETAILS
            # ====================================================

            st.markdown(
                "### Work Details"
            )

            d1, d2 = st.columns(2)

            with d1:

                # ------------------------------------------------
                # WORK ID
                # ------------------------------------------------

                actual_work_id = (
                    selected_row[
                        "Actual Work ID"
                    ]
                )

                st.write(
                    "**Work ID:**",
                    actual_work_id
                    if actual_work_id
                    else "Unavailable"
                )

                # ------------------------------------------------
                # STATE
                # ------------------------------------------------

                state_value = (
                    selected_row[
                        "State"
                    ]
                )

                st.write(
                    "**State:**",
                    state_value
                    if state_value
                    else "Unavailable"
                )

                # ------------------------------------------------
                # CONSTITUENCY
                # ------------------------------------------------

                constituency_value = (
                    selected_row[
                        "Constituency"
                    ]
                )

                st.write(
                    "**Constituency:**",
                    constituency_value
                    if constituency_value
                    else "Unavailable"
                )

                # ------------------------------------------------
                # MP
                # ------------------------------------------------

                mp_value = ""

                if (
                    "Hon’ble Member"
                    in selected_row.index
                ):

                    mp_value = (
                        selected_row[
                            "Hon’ble Member"
                        ]
                    )

                elif (
                    "Hon'ble Member"
                    in selected_row.index
                ):

                    mp_value = (
                        selected_row[
                            "Hon'ble Member"
                        ]
                    )

                st.write(
                    "**MP:**",
                    mp_value
                    if mp_value
                    else "Unavailable"
                )

            with d2:

                # ------------------------------------------------
                # DESCRIPTION
                # ------------------------------------------------

                description = (
                    selected_row[
                        "Parsed Work Description"
                    ]
                )

                st.write(
                    "**Work Description:**",
                    description
                    if description
                    else "Description Unavailable"
                )

                # ------------------------------------------------
                # RECOMMENDED DATE
                # ------------------------------------------------

                recommended_date = (
                    selected_row[
                        "Recommended Date Parsed"
                    ]
                )

                if pd.notna(
                    recommended_date
                ):

                    recommended_display = (
                        recommended_date.strftime(
                            "%Y-%m-%d"
                        )
                    )

                else:

                    recommended_display = (
                        "Unavailable"
                    )

                st.write(
                    "**Recommended Date:**",
                    recommended_display
                )

                # ------------------------------------------------
                # SANCTION DATE
                # ------------------------------------------------

                sanction_date = (
                    selected_row[
                        "Sanction Date Parsed"
                    ]
                )

                if pd.notna(
                    sanction_date
                ):

                    sanction_display = (
                        sanction_date.strftime(
                            "%Y-%m-%d"
                        )
                    )

                else:

                    sanction_display = (
                        "Unavailable"
                    )

                st.write(
                    "**Sanction Date:**",
                    sanction_display
                )

                # ------------------------------------------------
                # WORK STATUS
                # ------------------------------------------------

                work_status = ""

                if (
                    "Work Status"
                    in selected_row.index
                ):

                    work_status = (
                        selected_row[
                            "Work Status"
                        ]
                    )

                st.write(
                    "**Work Status:**",
                    work_status
                    if work_status
                    else "Unavailable"
                )

            # ====================================================
            # TIMELINE ASSESSMENT
            # ====================================================

            st.markdown(
                "### Timeline Assessment"
            )

            t1, t2, t3 = st.columns(3)

            with t1:

                rec_days = (
                    selected_row[
                        "Recommendation to Sanction Days"
                    ]
                )

                st.metric(
                    "Recommendation → Sanction",
                    (
                        f"{int(rec_days)} days"
                        if pd.notna(rec_days)
                        else "Unavailable"
                    )
                )

            with t2:

                sanction_days = (
                    selected_row[
                        "Days Since Sanction"
                    ]
                )

                st.metric(
                    "Days Since Sanction",
                    (
                        f"{int(sanction_days)}"
                        if pd.notna(sanction_days)
                        else "Unavailable"
                    )
                )

            with t3:

                st.metric(
                    "Overall Status",
                    selected_row[
                        "Overall Status"
                    ]
                )

            # ----------------------------------------------------
            # TIMELINE DETAILS
            # ----------------------------------------------------

            st.write(
                "**Sanction Timeline:**",
                selected_row[
                    "Sanction Timeline"
                ]
            )

            st.write(
                "**Completion Timeline:**",
                selected_row[
                    "Completion Timeline"
                ]
            )

            st.write(
                "**Completion Evidence:**",
                selected_row[
                    "Completion Evidence"
                ]
            )

            st.write(
                "**Data Quality:**",
                selected_row[
                    "Data Quality"
                ]
            )

            # ====================================================
            # ASSESSMENT
            # ====================================================

            st.markdown(
                "### Assessment"
            )

            if (
                selected_row[
                    "Overall Status"
                ]
                ==
                "Compliance Exception"
            ):

                st.warning(
                    "This work falls outside one or more "
                    "configured timeline benchmarks and "
                    "should be reviewed by the responsible "
                    "authority."
                )

            elif (
                selected_row[
                    "Overall Status"
                ]
                ==
                "Data Review"
            ):

                st.info(
                    "Required timeline information is "
                    "incomplete or requires additional "
                    "administrative verification."
                )

            else:

                st.success(
                    "No timeline exception was identified "
                    "under the configured monitoring "
                    "benchmarks."
                )

        else:

            st.info(
                "No works match the selected filters."
            )

        # ========================================================
        # METHODOLOGY
        # ========================================================

        with st.expander(
            "Methodology"
        ):

            st.write(
                """
                **Recommendation → Sanction**

                Works are screened against a 75-day benchmark
                between recommendation and sanction.

                **Sanction → Completion**

                Works are screened against a one-year completion
                benchmark. A work marked completed in the available
                status data is shown separately.

                **Data Quality**

                Missing dates or incomplete status information are
                classified for review rather than being treated as
                compliant or non-compliant.

                These indicators are screening signals for
                administrative review and do not by themselves
                establish non-compliance, misuse or fraud.
                """
            )

        # ========================================================
        # FOOTER
        # ========================================================

        st.caption(
            "Feature 6 • Automated Compliance Monitoring • "
            "MPLADS Decision-Support Prototype"
        )


    except Exception as e:

        st.error(
            f"Feature 6 could not be loaded: {e}"
        )


    # ============================================================

def feature_7():
    # FEATURE 7 — COMBINED AI RISK SCORE & EXPLAINABLE INSIGHTS
    # FINAL STABLE VERSION
    # ============================================================

    import re
    import pandas as pd
    import numpy as np
    import streamlit as st
    from pathlib import Path


    # ============================================================
    # FILE PATHS
    # ============================================================

    F7_SANCTIONED_FILE = (
        Path(DATA_DIR) / "Works Sanctioned (1).csv"
    )

    F7_EXPENDITURE_FILE = (
        Path(DATA_DIR)
        / "Expenditure on Completed and On-going Works as on Date.csv"
    )

    F7_F4_CACHE_FILE = (
        Path(DATA_DIR) / "f4_high_similarity_cache.csv"
    )


    # ============================================================
    # HELPER FUNCTIONS
    # ============================================================

    def f7_clean(value):

        if pd.isna(value):
            return ""

        text = str(value).strip()

        if text.lower() in [
            "nan",
            "none",
            "null",
            "*****"
        ]:
            return ""

        return text


    def f7_extract_work_id(value):

        text = f7_clean(value)

        if not text:
            return ""

        match = re.match(
            r"^(WS/[^/]+/\d{4}-\d{4}/\d+)-",
            text,
            flags=re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

        return ""


    def f7_extract_description(value):

        text = f7_clean(value)

        if not text:
            return ""

        match = re.match(
            r"^WS/[^/]+/\d{4}-\d{4}/\d+-(.*)$",
            text,
            flags=re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

        return text


    def f7_normalize_description(value):

        text = f7_clean(value).lower()

        text = re.sub(
            r"[^a-z0-9\s]",
            " ",
            text
        )

        text = re.sub(
            r"\s+",
            " ",
            text
        )

        return text.strip()


    def f7_risk_level(score):

        if score >= 70:
            return "High"

        elif score >= 40:
            return "Medium"

        return "Low"


    def f7_priority(score):

        if score >= 70:
            return "High Review Priority"

        elif score >= 40:
            return "Medium Review Priority"

        return "Low Review Priority"


    # ============================================================
    # LOAD DATA
    # ============================================================

    def f7_load_data():

        sanctioned = pd.read_csv(
            F7_SANCTIONED_FILE,
            low_memory=False
        )

        expenditure = pd.read_csv(
            F7_EXPENDITURE_FILE,
            low_memory=False
        )

        sanctioned.columns = [
            str(c).strip()
            for c in sanctioned.columns
        ]

        expenditure.columns = [
            str(c).strip()
            for c in expenditure.columns
        ]

        return sanctioned, expenditure


    def f7_load_feature4_cache():

        if not F7_F4_CACHE_FILE.exists():

            return pd.DataFrame()

        try:

            cache = pd.read_csv(
                F7_F4_CACHE_FILE,
                low_memory=False
            )

            cache.columns = [
                str(c).strip()
                for c in cache.columns
            ]

            return cache

        except Exception:

            return pd.DataFrame()


    # ============================================================
    # PROCESS FEATURE 7
    # ============================================================

    def f7_process_data(
        sanctioned,
        expenditure,
        similarity_cache
    ):

        df = sanctioned.copy()
        exp = expenditure.copy()

        # ========================================================
        # CLEAN DATA
        # ========================================================

        for col in df.columns:

            if df[col].dtype == "object":

                df[col] = df[col].apply(
                    f7_clean
                )

        for col in exp.columns:

            if exp[col].dtype == "object":

                exp[col] = exp[col].apply(
                    f7_clean
                )

        # ========================================================
        # ACTUAL WORK ID + DESCRIPTION
        # ========================================================

        if "Work" in df.columns:

            df["Actual Work ID"] = (
                df["Work"]
                .apply(f7_extract_work_id)
            )

            df["Work Description"] = (
                df["Work"]
                .apply(f7_extract_description)
            )

        else:

            df["Actual Work ID"] = ""
            df["Work Description"] = ""

        # ========================================================
        # REMOVE DUPLICATE WORK IDs
        # ========================================================

        has_work_id = (
            df["Actual Work ID"]
            .astype(str)
            .str.strip()
            .ne("")
        )

        with_id = (
            df[has_work_id]
            .drop_duplicates(
                subset=["Actual Work ID"],
                keep="first"
            )
        )

        without_id = df[~has_work_id]

        df = pd.concat(
            [
                with_id,
                without_id
            ],
            ignore_index=True
        )

        # ========================================================
        # DATE PROCESSING
        # ========================================================

        if "Recommended Date" in df.columns:

            df["Recommended Date Parsed"] = pd.to_datetime(
                df["Recommended Date"],
                errors="coerce"
            )

        else:

            df["Recommended Date Parsed"] = pd.NaT

        if "Sanction Date" in df.columns:

            df["Sanction Date Parsed"] = pd.to_datetime(
                df["Sanction Date"],
                errors="coerce"
            )

        else:

            df["Sanction Date Parsed"] = pd.NaT

        today = pd.Timestamp.today().normalize()

        # ========================================================
        # FEATURE 6
        # RECOMMENDATION → SANCTION
        #
        # Maximum = 15
        # ========================================================

        df["Recommendation to Sanction Days"] = (
            df["Sanction Date Parsed"]
            -
            df["Recommended Date Parsed"]
        ).dt.days

        df["F6 Sanction Points"] = 0.0

        mask = (
            df["Recommendation to Sanction Days"]
            .notna()
        )

        df.loc[
            mask
            &
            (
                df["Recommendation to Sanction Days"] > 75
            ),
            "F6 Sanction Points"
        ] = 7

        df.loc[
            mask
            &
            (
                df["Recommendation to Sanction Days"] > 120
            ),
            "F6 Sanction Points"
        ] = 11

        df.loc[
            mask
            &
            (
                df["Recommendation to Sanction Days"] > 180
            ),
            "F6 Sanction Points"
        ] = 15

        # ========================================================
        # FEATURE 1
        # SANCTION → COMPLETION
        #
        # Maximum = 20
        # ========================================================

        df["Days Since Sanction"] = (
            today
            -
            df["Sanction Date Parsed"]
        ).dt.days

        if "Work Status" in df.columns:

            status_text = (
                df["Work Status"]
                .fillna("")
                .astype(str)
                .str.lower()
            )

        else:

            status_text = pd.Series(
                "",
                index=df.index
            )

        df["Completed"] = (
            status_text
            .str.contains(
                r"\bcompleted\b",
                regex=True,
                na=False
            )
        )

        df["F1 Completion Points"] = 0.0

        incomplete = (
            df["Days Since Sanction"].notna()
            &
            ~df["Completed"]
        )

        df.loc[
            incomplete
            &
            (
                df["Days Since Sanction"] > 365
            ),
            "F1 Completion Points"
        ] = 8

        df.loc[
            incomplete
            &
            (
                df["Days Since Sanction"] > 540
            ),
            "F1 Completion Points"
        ] = 14

        df.loc[
            incomplete
            &
            (
                df["Days Since Sanction"] > 730
            ),
            "F1 Completion Points"
        ] = 20

        # ========================================================
        # FEATURE 6
        # ONGOING STATUS
        #
        # Maximum = 10
        # ========================================================

        ongoing_keywords = [
            "vendor identification",
            "vendor",
            "tender",
            "work in progress",
            "in progress",
            "under process",
            "physical inspection"
        ]

        df["Ongoing Work"] = (
            status_text.apply(
                lambda x:
                any(
                    keyword in x
                    for keyword in ongoing_keywords
                )
            )
        )

        df["F6 Status Points"] = np.where(
            df["Ongoing Work"],
            10,
            0
        )

        # ========================================================
        # EXPENDITURE WORK ID
        # ========================================================

        if "Work" in exp.columns:

            exp["Actual Work ID"] = (
                exp["Work"]
                .apply(f7_extract_work_id)
            )

        else:

            exp["Actual Work ID"] = ""

        # ========================================================
        # FUND AMOUNT
        # ========================================================

        exp["Fund Numeric"] = np.nan

        if "Fund Disbursed Amount" in exp.columns:

            exp["Fund Numeric"] = pd.to_numeric(
                exp["Fund Disbursed Amount"],
                errors="coerce"
            )

            exp.loc[
                exp["Fund Numeric"] <= 0,
                "Fund Numeric"
            ] = np.nan

        df["Fund Amount"] = np.nan

        usable_exp = exp[
            exp["Actual Work ID"]
            .astype(str)
            .str.strip()
            .ne("")
            &
            exp["Fund Numeric"].notna()
        ].copy()

        # ========================================================
        # MAP FUND AMOUNT
        # ========================================================

        if len(usable_exp) > 0:

            fund_map = (
                usable_exp
                .groupby(
                    "Actual Work ID"
                )["Fund Numeric"]
                .median()
            )

            df["Fund Amount"] = (
                df["Actual Work ID"]
                .map(fund_map)
            )

        # ========================================================
        # FEATURE 2
        # FINANCIAL ANOMALY
        #
        # Maximum = 10
        # ========================================================

        df["F2 Financial Points"] = 0.0
        df["F2 State Median"] = np.nan
        df["F2 Upper Fence"] = np.nan

        if len(usable_exp) > 0:

            financial_data = usable_exp.merge(
                df[
                    [
                        "Actual Work ID",
                        "State"
                    ]
                ],
                on="Actual Work ID",
                how="left"
            )

            state_stats = (
                financial_data
                .groupby("State")["Fund Numeric"]
                .agg(
                    Q1=lambda x: x.quantile(0.25),
                    Median="median",
                    Q3=lambda x: x.quantile(0.75)
                )
            )

            state_stats["IQR"] = (
                state_stats["Q3"]
                -
                state_stats["Q1"]
            )

            state_stats["Upper Fence"] = (
                state_stats["Q3"]
                +
                1.5
                *
                state_stats["IQR"]
            )

            df["F2 State Median"] = (
                df["State"]
                .map(
                    state_stats["Median"]
                )
            )

            df["F2 Upper Fence"] = (
                df["State"]
                .map(
                    state_stats["Upper Fence"]
                )
            )

            valid = (
                df["Fund Amount"].notna()
                &
                df["F2 State Median"].notna()
                &
                df["F2 Upper Fence"].notna()
            )

            # Statistical outlier
            df.loc[
                valid
                &
                (
                    df["Fund Amount"]
                    >
                    df["F2 Upper Fence"]
                ),
                "F2 Financial Points"
            ] = 10

            # Moderate financial deviation
            df.loc[
                valid
                &
                (
                    df["F2 Financial Points"] == 0
                )
                &
                (
                    df["Fund Amount"]
                    >
                    df["F2 State Median"] * 1.5
                ),
                "F2 Financial Points"
            ] = 5

        # ========================================================
        # FEATURE 3
        # PEER COST DEVIATION
        #
        # State + Work Type
        # Minimum 5 peers
        # Maximum = 15
        # ========================================================

        df["F3 Work Type"] = ""
        df["F3 Peer Median"] = np.nan
        df["F3 Cost Deviation %"] = np.nan
        df["F3 Cost Points"] = 0.0

        def classify_work_type(text):

            x = f7_clean(text).lower()

            if any(
                k in x
                for k in [
                    "road",
                    "pathway",
                    "drainage",
                    "bridge"
                ]
            ):
                return "Road & Infrastructure"

            if any(
                k in x
                for k in [
                    "school",
                    "college",
                    "education",
                    "classroom"
                ]
            ):
                return "Education"

            if any(
                k in x
                for k in [
                    "hospital",
                    "health",
                    "medical",
                    "clinic"
                ]
            ):
                return "Health"

            if any(
                k in x
                for k in [
                    "street light",
                    "high mast",
                    "led light",
                    "lighting"
                ]
            ):
                return "Lighting"

            if any(
                k in x
                for k in [
                    "community hall",
                    "hall",
                    "building"
                ]
            ):
                return "Community Buildings"

            if any(
                k in x
                for k in [
                    "water",
                    "drinking",
                    "borewell",
                    "pipeline"
                ]
            ):
                return "Water"

            if any(
                k in x
                for k in [
                    "bus",
                    "van",
                    "vehicle"
                ]
            ):
                return "Transport"

            return "Other"

        df["F3 Work Type"] = (
            df["Work Description"]
            .apply(classify_work_type)
        )

        if len(usable_exp) > 0:

            peer_data = usable_exp.merge(
                df[
                    [
                        "Actual Work ID",
                        "State",
                        "F3 Work Type"
                    ]
                ],
                on="Actual Work ID",
                how="left"
            )

            peer_stats = (
                peer_data
                .groupby(
                    [
                        "State",
                        "F3 Work Type"
                    ]
                )["Fund Numeric"]
                .agg(
                    Peer_Count="count",
                    Peer_Median="median",
                    Q1=lambda x: x.quantile(0.25),
                    Q3=lambda x: x.quantile(0.75)
                )
            )

            peer_stats["IQR"] = (
                peer_stats["Q3"]
                -
                peer_stats["Q1"]
            )

            peer_stats["Upper Fence"] = (
                peer_stats["Q3"]
                +
                1.5
                *
                peer_stats["IQR"]
            )

            df = df.merge(
                peer_stats[
                    [
                        "Peer_Count",
                        "Peer_Median",
                        "Upper Fence"
                    ]
                ],
                left_on=[
                    "State",
                    "F3 Work Type"
                ],
                right_index=True,
                how="left"
            )

            df["F3 Peer Median"] = (
                df["Peer_Median"]
            )

            valid_peer = (
                df["Fund Amount"].notna()
                &
                df["Peer_Median"].notna()
                &
                (
                    df["Peer_Count"] >= 5
                )
                &
                (
                    df["Peer_Median"] > 0
                )
            )

            df.loc[
                valid_peer,
                "F3 Cost Deviation %"
            ] = (
                (
                    df.loc[
                        valid_peer,
                        "Fund Amount"
                    ]
                    -
                    df.loc[
                        valid_peer,
                        "Peer_Median"
                    ]
                )
                /
                df.loc[
                    valid_peer,
                    "Peer_Median"
                ]
                *
                100
            )

            # Statistical outlier
            df.loc[
                valid_peer
                &
                (
                    df["Fund Amount"]
                    >
                    df["Upper Fence"]
                ),
                "F3 Cost Points"
            ] = 15

            # 40%+ above peer median
            df.loc[
                valid_peer
                &
                (
                    df["F3 Cost Points"] == 0
                )
                &
                (
                    df["F3 Cost Deviation %"] >= 40
                ),
                "F3 Cost Points"
            ] = 8

            # 25%+ above peer median
            df.loc[
                valid_peer
                &
                (
                    df["F3 Cost Points"] == 0
                )
                &
                (
                    df["F3 Cost Deviation %"] >= 25
                ),
                "F3 Cost Points"
            ] = 4

            df.drop(
                columns=[
                    "Peer_Count",
                    "Peer_Median",
                    "Upper Fence"
                ],
                inplace=True,
                errors="ignore"
            )

        # ========================================================
        # FEATURE 4
        # SIMILAR / DUPLICATE WORK
        #
        # Maximum = 15
        # ========================================================

        df["F4 Normalized Description"] = (
            df["Work Description"]
            .apply(
                f7_normalize_description
            )
        )

        df["F4 Similar Work Count"] = 0
        df["F4 Best Similarity"] = np.nan
        df["F4 Exact Match"] = False
        df["F4 Similar Work Points"] = 0.0

        # --------------------------------------------------------
        # EXACT DESCRIPTION MATCH
        # Same State + Constituency
        # --------------------------------------------------------

        meaningful = (
            df["F4 Normalized Description"]
            .str.len()
            >= 10
        )

        if meaningful.any():

            grouped = (
                df.loc[meaningful]
                .groupby(
                    [
                        "State",
                        "Constituency",
                        "F4 Normalized Description"
                    ]
                )["Actual Work ID"]
                .transform("count")
            )

            exact_mask = (
                meaningful
                &
                (
                    grouped > 1
                )
            )

            df.loc[
                exact_mask,
                "F4 Exact Match"
            ] = True

            df.loc[
                exact_mask,
                "F4 Similar Work Count"
            ] = (
                grouped[exact_mask]
                - 1
            )

            df.loc[
                exact_mask,
                "F4 Similar Work Points"
            ] = 15

        # --------------------------------------------------------
        # FEATURE 4 PRECOMPUTED HIGH-SIMILARITY CACHE
        # --------------------------------------------------------

        if (
            similarity_cache is not None
            and
            len(similarity_cache) > 0
        ):

            cache = similarity_cache.copy()

            cache.columns = [
                str(c).strip()
                for c in cache.columns
            ]

            id_a_col = None
            id_b_col = None
            sim_col = None

            for col in cache.columns:

                low = str(col).lower()

                if (
                    id_a_col is None
                    and
                    (
                        "work id a" in low
                        or
                        "work_id_a" in low
                    )
                ):
                    id_a_col = col

                if (
                    id_b_col is None
                    and
                    (
                        "work id b" in low
                        or
                        "work_id_b" in low
                    )
                ):
                    id_b_col = col

                if (
                    sim_col is None
                    and
                    "similarity" in low
                ):
                    sim_col = col

            if (
                id_a_col is not None
                and
                id_b_col is not None
                and
                sim_col is not None
            ):

                cache[id_a_col] = (
                    cache[id_a_col]
                    .astype(str)
                    .str.strip()
                )

                cache[id_b_col] = (
                    cache[id_b_col]
                    .astype(str)
                    .str.strip()
                )

                cache[sim_col] = pd.to_numeric(
                    cache[sim_col],
                    errors="coerce"
                )

                cache = cache[
                    cache[sim_col] >= 92
                ].copy()

                # Best similarity for each work
                best_a = (
                    cache
                    .groupby(id_a_col)[sim_col]
                    .max()
                )

                best_b = (
                    cache
                    .groupby(id_b_col)[sim_col]
                    .max()
                )

                best_similarity = pd.concat(
                    [
                        best_a,
                        best_b
                    ]
                )

                best_similarity = (
                    best_similarity
                    .groupby(
                        level=0
                    )
                    .max()
                )

                df["F4 Best Similarity"] = (
                    df["Actual Work ID"]
                    .map(best_similarity)
                )

                # Number of similar candidates
                count_a = (
                    cache
                    .groupby(id_a_col)
                    .size()
                )

                count_b = (
                    cache
                    .groupby(id_b_col)
                    .size()
                )

                all_counts = pd.concat(
                    [
                        count_a,
                        count_b
                    ]
                )

                all_counts = (
                    all_counts
                    .groupby(
                        level=0
                    )
                    .sum()
                )

                cached_count = (
                    df["Actual Work ID"]
                    .map(all_counts)
                    .fillna(0)
                )

                df["F4 Similar Work Count"] = np.maximum(
                    df["F4 Similar Work Count"],
                    cached_count
                )

                # ------------------------------------------------
                # Similarity scoring
                # ------------------------------------------------

                sim = df["F4 Best Similarity"]

                df.loc[
                    sim >= 99,
                    "F4 Similar Work Points"
                ] = np.maximum(
                    df.loc[
                        sim >= 99,
                        "F4 Similar Work Points"
                    ],
                    12
                )

                df.loc[
                    (sim >= 95)
                    &
                    (sim < 99),
                    "F4 Similar Work Points"
                ] = np.maximum(
                    df.loc[
                        (sim >= 95)
                        &
                        (sim < 99),
                        "F4 Similar Work Points"
                    ],
                    8
                )

                df.loc[
                    (sim >= 92)
                    &
                    (sim < 95),
                    "F4 Similar Work Points"
                ] = np.maximum(
                    df.loc[
                        (sim >= 92)
                        &
                        (sim < 95),
                        "F4 Similar Work Points"
                    ],
                    5
                )

        # ========================================================
        # FEATURE 5
        # PAYMENT STATUS
        #
        # Maximum = 5
        # ========================================================

        df["Payment Status"] = ""
        df["F5 Payment Points"] = 0.0

        if "Payment Status" in exp.columns:

            payment_data = (
                exp[
                    [
                        "Actual Work ID",
                        "Payment Status"
                    ]
                ]
                .drop_duplicates(
                    "Actual Work ID"
                )
            )

            payment_map = (
                payment_data
                .set_index(
                    "Actual Work ID"
                )["Payment Status"]
            )

            df["Payment Status"] = (
                df["Actual Work ID"]
                .map(payment_map)
                .fillna("")
            )

            payment_lower = (
                df["Payment Status"]
                .astype(str)
                .str.lower()
            )

            payment_review = (
                payment_lower
                .str.contains(
                    "pending|progress|process",
                    regex=True,
                    na=False
                )
            )

            df.loc[
                payment_review,
                "F5 Payment Points"
            ] = 5

        # ========================================================
        # FEATURE 5
        # VENDOR CONCENTRATION
        #
        # Maximum = 5
        # ========================================================

        df["Vendor Name"] = ""
        df["Vendor Work Count"] = 0
        df["F5 Vendor Points"] = 0.0

        if "Vendor Name" in exp.columns:

            vendor_data = exp[
                [
                    "Actual Work ID",
                    "Vendor Name"
                ]
            ].copy()

            vendor_data = vendor_data[
                vendor_data[
                    "Vendor Name"
                ]
                .astype(str)
                .str.strip()
                .ne("")
            ]

            if len(vendor_data) > 0:

                vendor_counts = (
                    vendor_data
                    .groupby(
                        "Vendor Name"
                    )["Actual Work ID"]
                    .nunique()
                )

                vendor_map = (
                    vendor_data
                    .drop_duplicates(
                        "Actual Work ID"
                    )
                    .set_index(
                        "Actual Work ID"
                    )["Vendor Name"]
                )

                df["Vendor Name"] = (
                    df["Actual Work ID"]
                    .map(vendor_map)
                    .fillna("")
                )

                df["Vendor Work Count"] = (
                    df["Vendor Name"]
                    .map(vendor_counts)
                    .fillna(0)
                )

                df.loc[
                    df["Vendor Work Count"] >= 100,
                    "F5 Vendor Points"
                ] = 5

                df.loc[
                    (
                        df["Vendor Work Count"] >= 50
                    )
                    &
                    (
                        df["Vendor Work Count"] < 100
                    ),
                    "F5 Vendor Points"
                ] = 3

        # ========================================================
        # FINAL COMBINED SCORE
        #
        # Completion Delay              20
        # Financial Anomaly              10
        # Peer Cost Deviation            15
        # Similar / Duplicate Work       15
        # Payment Status                  5
        # Vendor Concentration            5
        # Recommendation → Sanction     15
        # Ongoing Status                 10
        #
        # TOTAL                          95
        # ========================================================

        df["Raw Risk Score"] = (
            df["F1 Completion Points"]
            +
            df["F2 Financial Points"]
            +
            df["F3 Cost Points"]
            +
            df["F4 Similar Work Points"]
            +
            df["F5 Payment Points"]
            +
            df["F5 Vendor Points"]
            +
            df["F6 Sanction Points"]
            +
            df["F6 Status Points"]
        )

        df["Risk Score"] = (
            df["Raw Risk Score"]
            /
            95
            *
            100
        ).clip(
            0,
            100
        )

        # ========================================================
        # REAL AI / ML LAYER — UNSUPERVISED ANOMALY DETECTION
        # ========================================================
        # The supplied snapshot has no labelled fraud/non-fraud target.
        # Therefore this is an unsupervised anomaly model, not a fraud classifier.
        try:
            from sklearn.ensemble import IsolationForest

            ai_features = pd.DataFrame({
                "days_since_sanction": pd.to_numeric(df["Days Since Sanction"], errors="coerce"),
                "recommendation_to_sanction": pd.to_numeric(df["Recommendation to Sanction Days"], errors="coerce"),
                "rule_risk": pd.to_numeric(df["Risk Score"], errors="coerce"),
                "completion_points": pd.to_numeric(df["F1 Completion Points"], errors="coerce"),
                "financial_points": pd.to_numeric(df["F2 Financial Points"], errors="coerce"),
                "cost_points": pd.to_numeric(df["F3 Cost Points"], errors="coerce"),
                "similarity_points": pd.to_numeric(df["F4 Similar Work Points"], errors="coerce"),
                "payment_points": pd.to_numeric(df["F5 Payment Points"], errors="coerce"),
                "vendor_points": pd.to_numeric(df["F5 Vendor Points"], errors="coerce"),
                "sanction_points": pd.to_numeric(df["F6 Sanction Points"], errors="coerce"),
                "status_points": pd.to_numeric(df["F6 Status Points"], errors="coerce"),
            }).replace([np.inf, -np.inf], np.nan)
            ai_features = ai_features.fillna(ai_features.median(numeric_only=True)).fillna(0)

            if len(ai_features) >= 20 and ai_features.nunique().sum() > 1:
                ai_model = IsolationForest(n_estimators=200, contamination="auto", random_state=42, n_jobs=-1)
                ai_model.fit(ai_features)
                raw_ai = -ai_model.decision_function(ai_features)
                raw_min = float(np.nanmin(raw_ai))
                raw_max = float(np.nanmax(raw_ai))
                if raw_max > raw_min:
                    df["AI Anomaly Score"] = ((raw_ai - raw_min) / (raw_max - raw_min) * 100).clip(0, 100)
                else:
                    df["AI Anomaly Score"] = 0.0
                df["AI Anomaly Flag"] = np.where(ai_model.predict(ai_features) == -1, "AI anomaly candidate", "Typical pattern")
            else:
                df["AI Anomaly Score"] = df["Risk Score"]
                df["AI Anomaly Flag"] = "AI model needs more variation"
        except Exception:
            df["AI Anomaly Score"] = df["Risk Score"]
            df["AI Anomaly Flag"] = "AI model unavailable"

        # Mostly transparent rule score + a smaller ML component.
        df["AI-Assisted Risk Score"] = (
            (df["Risk Score"] * 0.80) +
            (df["AI Anomaly Score"] * 0.20)
        ).clip(0, 100)

        df["Risk Level"] = (
            df["AI-Assisted Risk Score"]
            .apply(f7_risk_level)
        )

        df["Review Priority"] = (
            df["AI-Assisted Risk Score"]
            .apply(f7_priority)
        )

        # ========================================================
        # INTERNAL SELECTION ID
        # ========================================================

        df["F7 Internal ID"] = [
            f"F7-{i:06d}"
            for i in range(
                1,
                len(df) + 1
            )
        ]

        return df


    # ============================================================
    # MAIN FEATURE 7
    # ============================================================

    try:

        # ========================================================
        # LOAD
        # ========================================================

        f7_sanctioned, f7_expenditure = (
            f7_load_data()
        )

        f7_similarity_cache = (
            f7_load_feature4_cache()
        )

        # ========================================================
        # PROCESS
        # ========================================================

        f7 = f7_process_data(
            f7_sanctioned,
            f7_expenditure,
            f7_similarity_cache
        )

        # ========================================================
        # TITLE
        # ========================================================

        st.title(
            "🧠 AI-Assisted Risk & Anomaly Assessment"
        )

        st.caption(
            "Combines explainable monitoring signals with an unsupervised ML anomaly model (Isolation Forest) to prioritize works for administrative review."
        )

        # ========================================================
        # OVERVIEW
        # ========================================================

        st.subheader(
            "Risk Overview"
        )

        total_works = len(f7)

        high_count = int(
            (
                f7["Risk Level"] == "High"
            ).sum()
        )

        medium_count = int(
            (
                f7["Risk Level"] == "Medium"
            ).sum()
        )

        low_count = int(
            (
                f7["Risk Level"] == "Low"
            ).sum()
        )

        average_score = float(
            f7["AI-Assisted Risk Score"].mean()
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Works Assessed",
            f"{total_works:,}"
        )

        c2.metric(
            "High Risk",
            f"{high_count:,}"
        )

        c3.metric(
            "Medium Risk",
            f"{medium_count:,}"
        )

        c4.metric(
            "Average Risk Score",
            f"{average_score:.1f}/100"
        )

        # ========================================================
        # RISK DISTRIBUTION
        # ========================================================

        st.subheader(
            "Risk Distribution"
        )

        risk_chart = pd.DataFrame(
            {
                "Risk Level": [
                    "High",
                    "Medium",
                    "Low"
                ],
                "Works": [
                    high_count,
                    medium_count,
                    low_count
                ]
            }
        )

        st.bar_chart(
            risk_chart.set_index(
                "Risk Level"
            ),
            height=300
        )

        # ========================================================
        # TOP PRIORITY CASES
        # ========================================================

        st.subheader(
            "Top Priority Cases"
        )

        top_cases = (
            f7
            .sort_values(
                "Risk Score",
                ascending=False
            )
            .head(15)
            .copy()
        )

        top_display = top_cases[
            [
                "AI-Assisted Risk Score",
                "AI Anomaly Score",
                "AI Anomaly Flag",
                "Risk Level",
                "Actual Work ID",
                "State",
                "Constituency",
                "Work Description",
                "Review Priority"
            ]
        ].copy()

        top_display = top_display.rename(
            columns={
                "Actual Work ID": "Work ID",
                "AI-Assisted Risk Score": "AI Risk Score"
            }
        )

        top_display["AI Risk Score"] = top_display["AI Risk Score"].round(1)
        top_display["AI Anomaly Score"] = top_display["AI Anomaly Score"].round(1)

        st.dataframe(
            top_display,
            width="stretch",
            hide_index=True
        )

        with st.expander("🤖 How the AI layer works", expanded=True):
            st.markdown("""
**Machine-learning component:** an **Isolation Forest** is fitted without labels to the available work-level signals. It learns combinations that are unusual within the supplied snapshot.

**Signals used include:** completion age, recommendation-to-sanction time, explainable rule score, financial/cost/similarity/payment/vendor indicators and sanction/status signals.

**Final AI-assisted score:** 80% transparent monitoring score + 20% ML anomaly score.

Because the supplied data has **no labelled fraud outcome**, this is an **unsupervised anomaly detector**, not a fraud classifier. A flagged work is a review candidate, not proof of wrongdoing.
            """)

        # ========================================================
        # FILTERS
        # ========================================================

        st.subheader(
            "Filter Risk Cases"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            selected_risk = st.selectbox(
                "Risk Level",
                [
                    "All",
                    "High",
                    "Medium",
                    "Low"
                ],
                key="f7_final_risk"
            )

        with col2:

            states = sorted(
                [
                    str(x).strip()
                    for x in f7["State"]
                    .dropna()
                    .unique()
                    if str(x).strip()
                ]
            )

            selected_state = st.selectbox(
                "State",
                ["All"] + states,
                key="f7_final_state"
            )

        with col3:

            search_text = st.text_input(
                "Search Work / Work ID",
                key="f7_final_search"
            )

        filtered = f7.copy()

        if selected_risk != "All":

            filtered = filtered[
                filtered["Risk Level"]
                ==
                selected_risk
            ]

        if selected_state != "All":

            filtered = filtered[
                filtered["State"]
                ==
                selected_state
            ]

        if search_text.strip():

            q = search_text.strip().lower()

            filtered = filtered[
                filtered["Actual Work ID"]
                .astype(str)
                .str.lower()
                .str.contains(
                    q,
                    na=False
                )
                |
                filtered["Work Description"]
                .astype(str)
                .str.lower()
                .str.contains(
                    q,
                    na=False
                )
            ]

        # ========================================================
        # FILTERED RISK CASES
        # ========================================================

        st.subheader(
            "Risk Cases"
        )

        st.caption(
            f"{len(filtered):,} matching record(s) • showing up to 200"
        )

        if len(filtered) > 0:

            cases_display = (
                filtered
                .sort_values(
                    "AI-Assisted Risk Score",
                    ascending=False
                )
                .head(200)
                .copy()
            )

            cases_display = cases_display[
                [
                    "AI-Assisted Risk Score",
                    "AI Anomaly Score",
                    "AI Anomaly Flag",
                    "Risk Level",
                    "Actual Work ID",
                    "State",
                    "Constituency",
                    "Work Description",
                    "Review Priority"
                ]
            ].rename(
                columns={
                    "AI-Assisted Risk Score": "AI Risk Score",
                    "Actual Work ID": "Work ID"
                }
            )

            cases_display["AI Risk Score"] = (
                cases_display["AI Risk Score"]
                .round(1)
            )
            cases_display["AI Anomaly Score"] = (
                cases_display["AI Anomaly Score"]
                .round(1)
            )

            st.dataframe(
                cases_display,
                width="stretch",
                hide_index=True
            )

        else:

            st.info(
                "No risk cases match the selected filters. Try another Risk Level, State, or search term."
            )

        # ========================================================
        # INDIVIDUAL INVESTIGATION
        # ========================================================

        st.subheader(
            "🔎 Individual Risk Investigation"
        )

        if len(filtered) > 0:

            investigation_lookup = {
                row["F7 Internal ID"]: row
                for _, row
                in filtered.iterrows()
            }

            options = list(
                investigation_lookup.keys()
            )

            def display_work_id(internal_id):

                row = investigation_lookup.get(
                    internal_id
                )

                if row is None:

                    return "Work ID Unavailable"

                work_id = (
                    row["Actual Work ID"]
                )

                if work_id:

                    return work_id

                return "Work ID Unavailable"

            # Use a filter-specific widget key so the investigation selection
            # is reset whenever Risk Level / State / Search changes. This keeps
            # the investigation strictly tied to the currently filtered cases.
            filter_signature = (
                f"{selected_risk}|{selected_state}|{search_text.strip()}|"
                f"{len(filtered)}|"
                f"{filtered['F7 Internal ID'].iloc[0] if len(filtered) else 'none'}"
            )

            selected_internal = st.selectbox(
                "Select a work for investigation",
                options,
                format_func=display_work_id,
                key=f"f7_final_investigation_{filter_signature}"
            )

            row = investigation_lookup[
                selected_internal
            ]

            # ====================================================
            # OVERALL RISK
            # ====================================================

            st.markdown(
                "### Overall Risk Assessment"
            )

            r1, r2, r3, r4 = st.columns(4)

            with r1:

                st.metric(
                    "AI Risk Score",
                    f"{row['AI-Assisted Risk Score']:.1f}/100"
                )

            with r2:
                st.metric(
                    "ML Anomaly Score",
                    f"{row['AI Anomaly Score']:.1f}/100"
                )

            with r3:

                st.metric(
                    "Risk Level",
                    row["Risk Level"]
                )

            with r4:
                st.metric(
                    "Review Priority",
                    row["Review Priority"]
                )

            # ====================================================
            # WORK DETAILS
            # ====================================================

            st.markdown(
                "### Work Details"
            )

            d1, d2 = st.columns(2)

            with d1:

                st.write(
                    "**Work ID:**",
                    row["Actual Work ID"]
                    if row["Actual Work ID"]
                    else "Unavailable"
                )

                st.write(
                    "**State:**",
                    row["State"]
                )

                st.write(
                    "**Constituency:**",
                    row["Constituency"]
                )

            with d2:

                st.write(
                    "**Work Description:**",
                    row["Work Description"]
                    if row["Work Description"]
                    else "Description Unavailable"
                )

                st.write(
                    "**Work Status:**",
                    row["Work Status"]
                    if row["Work Status"]
                    else "Unavailable"
                )

            # ====================================================
            # SIGNAL BREAKDOWN
            # ====================================================

            st.markdown(
                "### Risk Signal Breakdown"
            )

            breakdown = pd.DataFrame(
                {
                    "Risk Signal": [
                        "Completion Delay",
                        "Financial Anomaly",
                        "Peer Cost Deviation",
                        "Similar / Duplicate Work",
                        "Payment Status",
                        "Vendor Concentration",
                        "Recommendation → Sanction",
                        "Ongoing Work Status"
                    ],

                    "Points": [
                        row["F1 Completion Points"],
                        row["F2 Financial Points"],
                        row["F3 Cost Points"],
                        row["F4 Similar Work Points"],
                        row["F5 Payment Points"],
                        row["F5 Vendor Points"],
                        row["F6 Sanction Points"],
                        row["F6 Status Points"]
                    ]
                }
            )

            breakdown["Points"] = (
                breakdown["Points"]
                .round(1)
            )

            st.dataframe(
                breakdown,
                width="stretch",
                hide_index=True
            )

            # ====================================================
            # WHY FLAGGED
            # ====================================================

            st.markdown(
                "### 🧠 Why is this work flagged?"
            )

            reasons = []

            # ----------------------------------------------------
            # COMPLETION
            # ----------------------------------------------------

            days_since = row[
                "Days Since Sanction"
            ]

            if (
                pd.notna(days_since)
                and
                days_since > 365
                and
                not row["Completed"]
            ):

                reasons.append(
                    f"The work has been sanctioned for "
                    f"{int(days_since)} days and is not marked "
                    "completed in the available status data."
                )

            # ----------------------------------------------------
            # SANCTION DELAY
            # ----------------------------------------------------

            rec_days = row[
                "Recommendation to Sanction Days"
            ]

            if (
                pd.notna(rec_days)
                and
                rec_days > 75
            ):

                reasons.append(
                    f"Recommendation to sanction took "
                    f"{int(rec_days)} days, beyond the "
                    "75-day benchmark."
                )

            # ----------------------------------------------------
            # ONGOING STATUS
            # ----------------------------------------------------

            if row["Ongoing Work"]:

                reasons.append(
                    "The current work status indicates an "
                    "ongoing or incomplete execution stage."
                )

            # ----------------------------------------------------
            # FINANCIAL ANOMALY
            # ----------------------------------------------------

            if row[
                "F2 Financial Points"
            ] > 0:

                reasons.append(
                    "The available fund amount shows an "
                    "unusual pattern compared with the "
                    "state-level financial distribution."
                )

            # ----------------------------------------------------
            # PEER COST
            # ----------------------------------------------------

            cost_deviation = row[
                "F3 Cost Deviation %"
            ]

            if (
                pd.notna(cost_deviation)
                and
                cost_deviation >= 25
            ):

                reasons.append(
                    f"The available fund amount is "
                    f"{cost_deviation:.1f}% above the "
                    "historical peer median for this work type."
                )

            # ----------------------------------------------------
            # SIMILAR WORK
            # ----------------------------------------------------

            similar_count = int(
                row[
                    "F4 Similar Work Count"
                ]
            )

            best_similarity = row[
                "F4 Best Similarity"
            ]

            if row[
                "F4 Exact Match"
            ]:

                reasons.append(
                    f"{similar_count} other work record(s) "
                    "have the same meaningful description "
                    "within the same State and Constituency. "
                    "This is a verification indicator, not "
                    "proof of duplication."
                )

            elif (
                pd.notna(best_similarity)
                and
                best_similarity >= 92
            ):

                reasons.append(
                    f"A highly similar work description was "
                    f"identified ({best_similarity:.1f}% similarity) "
                    "within the same State and Constituency. "
                    "This requires verification and does not "
                    "establish duplication."
                )

            # ----------------------------------------------------
            # PAYMENT
            # ----------------------------------------------------

            if row[
                "F5 Payment Points"
            ] > 0:

                payment_status = row[
                    "Payment Status"
                ]

                reasons.append(
                    "Payment status requires additional "
                    f"review ({payment_status})."
                )

            # ----------------------------------------------------
            # VENDOR
            # ----------------------------------------------------

            if row[
                "F5 Vendor Points"
            ] > 0:

                vendor_name = row[
                    "Vendor Name"
                ]

                vendor_count = int(
                    row[
                        "Vendor Work Count"
                    ]
                )

                if vendor_name:

                    reasons.append(
                        f"The associated vendor appears across "
                        f"{vendor_count} works in the available "
                        "dataset."
                    )

            # ====================================================
            # DISPLAY
            # ====================================================

            if len(reasons) == 0:

                st.success(
                    "No major risk signals were identified "
                    "under the current screening rules."
                )

            else:

                for reason in reasons:

                    st.write(
                        "• " + reason
                    )

            # ====================================================
            # INTERPRETATION
            # ====================================================

            st.info(
                "This risk score is a decision-support indicator. "
                "It combines multiple analytical signals to "
                "prioritize cases for administrative review. "
                "A high score does not establish fraud, misuse, "
                "duplication or wrongdoing."
            )

        else:

            st.info(
                "No works match the selected filters."
            )

        # ========================================================
        # METHODOLOGY
        # ========================================================

        with st.expander(
            "Methodology"
        ):

            st.write(
                """
                The combined risk engine integrates analytical
                signals from Features 1–6:

                • Completion delay
                • Financial / fund anomaly
                • Historical peer cost deviation
                • Similar or potentially duplicate work descriptions
                • Payment status
                • Vendor concentration
                • Recommendation → sanction timeline
                • Ongoing work status

                Maximum raw score: 95 points.

                The raw score is normalized to a 0–100 scale.

                Risk levels:

                0–39   → Low
                40–69  → Medium
                70–100 → High

                Financial values such as ***** are treated as
                unavailable rather than zero.

                Similar work descriptions are treated as review
                indicators. Similarity does not establish that
                two physical works are duplicates.

                The final score is intended for prioritization
                and administrative decision support. It is not
                a legal or fraud determination.
                """
            )

        # ========================================================
        # FOOTER
        # ========================================================

        st.caption(
            "Feature 7 • Combined AI Risk Score & Explainable "
            "Insights • MPLADS Decision-Support Prototype"
        )


    except Exception as e:

        st.error(
            f"Feature 7 could not be loaded: {e}"
        )


    # ============================================================

def feature_8():
    # FEATURE 8 — TREND ANALYSIS
    # ============================================================

    st.header("📈 Trend Analysis")
    st.caption(
        "Historical activity trends across MPLADS datasets for recommendations, "
        "sanctions, completions and available financial records."
    )

    # ------------------------------------------------------------
    # FILE PATHS
    # ------------------------------------------------------------

    F8_RECOMMENDED_FILE = Path(DATA_DIR) / "Works Recommended.csv"
    F8_SANCTIONED_FILE = Path(DATA_DIR) / "Works Sanctioned (1).csv"
    F8_COMPLETED_FILE = Path(DATA_DIR) / "Works Completed (1).csv"
    F8_EXPENDITURE_FILE = Path(DATA_DIR) / (
        "Expenditure on Completed and On-going Works as on Date.csv"
    )


    # ------------------------------------------------------------
    # LOAD DATA
    # ------------------------------------------------------------

    @st.cache_data
    def load_feature8_data():

        recommended = pd.read_csv(
            F8_RECOMMENDED_FILE,
            low_memory=False
        )

        sanctioned = pd.read_csv(
            F8_SANCTIONED_FILE,
            low_memory=False
        )

        completed = pd.read_csv(
            F8_COMPLETED_FILE,
            low_memory=False
        )

        expenditure = pd.read_csv(
            F8_EXPENDITURE_FILE,
            low_memory=False
        )

        return recommended, sanctioned, completed, expenditure


    try:
        rec8, sanc8, comp8, exp8 = load_feature8_data()

    except Exception as e:
        st.error(f"Unable to load Feature 8 datasets: {e}")
        st.stop()


    # ------------------------------------------------------------
    # HELPER FUNCTIONS
    # ------------------------------------------------------------

    def find_column(df, possible_names):

        for name in possible_names:

            if name in df.columns:
                return name

        return None


    def clean_text(value):

        if pd.isna(value):
            return ""

        value = str(value).strip()

        if value.lower() in ["nan", "none", "null", ""]:
            return ""

        return value


    def extract_year(series):

        dates = pd.to_datetime(
            series,
            errors="coerce",
            dayfirst=False
        )

        return dates.dt.year


    def get_state_column(df):

        return find_column(
            df,
            [
                "State",
                "STATE",
                "State Name"
            ]
        )


    def get_year_column(df):

        return find_column(
            df,
            [
                "Recommended date",
                "Recommended Date",
                "Sanction Date",
                "Completion Date"
            ]
        )


    # ------------------------------------------------------------
    # PREPARE RECOMMENDED DATA
    # ------------------------------------------------------------

    rec8 = rec8.copy()

    rec_state_col = get_state_column(rec8)

    if "Recommended date" in rec8.columns:

        rec8["_Trend Year"] = extract_year(
            rec8["Recommended date"]
        )

    elif "Recommended Date" in rec8.columns:

        rec8["_Trend Year"] = extract_year(
            rec8["Recommended Date"]
        )

    else:

        rec8["_Trend Year"] = pd.NA


    # ------------------------------------------------------------
    # PREPARE SANCTIONED DATA
    # ------------------------------------------------------------

    sanc8 = sanc8.copy()

    sanc_state_col = get_state_column(sanc8)

    if "Sanction Date" in sanc8.columns:

        sanc8["_Trend Year"] = extract_year(
            sanc8["Sanction Date"]
        )

    else:

        sanc8["_Trend Year"] = pd.NA


    # ------------------------------------------------------------
    # PREPARE COMPLETED DATA
    # ------------------------------------------------------------

    comp8 = comp8.copy()

    comp_state_col = get_state_column(comp8)

    if "Completion Date" in comp8.columns:

        comp8["_Trend Year"] = extract_year(
            comp8["Completion Date"]
        )

    else:

        comp8["_Trend Year"] = pd.NA


    # ------------------------------------------------------------
    # PREPARE EXPENDITURE DATA
    # ------------------------------------------------------------

    exp8 = exp8.copy()

    exp_state_col = get_state_column(exp8)

    if "Fund Disbursed Amount" in exp8.columns:

        exp8["_Fund Amount"] = pd.to_numeric(
            exp8["Fund Disbursed Amount"],
            errors="coerce"
        )

    else:

        exp8["_Fund Amount"] = pd.NA

    exp8["_Trend Year"] = pd.NA

    if "Work ID" in exp8.columns:

        work_id_text = (
            exp8["Work ID"]
            .astype(str)
            .str.extract(r"(\d{4})-\d{4}", expand=False)
        )

        exp8["_Trend Year"] = pd.to_numeric(
            work_id_text,
            errors="coerce"
        )


    # ------------------------------------------------------------
    # DATASET COVERAGE NOTE
    # ------------------------------------------------------------

    st.info(
        "Dataset coverage note: Recommended, Sanctioned and Completed datasets "
        "are separate source files. The provided snapshot does not contain a "
        "reliable common work-level identifier between the Sanctioned and "
        "Completed datasets. Therefore, these counts are presented as "
        "dataset activity counts and are not treated as one sequential workflow."
    )


    # ============================================================
    # TREND FILTERS
    # ============================================================

    st.subheader("🔎 Trend Filters")

    all_years = set()

    for df in [rec8, sanc8, comp8]:

        if "_Trend Year" in df.columns:

            years = pd.to_numeric(
                df["_Trend Year"],
                errors="coerce"
            ).dropna()

            all_years.update(
                years.astype(int).tolist()
            )

    all_years = sorted(all_years)

    filter_col1, filter_col2 = st.columns(2)

    with filter_col1:

        selected_year = st.selectbox(
            "Year",
            ["All Years"] + all_years,
            key="f8_year_filter"
        )

    with filter_col2:

        all_states = set()

        for df in [rec8, sanc8, comp8]:

            state_col = get_state_column(df)

            if state_col:

                values = (
                    df[state_col]
                    .dropna()
                    .astype(str)
                    .str.strip()
                )

                all_states.update(
                    values[values != ""].tolist()
                )

        all_states = sorted(all_states)

        selected_state = st.selectbox(
            "State",
            ["All States"] + all_states,
            key="f8_state_filter"
        )


    # ============================================================
    # APPLY FILTERS
    # ============================================================

    def apply_trend_filters(df, state_col):

        result = df.copy()

        if selected_year != "All Years":

            result = result[
                pd.to_numeric(
                    result["_Trend Year"],
                    errors="coerce"
                ) == int(selected_year)
            ]

        if (
            selected_state != "All States"
            and state_col is not None
        ):

            result = result[
                result[state_col]
                .astype(str)
                .str.strip()
                .eq(selected_state)
            ]

        return result


    rec_filtered = apply_trend_filters(
        rec8,
        rec_state_col
    )

    sanc_filtered = apply_trend_filters(
        sanc8,
        sanc_state_col
    )

    comp_filtered = apply_trend_filters(
        comp8,
        comp_state_col
    )


    # ============================================================
    # DATASET ACTIVITY OVERVIEW
    # ============================================================

    st.subheader("📊 Dataset Activity Overview")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Recommended Records",
            f"{len(rec_filtered):,}"
        )

    with m2:
        st.metric(
            "Sanctioned Records",
            f"{len(sanc_filtered):,}"
        )

    with m3:
        st.metric(
            "Completed Records",
            f"{len(comp_filtered):,}"
        )

    usable_fund_count = exp8["_Fund Amount"].notna().sum()

    with m4:
        st.metric(
            "Usable Fund Records",
            f"{usable_fund_count:,}"
        )


    st.caption(
        "These figures represent records available in each respective "
        "dataset and should not be interpreted as linked stage-by-stage totals."
    )


    # ============================================================
    # YEAR-WISE WORK ACTIVITY
    # ============================================================

    st.subheader("📅 Work Activity Trend")

    yearly_rec = (
        rec8.dropna(subset=["_Trend Year"])
        .groupby("_Trend Year")
        .size()
        .rename("Recommended")
    )

    yearly_sanc = (
        sanc8.dropna(subset=["_Trend Year"])
        .groupby("_Trend Year")
        .size()
        .rename("Sanctioned")
    )

    yearly_comp = (
        comp8.dropna(subset=["_Trend Year"])
        .groupby("_Trend Year")
        .size()
        .rename("Completed")
    )

    yearly_activity = pd.concat(
        [
            yearly_rec,
            yearly_sanc,
            yearly_comp
        ],
        axis=1
    ).fillna(0)

    yearly_activity.index = (
        pd.to_numeric(
            yearly_activity.index,
            errors="coerce"
        )
    )

    yearly_activity = (
        yearly_activity
        .dropna()
        .sort_index()
    )

    yearly_activity.index = (
        yearly_activity.index
        .astype(int)
        .astype(str)
    )

    st.line_chart(
        yearly_activity[
            [
                "Recommended",
                "Sanctioned",
                "Completed"
            ]
        ]
    )

    display_yearly = yearly_activity.copy()

    display_yearly.index.name = "Year"

    display_yearly = display_yearly.astype(int)

    st.dataframe(
        display_yearly,
        width="stretch"
    )


    # ============================================================
    # FUND DISBURSEMENT TREND
    # ============================================================

    st.subheader("💰 Available Fund Disbursement Trend")

    if "_Trend Year" in exp8.columns:

        fund_trend = (
            exp8.dropna(subset=["_Trend Year"])
            .dropna(subset=["_Fund Amount"])
            .groupby("_Trend Year")["_Fund Amount"]
            .sum()
            .sort_index()
        )

    else:

        fund_trend = pd.Series(dtype=float)


    if len(fund_trend) > 0:

        fund_trend.index = fund_trend.index.astype(int).astype(str)

        st.line_chart(
            fund_trend
        )

        fund_table = fund_trend.to_frame(
            "Total Fund Disbursed"
        )

        st.dataframe(
            fund_table,
            width="stretch"
        )

    else:

        st.warning(
            "Fund disbursement trend is unavailable because the provided "
            "expenditure dataset does not contain usable numeric fund amounts."
        )


    # ============================================================
    # STATE-WISE WORK ACTIVITY
    # ============================================================

    st.subheader("🗺️ State-wise Work Activity")

    state_rec = pd.Series(dtype=int)
    state_sanc = pd.Series(dtype=int)
    state_comp = pd.Series(dtype=int)

    if rec_state_col:

        state_rec = (
            rec_filtered
            .groupby(rec_state_col)
            .size()
            .rename("Recommended")
        )

    if sanc_state_col:

        state_sanc = (
            sanc_filtered
            .groupby(sanc_state_col)
            .size()
            .rename("Sanctioned")
        )

    if comp_state_col:

        state_comp = (
            comp_filtered
            .groupby(comp_state_col)
            .size()
            .rename("Completed")
        )

    state_activity = pd.concat(
        [
            state_rec,
            state_sanc,
            state_comp
        ],
        axis=1
    ).fillna(0)

    state_activity = state_activity.sort_index()

    state_activity = state_activity.astype(int)

    st.bar_chart(
        state_activity[
            [
                "Recommended",
                "Sanctioned",
                "Completed"
            ]
        ]
    )

    st.dataframe(
        state_activity,
        width="stretch"
    )


    # ============================================================
    # AUTOMATED TREND INSIGHTS
    # ============================================================

    st.subheader("🧠 Automated Trend Insights")

    insights = []


    # ------------------------------------------------------------
    # SANCTIONED TREND
    # ------------------------------------------------------------

    if len(yearly_sanc) >= 2:

        sanctioned_years = yearly_sanc.sort_index()

        latest_year = sanctioned_years.index[-1]
        previous_year = sanctioned_years.index[-2]

        latest_value = sanctioned_years.iloc[-1]
        previous_value = sanctioned_years.iloc[-2]

        if previous_value > 0:

            change_pct = (
                (latest_value - previous_value)
                / previous_value
            ) * 100

            if change_pct > 0:

                insights.append(
                    f"Sanctioned work activity increased by "
                    f"{change_pct:.1f}% from {int(previous_year)} "
                    f"to {int(latest_year)}."
                )

            elif change_pct < 0:

                insights.append(
                    f"Sanctioned work activity decreased by "
                    f"{abs(change_pct):.1f}% from {int(previous_year)} "
                    f"to {int(latest_year)}."
                )

            else:

                insights.append(
                    f"Sanctioned work activity remained stable "
                    f"from {int(previous_year)} to {int(latest_year)}."
                )


    # ------------------------------------------------------------
    # HIGHEST SANCTIONED STATE
    # ------------------------------------------------------------

    if len(state_sanc) > 0:

        top_state = state_sanc.idxmax()
        top_value = state_sanc.max()

        insights.append(
            f"{top_state} has the highest number of sanctioned "
            f"records in the selected dataset coverage "
            f"({top_value:,})."
        )


    # ------------------------------------------------------------
    # HIGHEST COMPLETED STATE
    # ------------------------------------------------------------

    if len(state_comp) > 0:

        top_completed_state = state_comp.idxmax()
        top_completed_value = state_comp.max()

        insights.append(
            f"{top_completed_state} has the highest number of "
            f"completed records in the completed-work dataset "
            f"({top_completed_value:,})."
        )


    # ------------------------------------------------------------
    # FUND DATA AVAILABILITY
    # ------------------------------------------------------------

    if usable_fund_count == 0:

        insights.append(
            "Fund-disbursement trend analysis is currently limited "
            "because the expenditure dataset contains no usable "
            "numeric fund amounts."
        )

    else:

        insights.append(
            f"{usable_fund_count:,} expenditure records contain "
            "usable numeric fund amounts for financial trend analysis."
        )


    # ------------------------------------------------------------
    # SHOW INSIGHTS
    # ------------------------------------------------------------

    if len(insights) > 0:

        for insight in insights:

            st.write(
                "• " + insight
            )

    else:

        st.info(
            "Insufficient historical data is available to generate "
            "automated trend insights."
        )


    # ============================================================
    # METHODOLOGY
    # ============================================================

    with st.expander("📘 Methodology & Interpretation"):

        st.markdown(
            """
    ### Trend Analysis Methodology

    **1. Dataset-specific activity**

    The system separately analyzes:

    - Recommended works
    - Sanctioned works
    - Completed works
    - Available financial records

    These datasets are not assumed to represent the same work population.

    **2. Year extraction**

    Activity is grouped by the year available in the corresponding
    date field:

    - Recommended → Recommended Date
    - Sanctioned → Sanction Date
    - Completed → Completion Date

    **3. State-level analysis**

    Records are grouped by State to identify differences in work activity
    across geographic regions.

    **4. Financial trend**

    Fund-disbursement trends are calculated only when the source dataset
    contains usable numeric fund amounts.

    **5. Interpretation**

    Trend analysis identifies changes in activity and geographic
    concentration. It does not by itself indicate fraud, misuse or
    non-compliance.

    ### Important Data Coverage Note

    The supplied Sanctioned and Completed datasets do not contain a
    reliable common work-level identifier in the provided snapshot.

    Therefore, the system does **not** artificially force the datasets
    into a single Recommended → Sanctioned → Completed workflow.

    This preserves the integrity of the source data and avoids
    misrepresenting dataset coverage as work-level outcomes.
            """
        )


    # ============================================================
    # SAFE NOTE
    # ============================================================

    st.caption(
        "Analytical indicators are intended for monitoring and administrative "
        "review. They do not establish fraud, misuse or wrongdoing."
    )

    # ============================================================

def feature_9():
    # FEATURE 9 — PREDICTIVE / EARLY-WARNING INSIGHTS
    # ============================================================

    st.header("🔮 Predictive & Early-Warning Insights")
    st.caption(
        "Identify ongoing works approaching future monitoring thresholds "
        "so that authorities can take timely action."
    )

    # ------------------------------------------------------------
    # FILE
    # ------------------------------------------------------------

    F9_FILE = Path(DATA_DIR) / "Works Sanctioned (1).csv"


    # ============================================================
    # LOAD DATA
    # ============================================================

    @st.cache_data
    def load_feature9():

        return pd.read_csv(
            F9_FILE,
            low_memory=False
        )


    try:

        f9 = load_feature9()

    except Exception as e:

        st.error(f"Unable to load Feature 9 dataset: {e}")
        st.stop()


    # ============================================================
    # HELPER FUNCTIONS
    # ============================================================

    def f9_find_column(df, names):

        for name in names:

            if name in df.columns:
                return name

        return None


    def f9_clean(value):

        if pd.isna(value):
            return ""

        value = str(value).strip()

        if value.lower() in [
            "",
            "nan",
            "none",
            "null"
        ]:
            return ""

        return value


    # ============================================================
    # IDENTIFY COLUMNS
    # ============================================================

    f9_state_col = f9_find_column(
        f9,
        [
            "State",
            "STATE",
            "State Name"
        ]
    )

    f9_const_col = f9_find_column(
        f9,
        [
            "Constituency",
            "CONSTITUENCY"
        ]
    )

    f9_mp_col = f9_find_column(
        f9,
        [
            "Hon’ble Member",
            "Hon'ble Member",
            "Hon’ble Members of Parliament",
            "Hon'ble Members of Parliament"
        ]
    )

    f9_work_col = f9_find_column(
        f9,
        [
            "Work",
            "WORK"
        ]
    )

    f9_desc_col = f9_find_column(
        f9,
        [
            "Work Description",
            "WORK DESCRIPTION"
        ]
    )

    f9_sanction_col = f9_find_column(
        f9,
        [
            "Sanction Date",
            "Sanction date"
        ]
    )

    f9_status_col = f9_find_column(
        f9,
        [
            "Work Status",
            "WORK STATUS"
        ]
    )

    f9_category_col = f9_find_column(
        f9,
        [
            "Work Category",
            "Work category",
            "WORK CATEGORY"
        ]
    )


    # ============================================================
    # DATE PROCESSING
    # ============================================================

    if f9_sanction_col:

        f9["_Sanction Date"] = pd.to_datetime(
            f9[f9_sanction_col],
            errors="coerce"
        )

    else:

        f9["_Sanction Date"] = pd.NaT


    today_f9 = pd.Timestamp.today().normalize()

    f9["Days Since Sanction"] = (
        today_f9 - f9["_Sanction Date"]
    ).dt.days


    # ============================================================
    # STATUS PROCESSING
    # ============================================================

    if f9_status_col:

        f9["_Status"] = (
            f9[f9_status_col]
            .fillna("")
            .astype(str)
            .str.strip()
        )

    else:

        f9["_Status"] = ""


    f9["_Status Lower"] = (
        f9["_Status"]
        .str.lower()
    )


    # ============================================================
    # COMPLETION DETECTION
    # ============================================================

    completion_words = [
        "completed",
        "complete",
        "completion",
        "work completed"
    ]


    f9["_Is Completed"] = (
        f9["_Status Lower"]
        .apply(
            lambda x:
            any(word in x for word in completion_words)
        )
    )


    # ============================================================
    # EARLY-WARNING FORECAST
    # ============================================================

    def f9_forecast(row):

        days = row["Days Since Sanction"]

        status = row["_Status Lower"]


        # --------------------------------------------------------
        # MISSING DATE
        # --------------------------------------------------------

        if pd.isna(days):

            return pd.Series(
                [
                    "Data Review",
                    None,
                    "Sanction date unavailable"
                ]
            )


        days = int(days)


        # --------------------------------------------------------
        # COMPLETED
        # --------------------------------------------------------

        if row["_Is Completed"]:

            return pd.Series(
                [
                    "Completed",
                    None,
                    "Work is marked as completed"
                ]
            )


        # --------------------------------------------------------
        # CALCULATE DISTANCE FROM ONE-YEAR BENCHMARK
        # --------------------------------------------------------

        days_difference = 365 - days


        # --------------------------------------------------------
        # ALREADY BEYOND ONE YEAR
        # --------------------------------------------------------

        if days > 365:

            passed_by = days - 365

            return pd.Series(
                [
                    "Attention Required",
                    -passed_by,
                    (
                        f"Work has crossed the one-year completion "
                        f"benchmark by {passed_by:,} days and is not "
                        f"marked as completed"
                    )
                ]
            )


        # --------------------------------------------------------
        # EXACTLY 365 DAYS
        # --------------------------------------------------------

        if days == 365:

            return pd.Series(
                [
                    "Attention Required",
                    0,
                    "Work has reached the one-year completion benchmark "
                    "and is not marked as completed"
                ]
            )


        # --------------------------------------------------------
        # WITHIN 30 DAYS
        # --------------------------------------------------------

        if days >= 335:

            return pd.Series(
                [
                    "Critical Upcoming",
                    days_difference,
                    (
                        f"Work is {days_difference:,} days away from "
                        "the one-year completion benchmark"
                    )
                ]
            )


        # --------------------------------------------------------
        # WITHIN 90 DAYS
        # --------------------------------------------------------

        if days >= 275:

            return pd.Series(
                [
                    "Upcoming Attention",
                    days_difference,
                    (
                        f"Work is {days_difference:,} days away from "
                        "the one-year completion benchmark"
                    )
                ]
            )


        # --------------------------------------------------------
        # EMERGING WARNING
        # --------------------------------------------------------

        if days >= 180:

            administrative_status = any(
                word in status
                for word in [
                    "pending",
                    "process",
                    "vendor",
                    "tender",
                    "approval",
                    "identification"
                ]
            )


            if administrative_status:

                return pd.Series(
                    [
                        "Emerging Warning",
                        days_difference,
                        (
                            "Work has been ongoing for an extended "
                            "period and its current status indicates "
                            "an administrative or execution stage"
                        )
                    ]
                )


            return pd.Series(
                [
                    "Monitoring",
                    days_difference,
                    (
                        "Work has been ongoing for an extended period "
                        "and should continue to be monitored"
                    )
                ]
            )


        # --------------------------------------------------------
        # STABLE
        # --------------------------------------------------------

        return pd.Series(
            [
                "Stable",
                days_difference,
                (
                    "Work is currently below the defined "
                    "early-warning monitoring window"
                )
            ]
        )


    f9[
        [
            "Forecast Status",
            "Days Until 365",
            "Forecast Explanation"
        ]
    ] = f9.apply(
        f9_forecast,
        axis=1
    )


    # ============================================================
    # HUMAN-READABLE BENCHMARK STATUS
    # ============================================================

    def f9_benchmark_text(row):

        days = row["Days Since Sanction"]

        if pd.isna(days):

            return "Unavailable"


        days = int(days)


        if days < 365:

            remaining = 365 - days

            return f"{remaining:,} days remaining"


        elif days == 365:

            return "Benchmark reached"


        else:

            passed = days - 365

            return f"Passed by {passed:,} days"


    f9["Benchmark Timeline"] = f9.apply(
        f9_benchmark_text,
        axis=1
    )


    # ============================================================
    # OVERVIEW
    # ============================================================

    st.subheader("🚨 Early-Warning Overview")

    total_f9 = len(f9)

    attention_f9 = (
        f9["Forecast Status"]
        == "Attention Required"
    ).sum()

    critical_f9 = (
        f9["Forecast Status"]
        == "Critical Upcoming"
    ).sum()

    upcoming_f9 = (
        f9["Forecast Status"]
        == "Upcoming Attention"
    ).sum()

    emerging_f9 = (
        f9["Forecast Status"]
        == "Emerging Warning"
    ).sum()


    c1, c2, c3, c4, c5 = st.columns(5)


    with c1:

        st.metric(
            "Works Monitored",
            f"{total_f9:,}"
        )


    with c2:

        st.metric(
            "Attention Required",
            f"{attention_f9:,}"
        )


    with c3:

        st.metric(
            "Critical Upcoming",
            f"{critical_f9:,}"
        )


    with c4:

        st.metric(
            "Upcoming Attention",
            f"{upcoming_f9:,}"
        )


    with c5:

        st.metric(
            "Emerging Warning",
            f"{emerging_f9:,}"
        )


    # ============================================================
    # FORECAST DISTRIBUTION
    # ============================================================

    st.subheader("📊 Forecast Status Distribution")

    forecast_distribution = (
        f9["Forecast Status"]
        .value_counts()
    )

    st.bar_chart(
        forecast_distribution
    )


    # ============================================================
    # UPCOMING ATTENTION
    # ============================================================

    st.subheader(
        "📅 Works Approaching the One-Year Benchmark"
    )

    approaching = f9[
        f9["Forecast Status"].isin(
            [
                "Critical Upcoming",
                "Upcoming Attention"
            ]
        )
    ].copy()


    if len(approaching) > 0:

        approaching = approaching.sort_values(
            "Days Until 365",
            ascending=True
        )


        approaching_columns = []


        if f9_state_col:

            approaching_columns.append(
                f9_state_col
            )


        if f9_const_col:

            approaching_columns.append(
                f9_const_col
            )


        if f9_category_col:

            approaching_columns.append(
                f9_category_col
            )


        if f9_work_col:

            approaching_columns.append(
                f9_work_col
            )


        approaching_columns.extend(
            [
                "Days Since Sanction",
                "Benchmark Timeline",
                "Forecast Status",
                "Forecast Explanation"
            ]
        )


        approaching_columns = [
            c
            for c in approaching_columns
            if c in approaching.columns
        ]


        st.dataframe(
            approaching[
                approaching_columns
            ].head(100),
            width="stretch",
            hide_index=True
        )


    else:

        st.success(
            "No ongoing works are currently within the defined "
            "upcoming-attention window."
        )


    # ============================================================
    # EMERGING WARNING SIGNALS
    # ============================================================

    st.subheader("🌱 Emerging Warning Signals")

    emerging_cases = f9[
        f9["Forecast Status"]
        == "Emerging Warning"
    ].copy()


    if len(emerging_cases) > 0:

        emerging_cases = emerging_cases.sort_values(
            "Days Since Sanction",
            ascending=False
        )


        emerging_columns = []


        if f9_state_col:

            emerging_columns.append(
                f9_state_col
            )


        if f9_const_col:

            emerging_columns.append(
                f9_const_col
            )


        if f9_category_col:

            emerging_columns.append(
                f9_category_col
            )


        if f9_work_col:

            emerging_columns.append(
                f9_work_col
            )


        emerging_columns.extend(
            [
                "Days Since Sanction",
                "Benchmark Timeline",
                "Forecast Explanation"
            ]
        )


        emerging_columns = [
            c
            for c in emerging_columns
            if c in emerging_cases.columns
        ]


        st.dataframe(
            emerging_cases[
                emerging_columns
            ].head(100),
            width="stretch",
            hide_index=True
        )


    else:

        st.info(
            "No emerging warning cases were identified "
            "under the current screening rules."
        )


    # ============================================================
    # FILTERS
    # ============================================================

    st.subheader("🔎 Early-Warning Filters")

    f1, f2, f3 = st.columns(3)


    with f1:

        forecast_options = [
            "All Statuses",
            "Attention Required",
            "Critical Upcoming",
            "Upcoming Attention",
            "Emerging Warning",
            "Monitoring",
            "Stable",
            "Completed",
            "Data Review"
        ]


        selected_forecast = st.selectbox(
            "Forecast Status",
            forecast_options,
            key="f9_forecast_filter"
        )


    with f2:

        if f9_state_col:

            f9_states = sorted(
                [
                    x
                    for x in
                    f9[f9_state_col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    .unique()
                    if x
                ]
            )

        else:

            f9_states = []


        selected_f9_state = st.selectbox(
            "State",
            ["All States"] + f9_states,
            key="f9_state_filter"
        )


    with f3:

        f9_search = st.text_input(
            "Search Work / Description",
            key="f9_search"
        )


    # ============================================================
    # APPLY FILTERS
    # ============================================================

    f9_filtered = f9.copy()


    if selected_forecast != "All Statuses":

        f9_filtered = f9_filtered[
            f9_filtered["Forecast Status"]
            == selected_forecast
        ]


    if (
        selected_f9_state != "All States"
        and f9_state_col
    ):

        f9_filtered = f9_filtered[
            f9_filtered[f9_state_col]
            .fillna("")
            .astype(str)
            .str.strip()
            == selected_f9_state
        ]


    if f9_search.strip():

        search_value = (
            f9_search
            .strip()
            .lower()
        )


        search_mask = pd.Series(
            False,
            index=f9_filtered.index
        )


        if f9_work_col:

            search_mask = (
                search_mask
                |
                f9_filtered[f9_work_col]
                .fillna("")
                .astype(str)
                .str.lower()
                .str.contains(
                    search_value,
                    na=False
                )
            )


        if f9_desc_col:

            search_mask = (
                search_mask
                |
                f9_filtered[f9_desc_col]
                .fillna("")
                .astype(str)
                .str.lower()
                .str.contains(
                    search_value,
                    na=False
                )
            )


        f9_filtered = f9_filtered[
            search_mask
        ]


    # ============================================================
    # FILTERED CASES
    # ============================================================

    st.subheader("📋 Filtered Early-Warning Cases")

    filtered_columns = []


    if f9_state_col:

        filtered_columns.append(
            f9_state_col
        )


    if f9_const_col:

        filtered_columns.append(
            f9_const_col
        )


    if f9_category_col:

        filtered_columns.append(
            f9_category_col
        )


    if f9_work_col:

        filtered_columns.append(
            f9_work_col
        )


    filtered_columns.extend(
        [
            "Days Since Sanction",
            "Benchmark Timeline",
            "Forecast Status",
            "Forecast Explanation"
        ]
    )


    filtered_columns = [
        c
        for c in filtered_columns
        if c in f9_filtered.columns
    ]


    if len(f9_filtered) > 0:

        st.dataframe(
            f9_filtered[
                filtered_columns
            ].sort_values(
                "Days Since Sanction",
                ascending=False
            ).head(100),
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            "No works match the selected filters."
        )


    # ============================================================
    # INDIVIDUAL INVESTIGATION
    # ============================================================

    st.subheader("🔍 Investigate a Work")

    investigation_source = (
        f9_filtered
        .sort_values(
            "Days Since Sanction",
            ascending=False
        )
    )


    if len(investigation_source) == 0:

        st.info(
            "No works match the selected filters."
        )

    else:

        investigation_labels = []

        investigation_lookup = {}


        for idx, row in investigation_source.iterrows():

            state_value = (
                f9_clean(
                    row[f9_state_col]
                )
                if f9_state_col
                else "Unknown State"
            )


            work_value = (
                f9_clean(
                    row[f9_work_col]
                )
                if f9_work_col
                else "Work unavailable"
            )


            label = (
                f"{state_value} | "
                f"{work_value[:100]} | "
                f"{row['Forecast Status']}"
            )


            investigation_labels.append(
                label
            )

            investigation_lookup[
                label
            ] = idx


        selected_work = st.selectbox(
            "Select Work",
            investigation_labels,
            key="f9_investigation"
        )


        selected_idx = investigation_lookup[
            selected_work
        ]


        selected_row = f9.loc[
            selected_idx
        ]


        # --------------------------------------------------------
        # DETAILS
        # --------------------------------------------------------

        d1, d2, d3 = st.columns(3)


        with d1:

            st.write("**State**")

            st.write(
                f9_clean(
                    selected_row[f9_state_col]
                )
                if f9_state_col
                else "Unavailable"
            )


            st.write("**Constituency**")

            st.write(
                f9_clean(
                    selected_row[f9_const_col]
                )
                if f9_const_col
                else "Unavailable"
            )


        with d2:

            st.write("**Current Work Status**")

            st.write(
                f9_clean(
                    selected_row[f9_status_col]
                )
                if f9_status_col
                else "Unavailable"
            )


            st.write("**Days Since Sanction**")

            days_value = selected_row[
                "Days Since Sanction"
            ]


            if pd.isna(days_value):

                st.write("Unavailable")

            else:

                st.write(
                    f"{int(days_value):,} days"
                )


        with d3:

            st.write("**Forecast Status**")

            st.write(
                selected_row[
                    "Forecast Status"
                ]
            )


            st.write(
                "**One-Year Benchmark Status**"
            )

            st.write(
                selected_row[
                    "Benchmark Timeline"
                ]
            )


        # --------------------------------------------------------
        # WORK
        # --------------------------------------------------------

        if f9_work_col:

            st.write("**Work**")

            st.write(
                f9_clean(
                    selected_row[f9_work_col]
                )
            )


        if f9_desc_col:

            description = f9_clean(
                selected_row[f9_desc_col]
            )


            if description:

                st.write(
                    "**Work Description**"
                )

                st.write(
                    description
                )


        # --------------------------------------------------------
        # FORECAST EXPLANATION
        # --------------------------------------------------------

        st.write(
            "**Early-Warning Explanation**"
        )

        st.info(
            selected_row[
                "Forecast Explanation"
            ]
        )


    # ============================================================
    # AUTOMATED EARLY-WARNING INSIGHTS
    # ============================================================

    st.subheader(
        "🧠 Automated Early-Warning Insights"
    )

    forecast_insights = []


    if attention_f9 > 0:

        forecast_insights.append(
            f"{attention_f9:,} ongoing works have crossed "
            "the one-year completion benchmark without being "
            "marked completed."
        )


    if critical_f9 > 0:

        forecast_insights.append(
            f"{critical_f9:,} ongoing works are within "
            "30 days of the one-year benchmark."
        )


    if upcoming_f9 > 0:

        forecast_insights.append(
            f"{upcoming_f9:,} ongoing works are within "
            "90 days of the one-year benchmark."
        )


    if emerging_f9 > 0:

        forecast_insights.append(
            f"{emerging_f9:,} works show emerging warning "
            "signals based on extended duration and current "
            "administrative/execution status."
        )


    if not forecast_insights:

        forecast_insights.append(
            "No major early-warning concentration was "
            "detected under the current screening rules."
        )


    for insight in forecast_insights:

        st.write(
            "• " + insight
        )


    # ============================================================
    # METHODOLOGY
    # ============================================================

    with st.expander(
        "📘 Methodology & Interpretation"
    ):

        st.markdown(
            """
    ### Predictive / Early-Warning Methodology

    This module functions as an **early-warning mechanism**.

    Unlike Feature 7, which calculates the current combined risk
    of a work, Feature 9 focuses on the work's **future timeline**
    and identifies works approaching important monitoring thresholds.

    ### Forecast Logic

    **Stable**

    Work is below the early-warning monitoring window.

    **Monitoring**

    Work has been ongoing for an extended period and should continue
    to be observed.

    **Emerging Warning**

    Work has been ongoing for 180+ days and its current status may
    indicate an administrative or execution stage requiring attention.

    **Upcoming Attention**

    Work is within approximately 90 days of the one-year benchmark.

    **Critical Upcoming**

    Work is within approximately 30 days of the one-year benchmark.

    **Attention Required**

    Work has crossed the one-year benchmark and is not marked
    as completed.

    ### Benchmark Timeline

    The dashboard explicitly shows the distance from the one-year
    benchmark:

    - Days remaining
    - Benchmark reached
    - Days already passed

    This prevents an overdue work from being misleadingly displayed
    as having "0 days remaining."

    ### Decision-Support Purpose

    The module helps authorities identify works that may require
    attention **before a delay becomes more significant**.

    The forecast is an explainable early-warning indicator based on
    available project timeline and status data. It does not establish
    fraud, misuse, non-compliance or future project failure.
            """
        )


    # ============================================================
    # SAFE NOTE
    # ============================================================

    st.caption(
        "Early-warning indicators support proactive monitoring "
        "and administrative review. They do not establish fraud, "
        "misuse or non-compliance."
    )

# ============================================================
# PAGE DISPATCH
# ============================================================

page = st.session_state.page

if page == "Dashboard":
    show_dashboard()
elif page == "Work Search":
    show_work_search()
elif page == "Delayed Projects":
    feature_1()
elif page == "Financial Anomalies":
    feature_2()
elif page == "Cost Deviation":
    feature_3()
elif page == "Similar Works":
    feature_4()
elif page == "Payment & Vendor":
    feature_5()
elif page == "Compliance":
    feature_6()
elif page == "AI Risk Assessment":
    feature_7()
elif page == "Trend Analysis":
    feature_8()
elif page == "Early Warning":
    feature_9()
else:
    show_dashboard()
