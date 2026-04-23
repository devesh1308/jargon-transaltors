# frontend/app.py
# Lexify — Turnitin-style UI (Pure White Background, No Tailwind)

import streamlit as st
import requests
import html
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
import time
import base64
import os
# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Lexify AI",
    page_icon="lexify.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# GLOBAL CSS
# ============================================
st.markdown("""
<style>

/* =========================================
   1. BACKGROUND & APP STRUCTURE
   ========================================= */
/* Set a subtle light gray background for the app body to create depth */
html, body, .stApp, [data-testid="stAppViewContainer"], section[data-testid="stMain"] {
    background: #F1F5F9 !important;
    background-image: none !important;
}

[data-testid="stHeader"], .stAppDeployButton, #MainMenu, footer {
    display: none !important;
    visibility: hidden !important;
}

/* ---- Streamlit Overrides ---- */
#MainMenu, footer { visibility: hidden; }
.block-container { padding-top: 50px !important; max-width: 100% !important; background: transparent !important; }
section[data-testid="stMain"] > div { padding: 0 !important; background: transparent !important; }

/* ---- Make sure top padding exists for the hero ---- */
.hero-section {
    text-align:center;
    padding-bottom: 20px;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    margin-top: 40px;
}

/* =========================================
   TURNITIN-STYLE CARD ELEVATION & SHADOWS
   ========================================= */
   
/* 1. File Uploader Card */
div[data-testid="stFileUploader"] {
    background: #FAFAFA !important;
    border-radius: 16px !important;
    padding: 24px !important;
    border: 1px solid #E5E7EB !important;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03) !important;
    margin-top: 10px !important;
    margin-bottom: 24px !important;
    transition: all 0.3s ease;
}
div[data-testid="stFileUploader"]:hover {
    border-color: #00A19B !important;
    background: #F0FDFB !important;
}
div[data-testid="stFileUploader"] section {
    border: 2px dashed #00A19B !important;
    border-radius: 8px !important;
    background: transparent !important;
    padding: 32px !important;
}

/* 2. Feature Cards & How it Works */
.features-row { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; max-width: 600px; margin: 32px auto 0 auto;align-items:stretch; }
.feature-card {
    background: white; border-radius: 12px; padding: 24px 16px; text-align: center;
    flex: 1; min-width: 150px; max-width: 170px;
    border: 1px solid #E5E7EB;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05), 0 8px 24px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease !important;
    cursor: default;
}
.feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1) !important;
    border-color: #00A19B !important;
}
}
.feature-icon { font-size: 28px; margin-bottom: 12px; }
.feature-title { font-size: 14px; font-weight: 700; color: #1F2937; margin-bottom: 6px; }
.feature-desc { font-size: 12px; color: #6b7280; line-height: 1.5; }

.how-it-works {
    background: white; border-radius: 12px; padding: 32px;
    width: 100%; max-width: 540px;
    border: 1px solid #D1D5DB;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    margin-top: 24px;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    margin:30px auto;
    transition:all 0.3s ease;
}
.how-it-works:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.06), 0 16px 36px rgba(0,0,0,0.1);
}
.how-title { font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #00A19B; margin-bottom: 24px; text-align: center; }
.step-row { display: flex; align-items: flex-start; gap: 16px; margin-bottom: 20px; }
.step-num { width: 32px; height: 32px; border-radius: 8px; background: #F3F4F6; color: #00A19B; font-size: 14px; font-weight: 800; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.step-title { font-size: 14px; font-weight: 700; color: #1F2937; margin-bottom: 4px; }
.step-desc { font-size: 13px; color: #6b7280; }

/* 3. Navbar */
.cg-navbar {
    background: white;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 32px; height: 70px; border-bottom: 1px solid #E5E7EB;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 12px rgba(0,0,0,0.04);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
.cg-logo { font-size: 20px; font-weight: 800; color: #1F2937; display: flex; align-items: center; gap: 12px; }
.cg-logo-box { width: 32px; height: 32px; background: linear-gradient(135deg, #00A19B, #008D88); border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; color: white; }
.cg-filename { font-size: 13px; color: #6b7280; margin-left: 4px; font-weight: 500; }
.cg-score-badge { display:flex; align-items:center; gap:12px; background:white; border-radius:12px; padding:8px 20px 8px 8px; border:1px solid #D1D5DB; box-shadow: 0 2px 4px rgba(0,0,0,0.04); }
.cg-score-circle { width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 14px; font-weight: 800; color: white; }
.cg-score-lbl { font-size: 10px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px; }
.cg-score-lvl { font-size: 13px; font-weight: 700; color: #1F2937; }

/* 4. Tabbar */
.cg-tabbar { background: white; display:flex; align-items:center; padding:12px 32px; gap:12px; border-bottom:1px solid #D1D5DB; box-shadow: 0 2px 4px rgba(0,0,0,0.02);margin-bottom:30px; }
.cg-tab { padding: 8px 18px; font-size: 13px; font-weight: 600; color: #6b7280; border-radius: 8px; cursor: pointer; transition: all 0.2s; }
.cg-tab.active { background: rgba(0, 161, 155, 0.1); color:#00A19B; }
.cg-tab-count { display: inline-block; background: #EF4444; color: white; font-size: 11px; font-weight: 700; border-radius: 10px; padding: 2px 8px; margin-left: 6px; }
.cg-tab-count.am { background: #F59E0B; }
.cg-tab-count.gr { background: #00A19B; }

/* 5. Document Pane */

.cg-paper {
    background: white;
    max-width: 100% !important;
    margin: 0 auto;
    min-height: 100%; /* Force the white paper to always touch the bottom */
    padding: 40px 60px;
    border-radius: 8px;
    border: 1px solid #D1D5DB;
    box-shadow: 0 2px 4px rgba(0,0,0,0.04), 0 16px 32px rgba(0,0,0,0.08);
    font-family: Georgia, 'Times New Roman', serif;
    font-size: 15px;
    line-height: 1.9;
    color: #374151;
}
.cg-clause-row { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 16px; }
.cg-flag { min-width: 24px; width: 24px; height: 24px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 800; color: white; margin-top: 4px; flex-shrink: 0; cursor: pointer; }
.cg-spacer { min-width: 24px; width: 24px; }
.cg-clause { flex: 1; padding: 8px 14px; border-radius: 6px; border-left: 3px solid transparent; cursor: pointer; transition: all 0.2s; }
.cg-clause.pred { background: #FEF2F2; border-left-color: #EF4444; }
.cg-clause.caut { background: #FFFBEB; border-left-color: #F59E0B; }
.cg-clause.safe { border-left-color: #00A19B; }
.cg-clause.lit { box-shadow: 0 0 0 2px #00A19B !important; background: rgba(0, 161, 155, 0.08) !important; border-left-color: #00A19B !important; }

/* 6. Insights pane & Individual Cards (The Turnitin Sidebar look) */
/* 6. Insights pane & Individual Cards (The Turnitin Sidebar look) */
.cg-doc-bg {
    padding: 0px 20px 10px 0px !important;
    height: calc(100vh - 160px); /* Lock height to the screen size */
    overflow-y: auto; /* Create an independent scrollbar */
    overflow-x: hidden;
}

.cg-insights-pane {
    background: #F9FAFB;
    border-left: 2px solid #D1D5DB;
    border-bottom: 1px solid #D1D5DB; /* Add a bottom border to close the pane nicely */
    display: flex;
    flex-direction: column;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    box-shadow: -4px 0 15px rgba(0,0,0,0.03);
    margin-left: 0;
    padding-left: 0;
    padding-bottom: 16px; /* Add a little padding at the bottom */
}

/* Remove Streamlit's default column gap */
[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
}

/* Remove padding between columns */
[data-testid="column"] {
    padding-left: 0 !important;
    padding-right: 0 !important;
}
.cg-ip-header { padding: 20px; border-bottom: 1px solid #D1D5DB; background: white; }
.cg-ip-label { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: #6b7280; margin-bottom: 12px; }
.cg-stats-row { display: flex; border-bottom: 1px solid #D1D5DB; background: white; }
.cg-stat { flex: 1; padding: 16px 8px; text-align: center; border-right: 1px solid #D1D5DB; }
.cg-stat:last-child { border-right: none; }
.cg-stat-n { font-size: 24px; font-weight: 800; line-height: 1; }
.cg-stat-l { font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; color: #6b7280; margin-top: 6px; font-weight: 700; }

.cg-cards-list { padding: 16px;
    max-height: calc(100vh - 460px); /* Leave exact space for Risk Score & Buttons */
    overflow-y: auto; }
.cg-card {
    background: white;
    border-radius: 8px;
    padding: 16px; margin-bottom: 14px; cursor: pointer;
    border: 1px solid #D1D5DB;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
.cg-card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.06), 0 8px 20px rgba(0,0,0,0.1);
    transform: translateX(-3px) translateY(-1px);
}
.cg-card.pred { border-left: 4px solid #EF4444; }
.cg-card.caut { border-left: 4px solid #F59E0B; }
.cg-card.safe { border-left: 4px solid #00A19B; }
.cg-card.lit { box-shadow: 0 0 0 2px #00A19B !important; background: rgba(0, 161, 155, 0.02) !important; border-left-color: #00A19B !important; }
.cg-card-badge { display: flex; align-items: center; gap: 8px; margin-bottom: 10px; }
.cg-card-num { width: 22px; height: 22px; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 800; color: white; flex-shrink: 0; }
.cg-card-risk { font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px; }
.cg-card-excerpt { font-size: 13px; color: #374151; line-height: 1.5; margin-bottom: 10px; font-style: italic; }
.cg-card-why { font-size: 13px; color: #1F2937; line-height: 1.6; border-top: 1px solid #E5E7EB; padding-top: 10px; font-weight: 500; }

/* ---- Buttons & Inputs ---- */
.stButton > button {
    border-radius: 8px !important; font-weight: 700 !important; font-size: 15px !important; background: #00A19B !important; color: white !important;
    border: none !important; padding: 0.75rem 1.5rem !important; box-shadow: 0 4px 6px rgba(0,161,155,.2) !important;
}
.stDownloadButton > button { border-radius: 8px !important; font-weight: 600 !important; font-size: 14px !important; }
.stRadio > div { flex-direction: row !important; gap: 12px !important; flex-wrap: wrap !important; }
.stRadio label {
    background: white !important; padding: 6px 16px !important; border-radius: 8px !important;
    border: 1px solid #D1D5DB !important; cursor: pointer !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
}
.stRadio label p { color: #1F2937 !important; font-size: 13px !important; font-weight: 600 !important; margin: 0 !important; }
.stAlert { border-radius: 8px !important; font-size: 14px !important; background: white !important; border: 1px solid #D1D5DB !important; box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important; }
/* ============================================
   BALANCED GAP REMOVAL (No Overlap)
   ============================================ */
   
/* Remove gap between columns but keep them separated */
[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
}

/* Remove extra padding from columns */
[data-testid="column"] {
    padding-left: 0 !important;
    padding-right: 0 !important;
}

/* Left column - allow it to breathe */
[data-testid="stHorizontalBlock"] > div:first-child {
    padding-right: 0 !important;
    overflow-x: hidden !important;
}

/* Right column - give it proper padding */
[data-testid="stHorizontalBlock"] > div:last-child {
    padding-left: 0 !important;
}

/* Document background - balanced padding */
.cg-doc-bg {
    padding: 0px 20px 40px 40px !important;
}

/* Paper - keep it contained */
.cg-paper {
    max-width: 100% !important;
    margin-right: 0 !important;
    word-wrap: break-word !important;
}

/* Insights panel - proper spacing */
.cg-insights-pane {
    margin-left: 0 !important;
    padding-left: 16px !important;
    padding-right: 16px !important;
}

/* Cards - prevent overflow */
.cg-card {
    word-wrap: break-word !important;
    overflow-wrap: break-word !important;
}

.cg-card-excerpt {
    word-break: break-word !important;
}
/* ============================================
   SKELETON LOADER ANIMATION
   ============================================ */
   
.skeleton-container {
    padding: 40px;
    max-width: 1200px;
    margin: 0 auto;
}

.skeleton-pulse {
    animation: pulse 1.5s ease-in-out infinite;
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    border-radius: 8px;
}

@keyframes pulse {
    0% { opacity: 0.6; }
    50% { opacity: 1; }
    100% { opacity: 0.6; }
}

.scanning-header {
    text-align: center;
    margin-bottom: 40px;
}

.scanning-title {
    font-size: 28px;
    font-weight: 700;
    color: #1F2937;
    margin-bottom: 8px;
}

.scanning-subtitle {
    font-size: 16px;
    color: #6B7280;
}

.progress-steps {
    max-width: 500px;
    margin: 40px auto;
    background: white;
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border: 1px solid #E5E7EB;
}

.step-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px;
    border-radius: 12px;
    transition: all 0.3s;
}

.step-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
}

.step-content {
    flex: 1;
}

.step-title {
    font-size: 15px;
    font-weight: 600;
    color: #1F2937;
    margin-bottom: 4px;
}

.step-status {
    font-size: 13px;
    color: #6B7280;
}

.step-completed .step-icon {
    background: #10B981;
    color: white;
}

.step-active .step-icon {
    background: #00A19B;
    color: white;
    animation: pulse 1.5s infinite;
}

.step-pending .step-icon {
    background: #F3F4F6;
    color: #9CA3AF;
}

.skeleton-document {
    background: white;
    border-radius: 16px;
    padding: 40px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border: 1px solid #E5E7EB;
}

.skeleton-line {
    height: 16px;
    margin-bottom: 16px;
    border-radius: 8px;
    background: #F3F4F6;
}

.skeleton-line-short {
    width: 60%;
}

.skeleton-line-medium {
    width: 80%;
}

.skeleton-line-long {
    width: 100%;
}

.scanning-footer {
    text-align: center;
    margin-top: 40px;
    color: #9CA3AF;
    font-size: 14px;
}
/* ============================================
   UPLOAD TABS (PDF / Paste Text)
   ============================================ */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #F3F4F6;
    padding: 6px;
    border-radius: 12px;
    display: flex;
    justify-content: center;
    border: 1px solid #E5E7EB;
}
.stTabs [data-baseweb="tab"] {
    height: 40px;
    background-color: transparent;
    border-radius: 8px;
    color: #6B7280;
    font-weight: 600;
    padding: 0 24px;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background-color: white !important;
    color: #00A19B !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.stTabs [data-baseweb="tab-highlight"] {
    display: none; /* Hides the native red underline */
}
/* =========================================
   CUSTOM ELEGANT SCROLLBARS
   ========================================= */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: #CBD5E1;
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: #94A3B8;
}
/* =========================================
   CUSTOM MODERN TABS
   ========================================= */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background-color: #F3F4F6;
    padding: 6px;
    border-radius: 12px;
    display: flex;
    justify-content: center;
    border: 1px solid #E5E7EB;
}
.stTabs [data-baseweb="tab"] {
    height: 40px;
    background-color: transparent;
    border-radius: 8px;
    color: #6B7280;
    font-weight: 600;
    padding: 0 24px;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background-color: white !important;
    color: #00A19B !important;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.stTabs [data-baseweb="tab-highlight"] {
    display: none; /* Hides the native red underline */
}
/* =========================================
   MOBILE RESPONSIVENESS (Breakpoints)
   ========================================= */
@media screen and (max-width: 768px) {
    /* 1. Release the fixed heights so the page scrolls naturally on mobile */
    .cg-doc-bg, .cg-cards-list {
        height: auto !important;
        max-height: none !important;
        overflow-y: visible !important;
        padding-bottom: 20px !important;
    }

    /* 2. Shrink the giant desktop paddings */
    .cg-paper {
        padding: 20px 15px !important;
        font-size: 14px !important;
    }

    /* 3. Stack the Navbar nicely */
    .cg-navbar {
        flex-direction: column !important;
        height: auto !important;
        padding: 16px !important;
        gap: 12px !important;
        text-align: center;
    }
   
    /* 4. Let the Tabbar wrap if it gets too tight */
    .cg-tabbar {
        padding: 12px 16px !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 8px !important;
    }

    /* 5. Shrink the Hero text slightly */
    h1 {
        font-size: 32px !important;
    }
   
    /* 6. Ensure the Upload Box fits on screen */
    div[data-testid="stFileUploader"] {
        padding: 16px !important;
    }
    div[data-testid="stFileUploader"] section {
        padding: 20px 10px !important;
    }
}
</style>
""", unsafe_allow_html=True)

