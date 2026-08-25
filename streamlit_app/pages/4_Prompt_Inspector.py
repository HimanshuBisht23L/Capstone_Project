import streamlit as st
import ast
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.state_manager import StateManager
from components.custom_css import inject_custom_css
from components.kpi_cards import render_kpi_header
from components.sidebar import render_sidebar

# Static AST Visitor for Security Sandbox Demonstration
BLOCKED_MODULES = {"os", "sys", "subprocess", "shutil", "socket", "requests", "httpx", "importlib", "urllib", "pickle", "ctypes"}
BLOCKED_BUILTINS = {"eval", "exec", "open", "__import__", "globals", "locals", "getattr", "setattr", "delattr", "compile"}

class FrontendSecurityASTVisitor(ast.NodeVisitor):
    def __init__(self):
        self.violations = []

    def visit_Import(self, node):
        for alias in node.names:
            base_module = alias.name.split('.')[0]
            if base_module in BLOCKED_MODULES:
                self.violations.append(f"Security Error: Import of module '{alias.name}' is strictly forbidden.")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        if node.module:
            base_module = node.module.split('.')[0]
            if base_module in BLOCKED_MODULES:
                self.violations.append(f"Security Error: Import from module '{node.module}' is strictly forbidden.")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id in BLOCKED_BUILTINS:
                self.violations.append(f"Security Error: Invocation of builtin function '{node.func.id}()' is strictly forbidden.")
        self.generic_visit(node)

def audit_code_snippet(code_text: str):
    """Parses code text into AST and checks for forbidden module imports or function calls."""
    try:
        tree = ast.parse(code_text)
        visitor = FrontendSecurityASTVisitor()
        visitor.visit(tree)
        return len(visitor.violations) == 0, visitor.violations
    except SyntaxError as e:
        return False, [f"Syntax Error: {str(e)}"]
    except Exception as e:
        return False, [f"AST Parsing Error: {str(e)}"]

def main():
    st.set_page_config(page_title="Prompt Inspector — SheetPilot AI", page_icon="🛡️", layout="wide")
    inject_custom_css()
    StateManager.init_state()
    render_sidebar()

    st.title("🛡️ Prompt Inspector & AST Security Auditor")
    st.caption("Audit natural language prompts, inspect raw JSON action plan payloads, and test static AST security constraints.")
    st.markdown("---")

    render_kpi_header()
    st.markdown("<br>", unsafe_allow_html=True)

    tab_audit, tab_sandbox = st.tabs(["📜 Pipeline Audit Log", "🧪 Interactive AST Security Auditor"])

    with tab_audit:
        st.subheader("Active Pipeline Execution Trace")
        
        prompt = st.session_state.get("current_prompt")
        file_id = st.session_state.get("uploaded_file_id")
        plan_id = st.session_state.get("active_plan_id")
        plan_payload = st.session_state.get("active_plan_payload")
        code = st.session_state.get("generated_code")
        job_id = st.session_state.get("active_job_id")

        if prompt:
            st.markdown(f"**Natural Language Prompt:** *\"{prompt}\"*")
            st.markdown(f"**File ID:** `{file_id}`")
            st.markdown(f"**Plan ID:** `{plan_id}`")
            st.markdown(f"**Job ID:** `{job_id}`")
            
            col_json, col_code = st.columns([1, 1])
            with col_json:
                st.subheader("Raw ActionPlanPayload JSON")
                if plan_payload:
                    st.json(plan_payload)
                else:
                    st.caption("No plan payload in session state.")
                    
            with col_code:
                st.subheader("Synthesized Pandas Python Script")
                if code:
                    st.code(code, language="python")
                    passed, violations = audit_code_snippet(code)
                    if passed:
                        st.success("✅ AST Security Static Visitor: Verification PASSED")
                    else:
                        st.error("❌ AST Security Static Visitor: Violations Detected")
                        for v in violations:
                            st.write(f"• {v}")
                else:
                    st.caption("No generated code in session state.")
        else:
            st.info("No active pipeline execution recorded in this session. Run a prompt in the **Prompt Playground** to inspect audit logs.")

    with tab_sandbox:
        st.subheader("Interactive AST Security Verification Sandbox")
        st.caption("Test Python code snippets below to verify that dangerous imports and calls are blocked statically before execution.")
        
        # Sample malicious snippet templates
        malicious_samples = {
            "Custom Code": "",
            "Malicious OS Exec": "import os\nos.system('dir')",
            "Forbidden Subprocess Call": "import subprocess\nsubprocess.run(['ls', '-la'])",
            "Dangerous Builtin Eval": "user_input = '__import__(\"os\").system(\"calc\")'\neval(user_input)",
            "File System Access": "with open('/etc/passwd', 'r') as f:\n    content = f.read()"
        }
        
        sample_choice = st.selectbox("Load Sample Attack Vector:", options=list(malicious_samples.keys()))
        default_snippet = malicious_samples[sample_choice]
        
        test_snippet = st.text_area("Python Script Snippet for AST Inspection:", value=default_snippet, height=150)
        
        if st.button("🛡️ Run Static AST Visitor Audit", key="run_ast_audit_btn"):
            if not test_snippet.strip():
                st.warning("Please enter Python code to audit.")
            else:
                passed, violations = audit_code_snippet(test_snippet)
                if passed:
                    st.success("✅ **AST SECURITY AUDIT PASSED**: No forbidden modules or builtins detected.")
                else:
                    st.error("❌ **AST SECURITY AUDIT REJECTED**: Security Violation Detected!")
                    for viol in violations:
                        st.markdown(f"• 🚨 **{viol}**")

if __name__ == "__main__":
    main()
