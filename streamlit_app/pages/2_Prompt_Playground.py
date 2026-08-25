import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.state_manager import StateManager
from utils.api_client import SheetPilotAPIClient
from utils.data_loader import DataLoader
from components.custom_css import inject_custom_css
from components.kpi_cards import render_kpi_header
from components.sidebar import render_sidebar

# Standard Benchmark Test Prompts Map
BENCHMARK_PROMPTS = {
    "1_Employee_Payroll_Tax.xlsx": "Filter rows where Department is IT / Software and Base Salary is above 70000",
    "2_GST_Sales_Register.xlsx": "Filter rows where State is Maharashtra and Payment Status is Completed",
    "3_Corporate_Expenses.xlsx": "Filter rows where Amount is greater than 50000 and Status is Approved",
    "4_Quarterly_Financial_Revenue.xlsx": "Calculate a new column H2_Revenue as Q3_Revenue + Q4_Revenue",
    "5_Inventory_Stock_Audit.xlsx": "Filter rows where Stock Status is Low Stock",
    "6_TDS_Deduction_Report.xlsx": "Filter rows where Section is 194J",
    "7_Client_Invoicing_AR.xlsx": "Filter rows where Balance Due is greater than 20000",
    "8_Profit_Loss_Statement.xlsx": "Filter rows where Branch Tier is Tier A",
    "9_Bank_Reconciliation.xlsx": "Filter rows where Status is Pending",
    "10_Student_Academic_Grades.xlsx": "Filter rows where Stream is CS and Attendance Percentage is above 90"
}

def main():
    st.set_page_config(page_title="Prompt Playground — SheetPilot AI", page_icon="🧪", layout="wide")
    inject_custom_css()
    StateManager.init_state()
    render_sidebar()

    st.title("🧪 Prompt Playground & Execution Engine")
    st.caption("Upload workbooks or select benchmark datasets, enter natural language instructions, and execute sandboxed transformations.")
    st.markdown("---")

    render_kpi_header()
    st.markdown("<br>", unsafe_allow_html=True)

    # ---------------------------------------------------------
    # STEP 1: DATASET SELECTION & UPLOAD
    # ---------------------------------------------------------
    st.subheader("1. Load Spreadsheet Dataset")
    
    uploaded_file = st.file_uploader(
        "Choose an Excel (.xlsx, .xls) or CSV (.csv) workbook up to 50MB",
        type=["xlsx", "xls", "csv"],
        key="file_uploader_widget"
    )
    
    if uploaded_file is not None:
        # Check if this file is already active to avoid redundant upload calls
        if st.session_state.get("uploaded_file_name") != uploaded_file.name:
            with st.spinner(f"Uploading and extracting schema for {uploaded_file.name}..."):
                file_bytes = uploaded_file.getvalue()
                success, resp = SheetPilotAPIClient.upload_file(file_bytes, uploaded_file.name)
                
                if success:
                    file_id = resp["file_id"]
                    schema = resp.get("schema_info", {})
                    df = DataLoader.load_dataframe_from_bytes(file_bytes, uploaded_file.name)
                    
                    # Store in state and clear stale downstream state
                    StateManager.set_file_data(file_id, uploaded_file.name, file_bytes, df, schema)
                    st.toast(f"File {uploaded_file.name} uploaded successfully!", icon="✅")
                    st.rerun()
                else:
                    st.error(f"Upload failed: {resp.get('error', 'Unknown error')}")

    # Display Active Dataset Summary Card & Top 5 Row Preview
    current_file_id = st.session_state.get("uploaded_file_id")
    raw_df = st.session_state.get("raw_dataframe")
    file_name = st.session_state.get("uploaded_file_name")

    if current_file_id and raw_df is not None:
        with st.expander(f"📋 Dataset Preview & Column Schema — `{file_name}`", expanded=True):
            st.dataframe(raw_df.head(5), use_container_width=True)
            col_cols = list(raw_df.columns)
            st.caption(f"**Detected Columns ({len(col_cols)}):** `{'`, `'.join(str(c) for c in col_cols)}`")
    else:
        st.info("💡 Please upload an Excel or CSV file above to enable prompt execution.")
        st.stop()

    st.markdown("---")

    # ---------------------------------------------------------
    # STEP 2: PROMPT INPUT FORM & QUICK EXAMPLES
    # ---------------------------------------------------------
    st.subheader("2. Enter Natural Language Instruction")

    # Quick Example Prompt Buttons
    if file_name in BENCHMARK_PROMPTS:
        recommended = BENCHMARK_PROMPTS[file_name]
        st.markdown(f"💡 **Recommended Benchmark Prompt:** *\"{recommended}\"*")
        if st.button("✨ Insert Recommended Prompt", key="fill_prompt_btn"):
            st.session_state.current_prompt = recommended
            st.rerun()

    with st.form("prompt_execution_form"):
        user_prompt = st.text_area(
            "What transformation or analysis should SheetPilot AI perform?",
            value=st.session_state.get("current_prompt", ""),
            placeholder="e.g., Filter rows where Department is IT / Software and Base Salary > 70000",
            height=100
        )
        
        submit_btn = st.form_submit_button("🚀 Run with SheetPilot AI", use_container_width=True)

    if submit_btn:
        if not user_prompt.strip():
            st.warning("Please enter a natural language prompt before running.")
        else:
            st.session_state.current_prompt = user_prompt.strip()
            # Clear previous execution outputs
            StateManager.clear_execution_data()
            
            # Trigger Plan Generation
            with st.spinner("Synthesizing AI Action Plan & Generating Code..."):
                success, plan_resp = SheetPilotAPIClient.generate_plan(current_file_id, user_prompt)
                
                if success:
                    plan_data = plan_resp.get("plan", {})
                    
                    # Check for Clarification Request
                    if plan_data.get("requires_clarification"):
                        st.warning("⚠️ **Clarification Requested by AI Engine:**")
                        st.write(plan_data.get("clarification_message", "The instruction was ambiguous."))
                        st.session_state.active_plan_id = None
                    else:
                        st.session_state.active_plan_id = plan_resp.get("plan_id")
                        st.session_state.active_plan_payload = plan_data
                        st.session_state.generated_code = plan_resp.get("generated_code")
                        st.toast("Action plan synthesized successfully!", icon="⚙️")
                else:
                    st.error(f"Plan Generation Failed: {plan_resp.get('error')}")

    # ---------------------------------------------------------
    # STEP 3: ACTION PLAN & GENERATED CODE PREVIEW
    # ---------------------------------------------------------
    active_plan = st.session_state.get("active_plan_payload")
    gen_code = st.session_state.get("generated_code")
    active_plan_id = st.session_state.get("active_plan_id")

    if active_plan and active_plan_id:
        st.subheader("3. Action Plan & Code Inspection")
        
        col_p1, col_p2 = st.columns([1, 1])
        
        with col_p1:
            st.markdown(f"**Intent:** `{active_plan.get('intent', 'N/A')}`")
            confidence = active_plan.get("confidence", 1.0)
            st.progress(float(confidence), text=f"Confidence Score: {int(confidence * 100)}%")
            
            st.markdown("**Structured Operations:**")
            operations = active_plan.get("operations", [])
            for idx, op in enumerate(operations, 1):
                op_type = op.get("type", "operation").upper()
                desc = op.get("description", "")
                st.markdown(f"**{idx}. [{op_type}]** {desc}")

        with col_p2:
            st.markdown("**Synthesized Python Pandas Script:**")
            if gen_code:
                st.code(gen_code, language="python")
            else:
                st.caption("No Python code available for this plan.")

        # ---------------------------------------------------------
        # STEP 4: SUBPROCESS SANDBOX EXECUTION
        # ---------------------------------------------------------
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡ Execute Transformation in Subprocess Sandbox", key="exec_sandbox_btn", type="primary", use_container_width=True):
            st.session_state.execution_status = "RUNNING"
            
            with st.spinner("Executing script in isolated python subprocess sandbox..."):
                exec_success, exec_resp = SheetPilotAPIClient.execute_job(active_plan_id)
                
                if exec_success:
                    job_id = exec_resp.get("job_id")
                    st.session_state.active_job_id = job_id
                    
                    # Poll Status
                    poll_success, status_resp = SheetPilotAPIClient.poll_job_status(job_id)
                    
                    if poll_success:
                        status = status_resp.get("status")
                        if status == "SUCCESS":
                            st.session_state.execution_status = "SUCCESS"
                            st.session_state.execution_time_ms = status_resp.get("execution_time_ms", 0)
                            st.session_state.execution_diff = status_resp.get("diff_summary", {})
                            st.session_state.ast_security_passed = True
                            
                            # Download output result dataframe
                            dl_success, result_bytes, content_type = SheetPilotAPIClient.download_result(job_id)
                            if dl_success and result_bytes:
                                res_df = DataLoader.load_dataframe_from_bytes(result_bytes, "result.xlsx")
                                st.session_state.execution_result_df = res_df
                                st.session_state.result_bytes = result_bytes
                                st.toast("Transformation executed successfully!", icon="🎉")
                            else:
                                st.error("Failed to download output result workbook.")
                        else:
                            st.session_state.execution_status = "FAILED"
                            st.session_state.execution_error = status_resp.get("error_log", "Execution error occurred.")
                            st.session_state.ast_security_passed = False
                    else:
                        st.error(f"Status polling failed: {status_resp.get('error')}")
                else:
                    st.error(f"Job execution trigger failed: {exec_resp.get('error')}")

    # ---------------------------------------------------------
    # STEP 5: EXECUTION RESULTS & WORKBOOK DOWNLOAD
    # ---------------------------------------------------------
    result_df = st.session_state.get("execution_result_df")
    exec_diff = st.session_state.get("execution_diff")
    exec_status = st.session_state.get("execution_status")
    result_bytes = st.session_state.get("result_bytes")

    if exec_status == "SUCCESS" and result_df is not None:
        st.markdown("---")
        st.subheader("4. Transformation Results & Output Download")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        orig_rows = len(raw_df) if raw_df is not None else 0
        new_rows = len(result_df)
        delta_rows = new_rows - orig_rows
        
        col_res1.metric("Original Rows", orig_rows)
        col_res2.metric("Transformed Rows", new_rows, delta=f"{delta_rows} rows")
        col_res3.metric("AST Security Audit", "PASSED ✅")
        
        st.markdown("**Transformed Dataset Output Preview:**")
        st.dataframe(result_df, use_container_width=True)
        
        # Download Result Button
        if result_bytes:
            out_filename = f"SheetPilot_AI_{file_name}" if file_name else "SheetPilot_Result.xlsx"
            st.download_button(
                label=f"📥 Download Transformed Workbook ({out_filename})",
                data=result_bytes,
                file_name=out_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_result_btn",
                type="primary"
            )
    elif exec_status == "FAILED":
        st.markdown("---")
        st.error("❌ **Execution Failed in Sandbox:**")
        st.code(st.session_state.get("execution_error", "Unknown runtime error"), language="text")

if __name__ == "__main__":
    main()
