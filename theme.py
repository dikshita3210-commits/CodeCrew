"""
theme.py — single source of truth for CodeCrew's visual design.

Every page calls inject_css() once, at the top, right after st.set_page_config().
Change a color/spacing value here and it updates everywhere — that's the whole point.
"""

import streamlit as st

# ---------------------------------------------------------------------
# DESIGN TOKENS (matches the design language brief: GitHub Enterprise /
# Linear / Vercel / Stripe Dashboard aesthetic — no glassmorphism, no
# neon, no oversized rounded cards)
# ---------------------------------------------------------------------
BG = "#FAFAFB"
CARD_BG = "#FFFFFF"
BORDER = "#E5E7EB"
BORDER_STRONG = "#D1D5DB"
TEXT_PRIMARY = "#111827"
TEXT_SECONDARY = "#6B7280"
TEXT_MUTED = "#9CA3AF"

ACCENT = "#4F46E5"
ACCENT_HOVER = "#4338CA"
ACCENT_SOFT = "#EEF2FF"

SIDEBAR_BG = "#111827"
SIDEBAR_TEXT = "#9CA3AF"
SIDEBAR_TEXT_ACTIVE = "#FFFFFF"
SIDEBAR_ACTIVE_BG = "#1F2937"

CRITICAL = "#DC2626"
CRITICAL_SOFT = "#FEF2F2"
CRITICAL_BORDER = "#FECACA"

WARNING = "#D97706"
WARNING_SOFT = "#FFFBEB"
WARNING_BORDER = "#FDE68A"

INFO = "#059669"
INFO_SOFT = "#ECFDF5"
INFO_BORDER = "#A7F3D0"

VIOLET = "#7C3AED"
VIOLET_SOFT = "#F5F3FF"
BLUE = "#2563EB"
BLUE_SOFT = "#EFF6FF"
TEAL = "#0D9488"
TEAL_SOFT = "#F0FDFA"

NEUTRAL_SOFT = "#F3F4F6"

FONT = "Inter"

RADIUS = "8px"
SHADOW = "0 1px 2px rgba(16, 24, 40, 0.05)"