# Shared JS for cross-pane sync (injected once)
SYNC_JS = """
<script>
if (!window._cgSyncDefined) {
    window._cgSyncDefined = true;
    window.cgSync = function(idx) {
        document.querySelectorAll('.cg-clause.lit, .cg-card.lit').forEach(function(el){ el.classList.remove('lit'); });
        var cl = document.getElementById('cl-' + idx);
        if (cl) { cl.classList.add('lit'); cl.scrollIntoView({behavior:'smooth', block:'center'}); }
        var cd = document.getElementById('cd-' + idx);
        if (cd) { cd.classList.add('lit'); cd.scrollIntoView({behavior:'smooth', block:'nearest'}); }
    };
}
</script>
"""

# ============================================
# HELPERS
# ============================================
def check_backend():
    try:
        r = requests.get("http://127.0.0.1:8000/health", timeout=2)
        return r.status_code == 200
    except:
        return False

def calc_stats(clauses):
    p  = sum(1 for c in clauses if c.get('risk') == 'Predatory')
    ca = sum(1 for c in clauses if c.get('risk') == 'Caution')
    s  = sum(1 for c in clauses if c.get('risk') == 'Safe')
    return {"score": min(100, p*15 + ca*5), "predatory": p, "caution": ca, "safe": s}

def score_meta(score):
    if score >= 70: return "#e63e3e", "High Risk"
    if score >= 30: return "#d97706", "Medium Risk"
    return "#059669", "Low Risk"

