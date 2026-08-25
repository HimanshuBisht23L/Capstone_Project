import streamlit as st

def inject_custom_css():
    """
    Injects custom Modern Dark Glassmorphism Control Room CSS.
    Provides responsive layout styling, metric card aesthetics, button accents, and status badges.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        /* Base Control Room Theme Overrides (Enforce Dark Mode in Light Browser Settings) */
        header[data-testid="stHeader"] {
            background-color: #07090e !important;
            color: #F8FAFC !important;
        }

        div[data-testid="stAppViewContainer"] {
            background-color: #07090e !important;
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.06) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(129, 140, 248, 0.06) 0px, transparent 50%) !important;
            color: #F8FAFC !important;
        }

        .stApp {
            background-color: #07090e !important;
            color: #F8FAFC !important;
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* Force Sidebar Theme & Text Colors */
        section[data-testid="stSidebar"] {
            background-color: #0d121e !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        section[data-testid="stSidebar"] * {
            color: #CBD5E1 !important;
        }

        [data-testid="stSidebarNav"] a span,
        [data-testid="stSidebarNavItems"] span,
        section[data-testid="stSidebar"] a span {
            color: #E2E8F0 !important;
            font-weight: 500 !important;
        }

        /* General Markdown & Text Contrast Overrides */
        .stMarkdown p, .stMarkdown span, .stMarkdown li, .stMarkdown td, .stMarkdown th {
            color: #F8FAFC !important;
        }

        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
            color: #F8FAFC !important;
        }

        /* Form Inputs & Selectboxes */
        .stSelectbox label, .stTextInput label, .stTextArea label, .stFileUploader label, .stSlider label {
            color: #94A3B8 !important;
            font-weight: 600 !important;
        }

        .stSelectbox [data-baseweb="select"], .stTextInput input, .stTextArea textarea {
            background-color: #07090e !important;
            color: #F8FAFC !important;
            border-color: rgba(255, 255, 255, 0.15) !important;
        }

        /* Top Header Banner */
        .main-header {
            background: linear-gradient(135deg, rgba(13, 18, 30, 0.85) 0%, rgba(7, 9, 14, 0.95) 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 16px;
            padding: 24px 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(16px);
        }
        .main-header h1 {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%) !important;
            -webkit-background-clip: text !important;
            background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin: 0;
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.025em;
        }
        .main-header p {
            color: #94A3B8 !important;
            margin-top: 6px;
            margin-bottom: 0;
            font-size: 1.025rem;
        }

        /* Glassmorphism Card Containers */
        .glass-card {
            background-color: rgba(13, 18, 30, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 20px;
            box-shadow: 0 8px 24px -8px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(16px);
            transition: all 0.25s ease;
        }
        .glass-card:hover {
            border-color: rgba(56, 189, 248, 0.3) !important;
            box-shadow: 0 12px 32px -10px rgba(56, 189, 248, 0.15);
        }

        /* Custom Metric Cards */
        div[data-testid="metric-container"] {
            background-color: rgba(13, 18, 30, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            padding: 16px 20px !important;
            box-shadow: 0 6px 16px -4px rgba(0, 0, 0, 0.3) !important;
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        }
        div[data-testid="metric-container"]:hover {
            border-color: rgba(56, 189, 248, 0.4) !important;
            transform: translateY(-2px);
            box-shadow: 0 8px 20px -4px rgba(56, 189, 248, 0.15) !important;
        }
        div[data-testid="metric-container"] label {
            color: #94A3B8 !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #38BDF8 !important;
            font-size: 1.6rem !important;
            font-weight: 800 !important;
        }

        /* Status Badges */
        .status-badge-online {
            background-color: rgba(52, 211, 153, 0.12) !important;
            color: #34D399 !important;
            border: 1px solid rgba(52, 211, 153, 0.3) !important;
            padding: 4px 14px;
            border-radius: 9999px;
            font-size: 0.825rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .status-badge-offline {
            background-color: rgba(239, 68, 68, 0.12) !important;
            color: #F87171 !important;
            border: 1px solid rgba(239, 68, 68, 0.3) !important;
            padding: 4px 14px;
            border-radius: 9999px;
            font-size: 0.825rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        /* Form Buttons */
        .stButton>button {
            border-radius: 10px;
            background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            font-weight: 700;
            padding: 10px 22px;
            transition: all 0.2s ease;
            box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25);
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #38bdf8 0%, #6366f1 100%) !important;
            box-shadow: 0 6px 20px rgba(56, 189, 248, 0.4);
            transform: translateY(-1px);
        }

        /* Table Styling */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px;
            overflow: hidden;
        }

        </style>
    """, unsafe_allow_html=True)

