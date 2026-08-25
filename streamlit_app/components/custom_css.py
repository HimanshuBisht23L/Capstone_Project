import streamlit as st

def inject_custom_css():
    """
    Injects custom Modern Dark Glassmorphism Control Room CSS.
    Provides responsive layout styling, metric card aesthetics, button accents, and status badges.
    """
    st.markdown("""
        <style>
        /* Base Control Room Theme */
        .stApp {
            background-color: #0B0F19;
            color: #F9FAFB;
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* Top Header Banner */
        .main-header {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.9) 100%);
            border: 1px solid #1F2937;
            border-radius: 12px;
            padding: 24px 32px;
            margin-bottom: 24px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
        }
        .main-header h1 {
            color: #3B82F6;
            margin: 0;
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.025em;
        }
        .main-header p {
            color: #9CA3AF;
            margin-top: 6px;
            margin-bottom: 0;
            font-size: 1.05rem;
        }

        /* Glassmorphism Card Containers */
        .glass-card {
            background-color: #111827;
            border: 1px solid #1F2937;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }

        /* Custom Metric Cards */
        div[data-testid="metric-container"] {
            background-color: #111827 !important;
            border: 1px solid #1F2937 !important;
            border-radius: 8px !important;
            padding: 14px 18px !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.15) !important;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        div[data-testid="metric-container"]:hover {
            border-color: #3B82F6 !important;
            transform: translateY(-2px);
        }
        div[data-testid="metric-container"] label {
            color: #9CA3AF !important;
            font-size: 0.825rem !important;
            font-weight: 500 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #3B82F6 !important;
            font-size: 1.5rem !important;
            font-weight: 700 !important;
        }

        /* Status Badges */
        .status-badge-online {
            background-color: rgba(16, 185, 129, 0.15);
            color: #10B981;
            border: 1px solid rgba(16, 185, 129, 0.3);
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }
        .status-badge-offline {
            background-color: rgba(239, 68, 68, 0.15);
            color: #EF4444;
            border: 1px solid rgba(239, 68, 68, 0.3);
            padding: 4px 12px;
            border-radius: 9999px;
            font-size: 0.85rem;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }

        /* Form Buttons */
        .stButton>button {
            border-radius: 8px;
            background-color: #2563EB;
            color: #FFFFFF;
            border: none;
            font-weight: 600;
            padding: 10px 20px;
            transition: all 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #1D4ED8;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #0F172A !important;
            border-right: 1px solid #1F2937 !important;
        }

        /* Table Styling */
        div[data-testid="stDataFrame"] {
            border: 1px solid #1F2937;
            border-radius: 8px;
            overflow: hidden;
        }
        </style>
    """, unsafe_allow_html=True)
