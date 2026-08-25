import streamlit as st

def inject_custom_css():
    """
    Injects custom Modern Dark Glassmorphism Control Room CSS.
    Provides responsive layout styling, metric card aesthetics, button accents, and status badges.
    """
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

        /* Base Control Room Theme */
        .stApp {
            background-color: #07090e;
            background-image: 
                radial-gradient(at 0% 0%, rgba(56, 189, 248, 0.06) 0px, transparent 50%),
                radial-gradient(at 100% 0%, rgba(129, 140, 248, 0.06) 0px, transparent 50%);
            color: #F8FAFC;
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* Top Header Banner */
        .main-header {
            background: linear-gradient(135deg, rgba(13, 18, 30, 0.8) 0%, rgba(7, 9, 14, 0.95) 100%);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 24px 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(16px);
        }
        .main-header h1 {
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.025em;
        }
        .main-header p {
            color: #94A3B8;
            margin-top: 6px;
            margin-bottom: 0;
            font-size: 1.025rem;
        }

        /* Glassmorphism Card Containers */
        .glass-card {
            background-color: rgba(13, 18, 30, 0.75);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            padding: 22px;
            margin-bottom: 20px;
            box-shadow: 0 8px 24px -8px rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(16px);
            transition: all 0.25s ease;
        }
        .glass-card:hover {
            border-color: rgba(56, 189, 248, 0.3);
            box-shadow: 0 12px 32px -10px rgba(56, 189, 248, 0.15);
        }

        /* Custom Metric Cards */
        div[data-testid="metric-container"] {
            background-color: rgba(13, 18, 30, 0.8) !important;
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
            background-color: rgba(52, 211, 153, 0.12);
            color: #34D399;
            border: 1px solid rgba(52, 211, 153, 0.3);
            padding: 4px 14px;
            border-radius: 9999px;
            font-size: 0.825rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .status-badge-offline {
            background-color: rgba(239, 68, 68, 0.12);
            color: #F87171;
            border: 1px solid rgba(239, 68, 68, 0.3);
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
            background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%);
            color: #FFFFFF;
            border: none;
            font-weight: 700;
            padding: 10px 22px;
            transition: all 0.2s ease;
            box-shadow: 0 4px 14px rgba(2, 132, 199, 0.25);
        }
        .stButton>button:hover {
            background: linear-gradient(135deg, #38bdf8 0%, #6366f1 100%);
            box-shadow: 0 6px 20px rgba(56, 189, 248, 0.4);
            transform: translateY(-1px);
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0B0F19 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        /* Table Styling */
        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            overflow: hidden;
        }
        </style>
    """, unsafe_allow_html=True)

