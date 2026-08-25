import streamlit as st
from utils.state_manager import StateManager
from utils.api_client import SheetPilotAPIClient

def render_sidebar():
    """
    Renders persistent sidebar containing system connectivity, active dataset info,
    backend URL settings, and session reset button.
    """
    with st.sidebar:
        st.title("⚡ SheetPilot AI")
        st.caption("Control Room Telemetry & Controls")
        st.markdown("---")
        
        # 1. System Connection Status
        st.subheader("System Status")
        backend_online = st.session_state.get("backend_online", False)
        base_url = SheetPilotAPIClient.get_base_url()
        
        if backend_online:
            st.markdown('<div class="status-badge-online">🟢 Backend Connected</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-badge-offline">🔴 Backend Unavailable</div>', unsafe_allow_html=True)
        
        st.caption(f"Endpoint: `{base_url}`")
        
        # Re-check Health Button
        if st.button("🔌 Re-check Connection", key="recheck_health_btn", use_container_width=True):
            online, health_data = SheetPilotAPIClient.check_health()
            st.session_state.backend_online = online
            st.session_state.backend_health = health_data
            st.rerun()
            
        st.markdown("---")
        
        # 2. Active Dataset Metadata Summary
        st.subheader("📁 Active Dataset")
        file_name = st.session_state.get("uploaded_file_name")
        file_id = st.session_state.get("uploaded_file_id")
        schema = st.session_state.get("dataset_schema")
        
        if file_name and file_id:
            st.success(f"**{file_name}**")
            st.caption(f"File ID: `{file_id[:8]}...`")
            
            raw_df = st.session_state.get("raw_dataframe")
            if raw_df is not None:
                st.write(f"• Rows: `{len(raw_df)}`")
                st.write(f"• Columns: `{len(raw_df.columns)}`")
            
            if schema and "sheets" in schema:
                st.write(f"• Total Sheets: `{schema.get('total_sheets', 1)}`")
        else:
            st.info("No dataset loaded in session.")
            
        st.markdown("---")
        
        # 3. Workspace Session Controls
        st.subheader("⚙️ Session Controls")
        if st.button("🔄 Reset Workspace Session", key="reset_session_btn", use_container_width=True):
            StateManager.reset_session()
            st.toast("Workspace session cleared successfully!", icon="🧹")
            st.rerun()
            
        st.caption("SheetPilot AI v2.5 — Control Room Frontend")
