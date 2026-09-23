import sys
import os
import html
import io
import json

import streamlit as st  # <-- يجب استيراد streamlit هنا أولاً قبل أي استخدام لـ st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import tools
import agent
import ml_anomaly

st.set_page_config(page_title="FleetOps AI | XCMG Innovation Track", page_icon="🚧", layout="wide")

# ---------------------------------------------------------------------------
# Global CSS — industrial / engineering look
# ---------------------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Barlow+Condensed:wght@600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, sans-serif;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

.xcmg-banner {
    background: linear-gradient(90deg, #1D2126 0%, #2B3038 100%);
    border-bottom: 4px solid #C8102E;
    padding: 18px 28px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}
.xcmg-banner .brand-left { display: flex; align-items: center; gap: 14px; }
.xcmg-mark {
    width: 44px; height: 44px; border-radius: 6px;
    background: #C8102E;
    display: flex; align-items: center; justify-content: center;
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700; color: white; font-size: 22px;
    flex-shrink: 0;
}
.xcmg-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700; font-size: 26px; color: white; letter-spacing: 0.5px; line-height: 1.1;
}
.xcmg-subtitle { color: #B8BFC9; font-size: 12.5px; margin-top: 2px; }
.xcmg-pill {
    background: rgba(200,16,46,0.18); border: 1px solid #C8102E;
    color: #FF8C9A; padding: 6px 14px; border-radius: 20px;
    font-size: 11.5px; font-weight: 600; white-space: nowrap;
}

/* KPI cards */
.kpi-card {
    background: #FFFFFF;
    border-radius: 8px;
    padding: 16px 18px;
    border-left: 4px solid #C8102E;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    height: 100%;
}
.kpi-label {
    font-size: 12px;
    color: #5A6472;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}
.kpi-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: #1D2126 !important;
    margin-top: 2px;
}

.section-header {
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 20px;
    color: #1D2126 !important;
    border-left: 5px solid #C8102E;
    padding-left: 10px;
    margin: 6px 0 10px 0;
}

.stTabs [data-baseweb="tab-list"] { gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background: #F3F4F6; border-radius: 6px 6px 0 0; padding: 8px 18px; font-weight: 600; color: #5A6472;
}
.stTabs [aria-selected="true"] { background: #FFFFFF; color: #C8102E !important; border-bottom: 3px solid #C8102E; }

.stButton > button, .stDownloadButton > button {
    background: #1D2126; color: white; border: none; border-radius: 6px; font-weight: 600;
}
.stButton > button:hover, .stDownloadButton > button:hover { background: #C8102E; }

.agent-card {
    background: #FFFFFF;
    border: 1px solid #E3E6EA;
    border-left: 4px solid #C8102E;
    border-radius: 8px;
    padding: 14px 15px;
    min-height: 150px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    margin-bottom: 8px;
}
.agent-card-title { font-size: 14px; font-weight: 800; color: #1D2126 !important; margin-bottom: 5px; }
.agent-card-badge {
    display: inline-block; padding: 3px 8px; border-radius: 12px;
    background: #FCE8EC; color: #8C0B20; font-size: 10.5px; font-weight: 700; margin-bottom: 7px;
}
.agent-card-metric { font-family: 'Barlow Condensed', sans-serif; font-size: 25px; font-weight: 700; color: #1D2126 !important; margin: 2px 0 7px 0; }
.agent-card-body { font-size: 12.5px; color: #5A6472 !important; line-height: 1.45; }
.agent-card-action { margin-top: 8px; font-size: 12px; color: #1D2126 !important; font-weight: 600; }

@media (prefers-color-scheme: dark) {
    .kpi-card, .agent-card {
        background: #2B3038 !important;
        border-color: #3A414B !important;
    }
    .kpi-label, .agent-card-body { color: #B8BFC9 !important; }
    .kpi-value, .agent-card-title, .agent-card-metric, .agent-card-action { color: #F3F4F6 !important; }
    .section-header, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #F3F4F6 !important;
    }
}

.xcmg-footer {
    margin-top: 30px; padding: 14px 20px; background: #1D2126; border-radius: 6px;
    color: #9AA3AF; font-size: 11.5px; text-align: center; border-top: 3px solid #C8102E;
}
</style>
""", unsafe_allow_html=True)