def risk_css(risk):
    return {"Predatory": "pred", "Caution": "caut"}.get(risk, "safe")

def risk_color(risk):
    return {"Predatory": "#e63e3e", "Caution": "#d97706"}.get(risk, "#059669")


from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
import io
import base64

def generate_pdf_report(fname, stats, risk_lbl, clauses):
    """Generate a professional PDF report"""
   
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
   
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1F2937'),
        spaceAfter=30,
        alignment=1  # Center
    )
    story.append(Paragraph("Lexify AI Risk Analysis Report", title_style))
   
    # File info
    file_style = ParagraphStyle(
        'FileInfo',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#6B7280'),
        spaceAfter=20,
        alignment=1
    )
    story.append(Paragraph(f"File: {fname}", file_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", file_style))
   
    # Risk Score Section
    score_color = colors.HexColor('#EF4444') if stats['score'] >= 70 else colors.HexColor('#F59E0B') if stats['score'] >= 30 else colors.HexColor('#10B981')
   
    # Score table
    score_data = [
        ['Risk Score', f"{stats['score']}%"],
        ['Risk Level', risk_lbl],
        ['Predatory Clauses', str(stats['predatory'])],
        ['Caution Clauses', str(stats['caution'])],
        ['Safe Clauses', str(stats['safe'])]
    ]
   
    score_table = Table(score_data, colWidths=[2*inch, 2*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F3F4F6')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1F2937')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
        ('TEXTCOLOR', (1, 1), (1, 1), score_color),
    ]))
   
    story.append(score_table)
    story.append(Spacer(1, 0.3*inch))
   
    # Flagged Clauses Section
    story.append(Paragraph("Flagged Clauses", styles['Heading2']))
    story.append(Spacer(1, 0.2*inch))
   
    fn = 0
    for clause in clauses:
        risk = clause.get('risk', 'Safe')
        if risk in ('Predatory', 'Caution'):
            fn += 1
           
            # Clause header
            risk_color = colors.HexColor('#EF4444') if risk == 'Predatory' else colors.HexColor('#F59E0B')
            clause_header = Paragraph(f"<b>{fn}. [{risk.upper()}]</b>", styles['Heading3'])
            story.append(clause_header)
           
            # Clause text
            clause_text = Paragraph(
                f"<i>{clause.get('original_text', '')}</i>",
                styles['Normal']
            )
            story.append(clause_text)
           
            # Translation
            translation = Paragraph(
                f"<font color='#6B7280'>💡 {clause.get('translation', '')}</font>",
                styles['Normal']
            )
            story.append(translation)
           
            story.append(Spacer(1, 0.2*inch))
   
    # Footer
    story.append(Spacer(1, 0.5*inch))
    footer = Paragraph(
        "<font color='#9CA3AF' size=8>Lexify AI • Generated offline • 100% private analysis</font>",
        styles['Normal']
    )
    story.append(footer)
   
    # Build PDF
    doc.build(story)
    buffer.seek(0)
   
    return buffer