def inject_css():
    st.markdown(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">

        <style>

        html, body, [class*="css"] {{
            font-family: '{FONT}', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        .stApp {{
            background-color: {BG};
        }}

        /* ---- kill default streamlit chrome we don't want ---- */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{
            background: transparent;
        }}
        [data-testid="stToolbar"] {{
            visibility: hidden;
        }}
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1240px;
        }}

        /* ---- sidebar collapse/expand arrow — make it clearly visible
             instead of blending into the light background ---- */
        [data-testid="stSidebarCollapsedControl"] button,
        [data-testid="collapsedControl"] button {{
            background: {CARD_BG} !important;
            border: 1px solid {BORDER_STRONG} !important;
            border-radius: 6px !important;
        }}
        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="collapsedControl"] svg {{
            color: {TEXT_PRIMARY} !important;
            fill: {TEXT_PRIMARY} !important;
        }}

        /* ---- sidebar ---- */
        section[data-testid="stSidebar"] {{
            background-color: {SIDEBAR_BG};
            border-right: 1px solid #1F2937;
        }}
        section[data-testid="stSidebar"] * {{
            color: {SIDEBAR_TEXT};
        }}
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3 {{
            color: {SIDEBAR_TEXT_ACTIVE} !important;
        }}
        div[data-testid="stSidebarNav"] a {{
            border-radius: 6px;
            padding: 8px 12px;
            margin: 2px 8px;
            font-weight: 500;
            font-size: 0.88rem;
        }}
        div[data-testid="stSidebarNav"] a:hover {{
            background-color: {SIDEBAR_ACTIVE_BG};
        }}
        div[data-testid="stSidebarNav"] li:has(a[aria-current="page"]) a {{
            background-color: {SIDEBAR_ACTIVE_BG};
            color: {SIDEBAR_TEXT_ACTIVE} !important;
        }}
        
        /* THE DEFINITIVE LINE REMOVAL FIX */
        /* Targets the exact border below the native navigation container */
        div[data-testid="stSidebarNav"] {{
            border-bottom: none !important;
        }}
        /* Removes any default markdown horizontal rules inside the sidebar */
        section[data-testid="stSidebar"] hr,
        section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] hr {{
            display: none !important;
            border: none !important;
            height: 0px !important;
        }}

        /* Push navigation list up so it never collides with the pinned footer */
        div[data-testid="stSidebarNav"] ul {{
            padding-bottom: 120px !important;
        }}

        /* ---- typography ---- */
        h1, h2, h3, h4 {{
            color: {TEXT_PRIMARY};
            font-weight: 700;
            letter-spacing: -0.01em;
        }}
        p, span, div, label {{
            color: {TEXT_PRIMARY};
        }}
        .cc-subtle {{
            color: {TEXT_SECONDARY};
            font-size: 0.92rem;
        }}
        .cc-muted {{
            color: {TEXT_MUTED};
            font-size: 0.82rem;
        }}

        /* ---- buttons ---- */
        .stButton > button {{
            background-color: {ACCENT};
            color: #FFFFFF;
            border: none;
            border-radius: {RADIUS};
            font-weight: 600;
            font-size: 0.88rem;
            padding: 0.5rem 1.1rem;
            transition: background-color 0.15s ease;
        }}
        .stButton > button:hover {{
            background-color: {ACCENT_HOVER};
            color: #FFFFFF;
        }}
        .stButton > button[kind="secondary"] {{
            background-color: #FFFFFF;
            color: {TEXT_PRIMARY};
            border: 1px solid {BORDER_STRONG};
        }}
        .stButton > button[kind="secondary"]:hover {{
            background-color: {NEUTRAL_SOFT};
            color: {TEXT_PRIMARY};
        }}

        /* ---- inputs ---- */
        .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {{
            border-radius: {RADIUS} !important;
            border: 1px solid {BORDER_STRONG} !important;
            background-color: #FFFFFF !important;
            color: {TEXT_PRIMARY} !important;
            -webkit-text-fill-color: {TEXT_PRIMARY} !important;
        }}
        .stTextArea textarea {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.85rem;
        }}

        /* ---- tabs ---- */
        button[data-baseweb="tab"] {{
            font-weight: 600;
            font-size: 0.88rem;
        }}
        div[data-baseweb="tab-highlight"] {{
            background-color: {ACCENT} !important;
        }}

        /* ---- generic card ---- */
        .cc-card {{
            background-color: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: {RADIUS};
            padding: 20px;
            box-shadow: {SHADOW};
        }}
        .cc-card-tight {{
            background-color: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: {RADIUS};
            padding: 14px 16px;
            box-shadow: {SHADOW};
        }}

        /* ---- kpi card ---- */
        .cc-kpi-label {{
            font-size: 0.82rem;
            color: {TEXT_SECONDARY};
            font-weight: 500;
            margin-bottom: 6px;
        }}
        .cc-kpi-value {{
            font-size: 1.9rem;
            font-weight: 800;
            color: {TEXT_PRIMARY};
            letter-spacing: -0.02em;
        }}
        .cc-kpi-delta-up {{
            color: {INFO};
            font-size: 0.78rem;
            font-weight: 600;
        }}
        .cc-kpi-delta-down {{
            color: {CRITICAL};
            font-size: 0.78rem;
            font-weight: 600;
        }}

        /* ---- chips / badges ---- */
        .cc-chip {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 999px;
            font-size: 0.74rem;
            font-weight: 600;
            white-space: nowrap;
        }}
        .cc-chip-critical {{ background:{CRITICAL_SOFT}; color:{CRITICAL}; border:1px solid {CRITICAL_BORDER}; }}
        .cc-chip-warning  {{ background:{WARNING_SOFT}; color:{WARNING}; border:1px solid {WARNING_BORDER}; }}
        .cc-chip-info     {{ background:{INFO_SOFT}; color:{INFO}; border:1px solid {INFO_BORDER}; }}
        .cc-chip-neutral  {{ background:{NEUTRAL_SOFT}; color:{TEXT_SECONDARY}; border:1px solid {BORDER}; }}
        .cc-chip-accent   {{ background:{ACCENT_SOFT}; color:{ACCENT}; border:1px solid #C7D2FE; }}

        /* ---- issue card ---- */
        .cc-issue {{
            border: 1px solid {BORDER};
            border-left: 3px solid {BORDER};
            border-radius: {RADIUS};
            padding: 14px 16px;
            margin-bottom: 10px;
            background: {CARD_BG};
        }}
        .cc-issue-critical {{ border-left-color: {CRITICAL}; }}
        .cc-issue-warning  {{ border-left-color: {WARNING}; }}
        .cc-issue-info     {{ border-left-color: {INFO}; }}

        .cc-issue-title {{
            font-weight: 600;
            font-size: 0.92rem;
            color: {TEXT_PRIMARY};
            margin-bottom: 2px;
        }}
        .cc-issue-meta {{
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.76rem;
            color: {TEXT_MUTED};
            margin-bottom: 8px;
        }}
        .cc-issue-body {{
            font-size: 0.86rem;
            color: {TEXT_SECONDARY};
            line-height: 1.5;
        }}
        .cc-issue-fix {{
            margin-top: 8px;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 0.78rem;
            background: {NEUTRAL_SOFT};
            border-radius: 6px;
            padding: 8px 10px;
            color: {TEXT_PRIMARY};
        }}

        /* ---- section header ---- */
        .cc-section-title {{
            font-size: 1.15rem;
            font-weight: 700;
            color: {TEXT_PRIMARY};
            margin-bottom: 2px;
        }}
        .cc-section-sub {{
            font-size: 0.85rem;
            color: {TEXT_SECONDARY};
            margin-bottom: 16px;
        }}

        /* ---- page heading scale (use these instead of bare st.markdown("##")) ---- */
        .cc-h1 {{
            font-size: 1.9rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: {TEXT_PRIMARY};
            margin-bottom: 4px;
            line-height: 1.2;
        }}
        .cc-h1-sub {{
            font-size: 0.95rem;
            color: {TEXT_SECONDARY};
            margin-bottom: 4px;
        }}

        /* ---- stat card with colored icon block (for liveliness on utility pages) ---- */
        .cc-stat-card {{
            background: {CARD_BG};
            border: 1px solid {BORDER};
            border-radius: {RADIUS};
            padding: 14px 16px;
            display: flex;
            align-items: center;
            gap: 12px;
            box-shadow: {SHADOW};
        }}
        .cc-stat-icon {{
            width: 38px;
            height: 38px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.95rem;
            flex-shrink: 0;
        }}
        .cc-stat-icon-violet {{ background: {VIOLET_SOFT}; color: {VIOLET}; }}
        .cc-stat-icon-blue   {{ background: {BLUE_SOFT}; color: {BLUE}; }}
        .cc-stat-icon-teal   {{ background: {TEAL_SOFT}; color: {TEAL}; }}
        .cc-stat-icon-accent {{ background: {ACCENT_SOFT}; color: {ACCENT}; }}
        .cc-stat-value {{
            font-size: 1.25rem;
            font-weight: 800;
            color: {TEXT_PRIMARY};
            line-height: 1.1;
        }}
        .cc-stat-label {{
            font-size: 0.76rem;
            color: {TEXT_SECONDARY};
            font-weight: 500;
        }}

        /* ---- clickable pick card (repo quick-select) ---- */
        .cc-pick-card {{
            border: 1px solid {BORDER};
            border-left: 3px solid {ACCENT};
            border-radius: {RADIUS};
            padding: 12px 14px;
            background: {CARD_BG};
            transition: box-shadow 0.15s ease, border-color 0.15s ease;
        }}
        .cc-pick-card:hover {{
            box-shadow: 0 2px 6px rgba(16,24,40,0.08);
        }}

        /* ---- segmented control (used instead of default radio for input mode) ---- */
        div[data-testid="stRadio"] > div {{
            gap: 4px;
            background: {NEUTRAL_SOFT};
            padding: 4px;
            border-radius: 8px;
            display: inline-flex;
        }}
        div[data-testid="stRadio"] label {{
            padding: 6px 14px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.85rem;
        }}
        div[data-testid="stRadio"] label:has(input:checked) {{
            background: {CARD_BG};
            box-shadow: {SHADOW};
        }}

        hr {{
            border-color: {BORDER};
        }}

        /* ---- top bar (breadcrumb + page title, sits above every app page) ---- */
        .cc-topbar {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            border-bottom: 1px solid {BORDER};
            padding-bottom: 16px;
            margin-bottom: 24px;
        }}
        .cc-breadcrumb {{
            font-size: 0.78rem;
            color: {TEXT_MUTED};
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 4px;
        }}
        .cc-page-title {{
            font-size: 1.7rem;
            font-weight: 800;
            color: {TEXT_PRIMARY};
            letter-spacing: -0.02em;
            line-height: 1.2;
        }}
        .cc-page-sub {{
            font-size: 0.9rem;
            color: {TEXT_SECONDARY};
            margin-top: 2px;
        }}

        /* ---- segmented control (replaces default radio styling) ---- */
        .cc-seg-active > button {{
            background-color: {ACCENT} !important;
            color: #FFFFFF !important;
        }}

        /* ---- colored accent cards / left-border variants ---- */
        .cc-accent-indigo {{ border-left: 3px solid {ACCENT}; }}
        .cc-accent-teal   {{ border-left: 3px solid #0D9488; }}
        .cc-accent-amber  {{ border-left: 3px solid {WARNING}; }}
        .cc-accent-rose   {{ border-left: 3px solid {CRITICAL}; }}

        /* ---- stat pill (small colored stat block, more lively than plain kpi) ---- */
        .cc-stat-pill {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 14px;
            border-radius: {RADIUS};
            border: 1px solid {BORDER};
            background: {CARD_BG};
        }}
        .cc-stat-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            flex-shrink: 0;
        }}
        .cc-stat-value {{
            font-size: 1.15rem;
            font-weight: 700;
            color: {TEXT_PRIMARY};
            line-height: 1.1;
        }}
        .cc-stat-label {{
            font-size: 0.72rem;
            color: {TEXT_SECONDARY};
            font-weight: 500;
        }}

        .cc-step-badge {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 22px;
            height: 22px;
            border-radius: 6px;
            background: {ACCENT};
            color: #FFFFFF;
            font-size: 0.72rem;
            font-weight: 700;
            margin-right: 8px;
        }}

        /* ---- pin the sidebar brand block near the bottom ---- */
        section[data-testid="stSidebar"] {{
            position: relative;
        }}
        
        .cc-sidebar-footer {{
            position: fixed;
            bottom: 0;
            left: 0;
            width: 18rem;
            background: {SIDEBAR_BG};
            padding: 20px 24px 28px 24px;
            box-sizing: border-box;
            border-top: 1px solid #1F2937;
            z-index: 99;
        }}

        @media (max-width: 768px) {{
            .cc-sidebar-footer {{
                width: 100%;
                position: relative;
            }}
        }}

        /* ---- landing page top nav ---- */
        .cc-landing-nav {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 4px 0 20px 0;
            border-bottom: 1px solid {BORDER};
            margin-bottom: 8px;
        }}
        .cc-landing-logo {{
            font-size: 2.1rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: {TEXT_PRIMARY};
        }}
        .cc-landing-tagline {{
            font-size: 0.88rem;
            color: {TEXT_SECONDARY};
            font-weight: 500;
            letter-spacing: 0.01em;
            margin-top: 4px;
        }}
        .cc-landing-links a {{
            color: {TEXT_SECONDARY};
            text-decoration: none;
            font-size: 0.86rem;
            font-weight: 500;
            margin-right: 28px;
        }}
        .cc-landing-links a:hover {{
            color: {TEXT_PRIMARY};
        }}

        /* ---- anchor styled as a button ---- */
        .cc-btn-link {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 0.5rem 1.1rem;
            border-radius: {RADIUS};
            border: 1px solid {BORDER_STRONG};
            background: #FFFFFF;
            color: {TEXT_PRIMARY} !important;
            font-weight: 600;
            font-size: 0.88rem;
            text-decoration: none !important;
            box-sizing: border-box;
        }}
        .cc-btn-link:hover {{
            background: {NEUTRAL_SOFT};
        }}

        /* ---- stepper (Live Review page) ---- */
        .cc-step-row {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 0;
        }}
        .cc-step-icon {{
            width: 26px;
            height: 26px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            font-weight: 700;
            flex-shrink: 0;
        }}
        .cc-step-icon-done {{ background: {INFO_SOFT}; color: {INFO}; }}
        .cc-step-icon-active {{ background: {ACCENT_SOFT}; color: {ACCENT}; }}
        .cc-step-icon-pending {{ background: {NEUTRAL_SOFT}; color: {TEXT_MUTED}; }}
        .cc-step-label-done {{ color: {TEXT_PRIMARY}; font-weight: 600; font-size: 0.88rem; }}
        .cc-step-label-active {{ color: {ACCENT}; font-weight: 700; font-size: 0.88rem; }}
        .cc-step-label-pending {{ color: {TEXT_MUTED}; font-weight: 500; font-size: 0.88rem; }}
        .cc-step-connector {{
            width: 1px;
            height: 18px;
            background: {BORDER};
            margin-left: 13px;
        }}

        /* ---- severity bar chart (Report page) ---- */
        .cc-bar-row {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}
        .cc-bar-label {{
            width: 70px;
            font-size: 0.8rem;
            font-weight: 600;
            color: {TEXT_SECONDARY};
            flex-shrink: 0;
        }}
        .cc-bar-track {{
            flex-grow: 1;
            height: 10px;
            background: {NEUTRAL_SOFT};
            border-radius: 999px;
            overflow: hidden;
        }}
        .cc-bar-fill {{
            height: 100%;
            border-radius: 999px;
        }}
        .cc-bar-count {{
            width: 24px;
            text-align: right;
            font-size: 0.82rem;
            font-weight: 700;
            color: {TEXT_PRIMARY};
            flex-shrink: 0;
        }}

        /* ---- dataframe / table ---- */
        div[data-testid="stDataFrame"] {{
            border: 1px solid {BORDER};
            border-radius: {RADIUS};
        }}

        code {{
            font-family: 'IBM Plex Mono', monospace;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )