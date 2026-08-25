import streamlit as st
import os
import sys

# Ensure streamlit_app root is in Python path for clean module imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.state_manager import StateManager
from utils.api_client import SheetPilotAPIClient
from components.custom_css import inject_custom_css
from components.kpi_cards import render_kpi_header
from components.sidebar import render_sidebar

def main():
    # 1. Page Configuration & Layout Setup
    st.set_page_config(
        page_title="SheetPilot AI Control Room",
        page_icon="⚡",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 2. Inject Custom Theme & Initialize Session State
    inject_custom_css()
    StateManager.init_state()
    
    # 3. Check Backend Health on Initial Load
    if not st.session_state.get("backend_online"):
        online, health_data = SheetPilotAPIClient.check_health()
        st.session_state.backend_online = online
        st.session_state.backend_health = health_data

    # 4. Render Persistent Navigation & Sidebar
    render_sidebar()

    # 5. Render Top Hero Banner
    st.markdown("""
        <div class="main-header">
            <h1>SheetPilot AI — Control Room</h1>
            <p>Enterprise AI-Powered Spreadsheet Transformation & Analysis Engine</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 6. Render Data-Driven KPI Metrics Header
    render_kpi_header()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 7. Navigation Guidance & Core Architecture Features
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("🎯 Operational Workflow")
        st.markdown("""
        SheetPilot AI operates as a deterministic, AST-sandboxed automation client:
        
        1. **📁 Upload Spreadsheet**: Select a multi-sheet Excel or CSV dataset or choose from 10 enterprise benchmark files.
        2. **💬 Enter Instruction**: Express complex filtering, calculations, text replacements, or multi-step transforms in plain English.
        3. **⚙️ AI Plan Synthesis**: SheetPilot parses column schemas and generates structured operation steps and Pandas scripts.
        4. **🛡️ AST Security Verification**: Code is statically audited by a security AST visitor before subprocess isolation.
        5. **⚡ Execution & Inspection**: Download the transformed workbook and audit cell-level differential metrics.
        """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("👈 **Navigate using the sidebar menu** to access the **Prompt Playground**, **Dataset Explorer**, and **Prompt Inspector**.")

    with col2:
        st.subheader("🛡️ Security & Integrity Matrix")
        st.markdown("""
        - **Zero Code Execution on Frontend**: All script execution is handled via isolated Python subprocess sandboxes on the FastAPI backend.
        - **Static AST Auditor**: Blocks unsafe operations (`os`, `sys`, `subprocess`, `eval`, `exec`, `open`, network requests).
        - **Data Integrity**: Enforces strict header detection and zero metric fabrication.
        """)
        
        if not st.session_state.backend_online:
            st.warning("⚠️ **Backend is currently offline.** Please ensure the FastAPI server is running on `http://localhost:8000` or configure `SHEETPILOT_BACKEND_URL`.")

if __name__ == "__main__":
    main()