def show_scanning_animation():
    import time
    import streamlit as st

@st.dialog("🔍 Analyzing Contract", width="large")
def analyze_document_modal(input_data, filename, is_text=False):
    import time
   
    # --- 1. THE UI ANIMATION ---
    steps = [
        ("📄", "Reading contract", "Extracting text and clauses", 20),
        ("🔍", "Scanning risks", "Finding hidden fees and unfair terms", 45),
        ("⚖️", "Legal analysis", "Checking tenant protections", 72),
        ("📊", "Generating report", "Preparing your dashboard", 100),
    ]

    tips = [
        "Late fees above reasonable limits can be risky.",
        "Undefined deposit timelines often cause disputes.",
        "Entry without notice may reduce privacy protections.",
        "Unclear repair clauses can shift unfair costs."
    ]

    # Removed the extra st.markdown heading here, kept the caption!
    st.caption("AI is reviewing every clause in real time")

    progress = st.progress(0)
    percent = st.empty()
    status = st.empty()

    col1, col2 = st.columns([1, 2])
    metric_box = col1.empty()
    preview_box = col2.empty()
    tip_box = st.empty()

    current = 0
    for i, (icon, title, subtitle, target) in enumerate(steps):
        while current < target:
            current += 2
            progress.progress(current)
            percent.markdown(f"### {current}%")
            status.info(f"{icon} {title} — {subtitle}")
            metric_box.metric("Processing", f"{current}%")
           
            preview_box.markdown("""
            <div style="margin-bottom: 8px; font-weight: 600; color: #1F2937;">Live Preview</div>
            <div style="font-size: 13px; color: #6b7280; margin-bottom: 16px;">Generating flagged clauses...</div>
            
            <div style="display: flex; flex-direction: column; gap: 12px;">
                <div style="height: 12px; width: 100%; background-color: #E5E7EB; border-radius: 6px;"></div>
                <div style="height: 12px; width: 80%; background-color: #E5E7EB; border-radius: 6px;"></div>
                <div style="height: 12px; width: 95%; background-color: #E5E7EB; border-radius: 6px;"></div>
                <div style="height: 12px; width: 60%; background-color: #E5E7EB; border-radius: 6px;"></div>
            </div>
            """, unsafe_allow_html=True)
            tip_box.caption(f"💡 {tips[i]}")
            time.sleep(0.04)
        time.sleep(0.35)
       
    status.success("✅ Analysis Complete! Fetching results...")

    # --- 2. THE API CALL ---
    try:
        if is_text:
            # If it's raw text, send it as JSON to a text-specific endpoint
            resp = requests.post(
                "http://127.0.0.1:8000/predict-text",
                json={"text": input_data},
                timeout=60
            )
        else:
            # If it's a file, send it as multipart form data
            resp = requests.post(
                "http://127.0.0.1:8000/predict",
                files={"file": (filename, input_data, "application/pdf")}, # <-- This was the culprit!
                timeout=60
            )

        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success" and "clauses" in data:
                st.session_state.results = data["clauses"]
                st.session_state.filename = filename
                st.rerun() # Closes the modal and loads the results page
            else:
                st.error("Invalid backend response.")
        else:
            st.error(f"Backend error: {resp.status_code}-{resp.text}")
    except Exception as e:
        st.error(f"Connection error: {e}")

