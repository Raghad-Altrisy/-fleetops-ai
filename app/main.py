# ---------------------------------------------------------------------------
# Global CSS — industrial / engineering look (Fixed Contrast & Dark Mode)
# ---------------------------------------------------------------------------
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Barlow+Condensed:wght@600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, sans-serif;
}}

/* Hide default Streamlit chrome for a cleaner branded look */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}

/* Top brand banner */
.xcmg-banner {{
    background: linear-gradient(90deg, {CHARCOAL} 0%, {CHARCOAL_2} 100%);
    border-bottom: 4px solid {RED};
    padding: 18px 28px;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}}
.xcmg-banner .brand-left {{ display: flex; align-items: center; gap: 14px; }}
.xcmg-mark {{
    width: 44px; height: 44px; border-radius: 6px;
    background: {RED};
    display: flex; align-items: center; justify-content: center;
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700; color: white; font-size: 22px;
    flex-shrink: 0;
}}
.xcmg-title {{
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700; font-size: 26px; color: white; letter-spacing: 0.5px; line-height: 1.1;
}}
.xcmg-subtitle {{ color: #B8BFC9; font-size: 12.5px; margin-top: 2px; }}
.xcmg-pill {{
    background: rgba(200,16,46,0.18); border: 1px solid {RED};
    color: #FF8C9A; padding: 6px 14px; border-radius: 20px;
    font-size: 11.5px; font-weight: 600; white-space: nowrap;
}}

/* KPI cards — Updated for light and dark modes */
.kpi-card {{
    background: {WHITE};
    border-radius: 8px;
    padding: 16px 18px;
    border-left: 4px solid {RED};
    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    height: 100%;
}}
.kpi-label {{
    font-size: 12px;
    color: {STEEL};
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.4px;
}}
.kpi-value {{
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 30px;
    font-weight: 700;
    color: {CHARCOAL} !important; /* لون داكن ثابت على الخلفية البيضاء */
    margin-top: 2px;
}}

/* Section headers */
.section-header {{
    font-family: 'Barlow Condensed', sans-serif;
    font-weight: 700;
    font-size: 20px;
    color: {CHARCOAL} !important;
    border-left: 5px solid {RED};
    padding-left: 10px;
    margin: 6px 0 10px 0;
}}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
.stTabs [data-baseweb="tab"] {{
    background: {CONCRETE}; border-radius: 6px 6px 0 0; padding: 8px 18px; font-weight: 600; color: {STEEL};
}}
.stTabs [aria-selected="true"] {{ background: {WHITE}; color: {RED} !important; border-bottom: 3px solid {RED}; }}

/* Buttons */
.stButton > button, .stDownloadButton > button {{
    background: {CHARCOAL}; color: white; border: none; border-radius: 6px; font-weight: 600;
}}
.stButton > button:hover, .stDownloadButton > button:hover {{ background: {RED}; }}

/* Agent response cards */
.agent-card {{
    background: #FFFFFF;
    border: 1px solid #E3E6EA;
    border-left: 4px solid {RED};
    border-radius: 8px;
    padding: 14px 15px;
    min-height: 150px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06);
    margin-bottom: 8px;
}}
.agent-card-title {{ font-size: 14px; font-weight: 800; color: {CHARCOAL} !important; margin-bottom: 5px; }}
.agent-card-badge {{
    display: inline-block; padding: 3px 8px; border-radius: 12px;
    background: #FCE8EC; color: {RED_DARK}; font-size: 10.5px; font-weight: 700; margin-bottom: 7px;
}}
.agent-card-metric {{ font-family: 'Barlow Condensed', sans-serif; font-size: 25px; font-weight: 700; color: {CHARCOAL} !important; margin: 2px 0 7px 0; }}
.agent-card-body {{ font-size: 12.5px; color: {STEEL} !important; line-height: 1.45; }}
.agent-card-action {{ margin-top: 8px; font-size: 12px; color: {CHARCOAL} !important; font-weight: 600; }}

/* Dark mode adjustments - making sure cards adapt properly */
@media (prefers-color-scheme: dark) {{
    .kpi-card, .agent-card {{
        background: {CHARCOAL_2} !important;
        border-color: #3A414B !important;
    }}
    .kpi-label, .agent-card-body {{ color: #B8BFC9 !important; }}
    .kpi-value, .agent-card-title, .agent-card-metric, .agent-card-action {{ color: #F3F4F6 !important; }}
    .section-header, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {{
        color: #F3F4F6 !important;
    }}
}}

/* Footer strip */
.xcmg-footer {{
    margin-top: 30px; padding: 14px 20px; background: {CHARCOAL}; border-radius: 6px;
    color: #9AA3AF; font-size: 11.5px; text-align: center; border-top: 3px solid {RED};
}}
</style>
""", unsafe_allow_html=True)
