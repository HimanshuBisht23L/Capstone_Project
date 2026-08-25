import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.state_manager import StateManager
from utils.api_client import SheetPilotAPIClient
from components.custom_css import inject_custom_css
from components.kpi_cards import render_kpi_header
from components.sidebar import render_sidebar

def main():
    st.set_page_config(page_title="Overview — SheetPilot AI", page_icon="📊", layout="wide")
    inject_custom_css()
    StateManager.init_state()
    render_sidebar()

    st.title("📊 System Overview & Telemetry")
    st.caption("Real-time operational status, backend health metrics, and active dataset diagnostics.")
    st.markdown("---")
    
    render_kpi_header()
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([1, 1])
    
    # 1. Backend Telemetry Container
    with col_left:
        st.subheader("🖥️ FastAPI Backend Health")
        backend_online = st.session_state.get("backend_online", False)
        health_data = st.session_state.get("backend_health", {})
        
        if backend_online:
            st.success("FastAPI REST Gateway: Operational")
            st.json(health_data)
        else:
            st.error("FastAPI REST Gateway: Unavailable")
            st.write("Unable to reach backend health endpoint.")
            if st.button("Retry Health Check"):
                online, h_data = SheetPilotAPIClient.check_health()
                st.session_state.backend_online = online
                st.session_state.backend_health = h_data
                st.rerun()

    # 2. Active Dataset Diagnostics
    with col_right:
        st.subheader("📋 Dataset Telemetry")
        raw_df = st.session_state.get("raw_dataframe")
        file_name = st.session_state.get("uploaded_file_name")
        schema = st.session_state.get("dataset_schema")
        
        if raw_df is not None and file_name:
            st.markdown(f"**Dataset Name:** `{file_name}`")
            st.markdown(f"**Dimensions:** `{len(raw_df)}` rows × `{len(raw_df.columns)}` columns")
            
            # Missing Value Distribution Chart
            missing_counts = raw_df.isnull().sum()
            missing_cols = missing_counts[missing_counts > 0]
            
            if not missing_cols.empty:
                st.write("**Missing Values per Column:**")
                st.bar_chart(missing_cols)
            else:
                st.info("✅ Zero null/missing values detected across all columns.")
                
            # Column Data Type Distribution
            dtype_counts = raw_df.dtypes.value_counts().astype(str)
            st.write("**Column Dtypes:**")
            st.dataframe(pd.DataFrame({"Count": raw_df.dtypes.value_counts()}), use_container_width=True)
        else:
            st.info("No active dataset loaded in session. Navigate to the **Prompt Playground** to upload an Excel/CSV file or select a benchmark dataset.")

if __name__ == "__main__":
    main()