def get_base64_image(image_path):
    """Converts a local image into a base64 string for HTML embedding."""
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return "" # Return empty if file isn't found
    # ============================================
# UPLOAD / LANDING PAGE
# ============================================
def show_upload(backend_ok):
   
    # 1. Hero Section
    # Get the logo!
    logo_b64 = get_base64_image("lexify.png")
   
    # If the logo is found, use it.
    if logo_b64:
        # NOTE: Added transform: translateX(12px) to visually balance the asymmetric shield!
        logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="display: block; margin: 0 auto 2px auto; width: 130px; height: 130px; object-fit: contain; filter: drop-shadow(0 8px 16px rgba(0,0,0,0.08)); transform: translateX(-15px);">'
    else:
        logo_html = '<div style="width:72px;height:72px;background:linear-gradient(135deg,#00A19B,#008D88); border-radius:20px;display:inline-flex;align-items:center;justify-content:center; font-size:36px;margin-bottom:16px;box-shadow:0 12px 32px rgba(0,161,155,0.3); color:white;">🔒</div>'

    # 1. Hero Section
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; width: 100%; margin-top: 2rem; margin-bottom: 2rem;">
        {logo_html}
        <h1 style="font-size:42px; font-weight:900; color:#1F2937; letter-spacing:-1.5px; margin: 0 auto 8px auto; line-height:1; text-align: center; width: 100%;">Lexify AI</h1>
        <p style="font-size:16px; color:#6b7280; max-width:400px; margin:0 auto; line-height:1.5; text-align: center;">
            Understand your rental agreement before you sign. <br/><b>100% private, offline analysis.</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 2. Upload Section
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        if not backend_ok:
            st.warning("⚠️ Backend offline. Run: `uvicorn backend.main:app --reload`")

        st.markdown("""
        <div style="text-align: center; font-size: 16px; font-weight: 700; color: #1F2937; font-family: sans-serif;">
            📄 Upload or Copy your rental agreement.
        </div>
        """, unsafe_allow_html=True)

        # Tab switcher for PDF Upload or Paste Text
        tab1, tab2 = st.tabs([" Upload PDF", " Paste Text"])
       
        analyze_data = None
        analyze_name = None
        is_text_mode = False
       
        with tab1:
            uploaded = st.file_uploader(
                "Drop PDF", type="pdf",
                label_visibility="collapsed",
                key="pdf_uploader"
            )
            # If a PDF is uploaded, prep it (unless text overwrites it below)
            if uploaded:
                analyze_data = uploaded.getvalue()
                analyze_name = uploaded.name
                is_text_mode = False
       
        with tab2:
            pasted_text = st.text_area(
                "Paste your rental agreement text",
                placeholder="Paste the full text here... (Click outside the box after pasting!)",
                height=250,
                key="pasted_text"
            )
           
            # If there is text, it OVERRIDES the PDF tab completely
            if pasted_text and len(pasted_text.strip()) > 0:
                st.success(" Text registered! Ready to analyze.")
                analyze_data = pasted_text
                analyze_name = "pasted_text"
                is_text_mode = True
       
        # Analyze button rendering
        if analyze_data is not None:
            bc = st.columns([1, 2, 1])
            with bc[1]:
                if st.button(" Analyze Contract", type="primary", use_container_width=True):
                    if not backend_ok:
                        st.error("Backend is offline. Please start the server first.")
                    else:
                        # Send it to the modal!
                        analyze_document_modal(analyze_data, analyze_name, is_text=is_text_mode)

        else:
            st.markdown("""
            <div style="text-align:center;color:#9ca3af;font-size:12px;padding:8px 0;">
                Upload a PDF or paste text to get started
            </div>""", unsafe_allow_html=True)

        # 3. Feature cards
        st.markdown("""
        <div class="features-row">
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <div class="feature-title">100% Private</div>
                <div class="feature-desc">Your document never leaves your device.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Risk Detection</div>
                <div class="feature-desc">Color-coded highlights for every risky clause.</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <div class="feature-title">Plain English</div>
                <div class="feature-desc">Every flag explained in simple language.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4. How it works
        st.markdown("""
        <div class="how-it-works">
            <div class="how-title">How it works</div>
            <div class="step-row">
                <div class="step-num">1</div>
                <div>
                    <div class="step-title">Upload your agreement</div>
                    <div class="step-desc">Select any rental or lease PDF from your device.</div>
                </div>
            </div>
            <div class="step-row">
                <div class="step-num">2</div>
                <div>
                    <div class="step-title">AI scans every clause</div>
                    <div class="step-desc">Our model classifies each clause: Predatory, Caution, or Safe.</div>
                </div>
            </div>
            <div class="step-row">
                <div class="step-num">3</div>
                <div>
                    <div class="step-title">Review the report</div>
                    <div class="step-desc">Highlighted clauses with plain-English explanations, side by side.</div>
                </div>
            </div>
            <div class="step-row">
                <div class="step-num">4</div>
                <div>
                    <div class="step-title">Download & negotiate</div>
                    <div class="step-desc">Export your report and know exactly what to push back on.</div>
                </div>
            </div>
        </div>
        <div style="text-align:center;font-size:11px;color:#d1d5db;padding:20px 0 40px 0;">
            Lexify AI &nbsp;&middot;&nbsp; All analysis runs locally on your machine
        </div>
        """, unsafe_allow_html=True)

# ============================================
# RESULTS PAGE
# ============================================
def show_results(clauses):
    stats = calc_stats(clauses)
    sc_col, risk_lbl = score_meta(stats['score'])
    fname = st.session_state.get('filename', 'Agreement.pdf')

    # Build flag index
    flag_idx = {}
    n = 0
    for i, c in enumerate(clauses):
        if c.get('risk') in ('Predatory', 'Caution'):
            n += 1
            flag_idx[i] = n

    pc = stats['predatory']
    cc = stats['caution']
    sc = stats['safe']

    # ---- NAVBAR ----
    # Fetch the custom logo for the navbar
    logo_b64 = get_base64_image("lexify.png")
    if logo_b64:
        nav_logo_html = f'<img src="data:image/png;base64,{logo_b64}" style="width: 36px; height: 36px; object-fit: contain;">'
    else:
        nav_logo_html = '<div class="cg-logo-box">🔒</div>'

    st.markdown(SYNC_JS,unsafe_allow_html=True)
    st.markdown(f"""
   
    <div class="cg-navbar" style="margin-top: -40px; margin-bottom: 20px; width: 100%; border-radius: 8px;">
        <div style="display:flex;align-items:center;gap:14px;">
            <div class="cg-logo" style="display: flex; align-items: center; gap: 10px;">
                {nav_logo_html}
                Lexify AI
            </div>
            <div class="cg-filename" style="color:#9CA3AF; font-size:15px;">/ &nbsp;{html.escape(fname)}</div>
        </div>
        <div style="display:flex;align-items:center;gap:16px;">
            <div style="font-size:13px; font-weight:600; color:#4B5563; cursor:pointer;">Settings</div>
            <div style="background:#00A19B; color:white; padding:8px 16px; border-radius:6px; font-size:13px; font-weight:700; cursor:pointer; box-shadow:0 2px 4px rgba(0,0,0,0.1);">Deploy</div>
        </div>
    </div>
   
    <div class="cg-tabbar">
        <div class="cg-tab active">Risk Analysis <span class="cg-tab-count">{pc+cc}</span></div>
        <div class="cg-tab">Predatory <span class="cg-tab-count">{pc}</span></div>
        <div class="cg-tab">Caution <span class="cg-tab-count am">{cc}</span></div>
        <div class="cg-tab">Safe <span class="cg-tab-count gr">{sc}</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ---- TWO COLUMNS ----
    col_left, col_right = st.columns([6, 3.5])

    # ---- LEFT: Document ----
    with col_left:
        rows_html = ""
        for i, clause in enumerate(clauses):
            risk = clause.get('risk', 'Safe')
            css  = risk_css(risk)
            clr  = risk_color(risk)
            txt  = html.escape(clause.get('original_text', ''))

            if i in flag_idx:
                flag = f'<div class="cg-flag" style="background:{clr};" onclick="cgSync({i})">{flag_idx[i]}</div>'
            else:
                flag = '<div class="cg-spacer"></div>'

            rows_html += f"""
            <div class="cg-clause-row">
                {flag}
                <div class="cg-clause {css}" id="cl-{i}" onclick="cgSync({i})">{txt}</div>
            </div>"""

        st.markdown(f"""
        <div class="cg-doc-bg">
            <div class="cg-paper">{rows_html}</div>
        </div>
        """, unsafe_allow_html=True)

    # ---- RIGHT: Insights ----
    with col_right:
        # ============================================
        # PROMINENT RISK SCORE CARD (At the Top!)
        # ============================================
        st.markdown(f"""
        <div style="background: white;
                    border: 1px solid #D1D5DB;
                    border-left: 6px solid {sc_col};
                    border-radius: 12px;
                    padding: 16px 20px;
                    margin-bottom: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <div>
                <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #64748b; margin-bottom: 4px;">
                    Overall Risk
                </div>
                <div style="display:flex; align-items:baseline; gap:8px;">
                    <div style="font-size: 36px; font-weight: 900; color: {sc_col}; line-height: 1;">
                        {stats['score']}%
                    </div>
                    <div style="font-size: 14px; font-weight: 700; color: #4B5563;">
                        ({risk_lbl})
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 16px; border-left: 1px solid #E5E7EB; padding-left: 16px;">
                <div style="text-align: center;">
                    <div style="font-size: 20px; font-weight: 800; color: #ef4444;">{pc}</div>
                    <div style="font-size: 10px; color: #64748b; text-transform:uppercase; font-weight:700;">Predatory</div>
                </div>
                <div style="text-align: center;">
                    <div style="font-size: 20px; font-weight: 800; color: #f59e0b;">{cc}</div>
                    <div style="font-size: 10px; color: #64748b; text-transform:uppercase; font-weight:700;">Caution</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)        
        # ============================================
        # FILTER RADIO BUTTONS
        # ============================================
        filt = st.radio(
            "Filter",
            ["All", "Predatory", "Caution", "Safe"],
            horizontal=True, key="filt",
            label_visibility="collapsed"
        )
       
        # ============================================
        # FLAGGED CLAUSES PANEL
        # ============================================
       # ============================================
        # FLAGGED CLAUSES PANEL
        # ============================================
       
        # 1. MAKE SURE THIS LINE IS HERE (This creates the variable)
        cards_html = ""
       
        # 2. THE LOOP
        for i, clause in enumerate(clauses):
            risk = clause.get('risk', 'Safe')
            if filt == "Predatory" and risk != "Predatory":
                continue
            if filt == "Caution" and risk != "Caution":
                continue
            if filt == "Safe" and risk != "Safe":
                continue

            css = risk_css(risk)
            clr = risk_color(risk)
            num = flag_idx.get(i, "✓")
            excerpt = clause.get('original_text', '')
            if len(excerpt) > 115:
                excerpt = excerpt[:115] + "…"
            why = clause.get('translation', 'No explanation available.')

            cards_html += f"""
            <div class="cg-card {css}" id="cd-{i}" onclick="cgSync({i})">
                <div class="cg-card-badge">
                    <div class="cg-card-num" style="background:{clr};">{num}</div>
                    <span class="cg-card-risk" style="color:{clr};">{html.escape(risk)}</span>
                </div>
                <div class="cg-card-excerpt">{html.escape(excerpt)}</div>
                <div class="cg-card-why">{html.escape(why)}</div>
            </div>"""

        # 3. EMPTY STATE CHECK (Now it knows cards_html exists!)
        if cards_html == "":
            cards_html = f"""
            <div style="text-align: center; padding: 60px 20px; background: white; border-radius: 8px; border: 1px dashed #D1D5DB; margin-top: 10px;">
                <div style="font-size: 32px; margin-bottom: 12px; opacity: 0.6;">🔍</div>
                <div style="font-size: 15px; font-weight: 700; color: #4B5563;">No {filt.lower()} clauses found</div>
                <div style="font-size: 13px; color: #9CA3AF; margin-top: 6px;">
                    There are no clauses matching this risk level in the current document.
                </div>
            </div>
            """

        # 4. RENDER TO STREAMLIT
        st.markdown(f"""
        <div class="cg-insights-pane">
            <div class="cg-ip-header">
                <div class="cg-ip-label">Flagged Clauses</div>
            </div>
            <div class="cg-cards-list">{cards_html}</div>
        </div>
        """, unsafe_allow_html=True)

       

        # ============================================
        # ACTION BUTTONS
        # ============================================
        st.markdown('<hr style="border:0; border-top:1px solid transparent; margin: 8px 0;">', unsafe_allow_html=True)
       
        pdf_buffer = generate_pdf_report(fname, stats, risk_lbl, clauses)
        pdf_data = pdf_buffer.getvalue()
       
        # Use a 3-column layout where the middle column acts as an invisible gap
        b1, spacer, b2 = st.columns([1, 0.05, 1])
       
        with b1:
            if st.button("⟵ New Analysis", key="reset", use_container_width=True):
                st.session_state.results = None
                st.session_state.filename = None
                st.rerun()
               
        with spacer:
            # Leave this completely empty to create the gap
            pass
           
        with b2:
            st.download_button(
                "⬇ Download Full PDF Report",
                data=pdf_data,
                file_name=f"Lexify_AI_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

       


# ============================================
# MAIN
# ============================================
def main():
    if 'results'  not in st.session_state: st.session_state.results  = None
    if 'filename' not in st.session_state: st.session_state.filename = None

    if st.session_state.results is None:
        show_upload(check_backend())
    else:
        show_results(st.session_state.results)

if __name__ == "__main__":
    main()