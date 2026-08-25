import streamlit as st
from typing import Optional

def render_kpi_header():
    """
    Renders data-driven KPI metric cards at the top of pages.
    Displays dynamic metrics from session state or neutral placeholder values '—'.
    STRICT REQUIREMENT: Zero fake or hardcoded metrics.
    """
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # 1. Backend Status
    backend_online = st.session_state.get("backend_online", False)
    status_label = "🟢 Online" if backend_online else "🔴 Offline"
    col1.metric(label="System Status", value=status_label)
    
    # 2. Active Dataset Name
    file_name = st.session_state.get("uploaded_file_name")
    display_file = file_name if file_name else "No dataset loaded"
    col2.metric(label="Active Dataset", value=display_file)
    
    # 3. Row Count
    raw_df = st.session_state.get("raw_dataframe")
    result_df = st.session_state.get("execution_result_df")
    
    if result_df is not None:
        row_str = f"{len(result_df)} (Output)"
    elif raw_df is not None:
        row_str = f"{len(raw_df)} (Input)"
    else:
        row_str = "—"
    col3.metric(label="Total Rows", value=row_str)
    
    # 4. Column Count
    if result_df is not None:
        col_str = f"{len(result_df.columns)}"
    elif raw_df is not None:
        col_str = f"{len(raw_df.columns)}"
    else:
        col_str = "—"
    col4.metric(label="Total Columns", value=col_str)
    
    # 5. Execution Time Latency
    exec_time = st.session_state.get("execution_time_ms", 0)
    time_str = f"{exec_time} ms" if exec_time > 0 else "Not executed"
    col5.metric(label="Execution Time", value=time_str)
