import streamlit as st
import pandas as pd
import io
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.state_manager import StateManager
from components.custom_css import inject_custom_css
from components.kpi_cards import render_kpi_header
from components.sidebar import render_sidebar

def main():
    st.set_page_config(page_title="Dataset Explorer — SheetPilot AI", page_icon="🔍", layout="wide")
    inject_custom_css()
    StateManager.init_state()
    render_sidebar()

    st.title("🔍 Dataset Explorer & Ground Truth Editor")
    st.caption("Inspect tabular schemas, view missing data diagnostics, and perform interactive ground-truth dataset edits.")
    st.markdown("---")

    render_kpi_header()
    st.markdown("<br>", unsafe_allow_html=True)

    raw_df = st.session_state.get("raw_dataframe")
    result_df = st.session_state.get("execution_result_df")
    file_name = st.session_state.get("uploaded_file_name", "Dataset")

    if raw_df is None:
        st.info("💡 No active dataset loaded. Please upload a file or select a benchmark dataset in the **Prompt Playground** first.")
        st.stop()

    tab_orig, tab_trans, tab_stats = st.tabs(["📄 Original Dataset Editor", "✨ Transformed Result Output", "📊 Column Statistics & Profiling"])

    with tab_orig:
        st.subheader(f"Interactive Editor — `{file_name}`")
        st.caption("Edit cells below to update ground-truth values in session state.")
        
        edited_df = st.data_editor(raw_df, key="original_data_editor", use_container_width=True, num_rows="dynamic")
        
        # Download edited dataset
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            edited_df.to_excel(writer, index=False)
        
        st.download_button(
            label="📥 Export Edited Ground-Truth Workbook (.xlsx)",
            data=buffer.getvalue(),
            file_name=f"GroundTruth_{file_name}",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            key="export_ground_truth_btn"
        )

    with tab_trans:
        st.subheader("Transformed Output Dataset")
        if result_df is not None:
            st.dataframe(result_df, use_container_width=True)
            
            res_buffer = io.BytesIO()
            with pd.ExcelWriter(res_buffer, engine="openpyxl") as writer:
                result_df.to_excel(writer, index=False)
                
            st.download_button(
                label="📥 Download Transformed Result (.xlsx)",
                data=res_buffer.getvalue(),
                file_name=f"SheetPilot_Result_{file_name}",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="export_transformed_explorer_btn"
            )
        else:
            st.info("No transformation has been executed yet in this session. Execute a prompt in the **Prompt Playground** to inspect results here.")

    with tab_stats:
        st.subheader("Column Schema Profiling")
        
        stats_list = []
        for col in raw_df.columns:
            series = raw_df[col]
            stats_list.append({
                "Column Name": col,
                "Data Type": str(series.dtype),
                "Total Count": len(series),
                "Non-Null Count": series.count(),
                "Null Count": series.isnull().sum(),
                "Unique Values": series.nunique(),
                "Sample Values": ", ".join([str(v) for v in series.dropna().unique()[:3]])
            })
            
        stats_df = pd.DataFrame(stats_list)
        st.dataframe(stats_df, use_container_width=True)

if __name__ == "__main__":
    main()
