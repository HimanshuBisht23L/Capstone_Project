import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any

class StateManager:
    """
    Centralized Session State Manager for SheetPilot AI Streamlit Control Room.
    Enforces clean state initialization, reset protocols, and stale state eviction.
    """
    
    @staticmethod
    def init_state():
        """Initializes default values for all session state keys if not already present."""
        defaults: Dict[str, Any] = {
            "backend_online": False,
            "backend_health": {},
            "uploaded_file_id": None,
            "uploaded_file_name": None,
            "uploaded_file_bytes": None,
            "raw_dataframe": None,
            "dataset_schema": None,
            "current_prompt": "",
            "active_plan_id": None,
            "active_plan_payload": None,
            "generated_code": None,
            "active_job_id": None,
            "execution_status": "IDLE",
            "execution_result_df": None,
            "execution_time_ms": 0,
            "execution_diff": None,
            "execution_error": None,
            "selected_benchmark_name": None,
            "ast_security_passed": None
        }
        for key, val in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = val

    @staticmethod
    def reset_session():
        """Clears all session state variables and re-initializes clean defaults."""
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        StateManager.init_state()

    @staticmethod
    def set_file_data(file_id: str, file_name: str, file_bytes: bytes, df: Optional[pd.DataFrame], schema: Optional[dict]):
        """
        Updates session state with newly uploaded or selected dataset,
        and evicts stale downstream plan, execution, and error states.
        """
        st.session_state.uploaded_file_id = file_id
        st.session_state.uploaded_file_name = file_name
        st.session_state.uploaded_file_bytes = file_bytes
        st.session_state.raw_dataframe = df
        st.session_state.dataset_schema = schema
        
        # Evict stale downstream states to prevent cross-dataset leakage
        st.session_state.active_plan_id = None
        st.session_state.active_plan_payload = None
        st.session_state.generated_code = None
        st.session_state.active_job_id = None
        st.session_state.execution_status = "IDLE"
        st.session_state.execution_result_df = None
        st.session_state.execution_diff = None
        st.session_state.execution_error = None
        st.session_state.ast_security_passed = None

    @staticmethod
    def clear_execution_data():
        """Clears execution metrics, errors, and output dataframe when a prompt is edited."""
        st.session_state.active_job_id = None
        st.session_state.execution_status = "IDLE"
        st.session_state.execution_result_df = None
        st.session_state.execution_diff = None
        st.session_state.execution_error = None
        st.session_state.execution_time_ms = 0
