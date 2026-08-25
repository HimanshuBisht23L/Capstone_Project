import os
import re
import sys
import uuid
import time
import subprocess
import pandas as pd
from typing import Dict, Any, Tuple
from app.core.config import settings
from app.sandbox.ast_checker import verify_code_security

class SandboxRunner:
    @staticmethod
    def execute_in_sandbox(
        python_code: str,
        input_file_path: str,
        output_file_name: str,
        timeout_seconds: int = 10
    ) -> Tuple[bool, str, Dict[str, Any], int, str]:
        """
        Executes AST-verified Python transformation script in an isolated child subprocess.
        Returns Tuple: (success, output_storage_key, diff_summary, execution_time_ms, stdout_log)
        """
        start_time = time.time()
        
        # 1. Perform Static AST Security Verification
        verify_code_security(python_code)

        # Generate unique temporary files (stored in system temp dir to prevent uvicorn reload triggers)
        import tempfile
        exec_id = uuid.uuid4().hex
        temp_script_path = os.path.join(tempfile.gettempdir(), f"sp_script_{exec_id}.py")
        
        ext = os.path.splitext(input_file_path)[1].lower() or ".xlsx"
        output_storage_key = f"transformed_{exec_id}{ext}"
        output_file_path = os.path.join(settings.STORAGE_DIR, output_storage_key)

        # 2. Inject File Paths into Python Script (using forward slashes for cross-platform safety)
        safe_input_path = input_file_path.replace("\\", "/")
        safe_output_path = output_file_path.replace("\\", "/")

        prepared_code = python_code
        prepared_code = re.sub(
            r"input_path\s*=\s*['\"].*?['\"]",
            f"input_path = {repr(safe_input_path)}",
            prepared_code
        )
        prepared_code = re.sub(
            r"output_path\s*=\s*['\"].*?['\"]",
            f"output_path = {repr(safe_output_path)}",
            prepared_code
        )

        # Write script to temporary file
        with open(temp_script_path, "w", encoding="utf-8") as f:
            f.write(prepared_code)

        stdout_log = ""
        try:
            # 3. Execute in Subprocess with Timeout Enforcement
            result = subprocess.run(
                [sys.executable, temp_script_path],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                check=True
            )
            stdout_log = result.stdout
            execution_time_ms = int((time.time() - start_time) * 1000)

            # 4. Calculate Differential Metrics
            diff_summary = SandboxRunner._calculate_diff(input_file_path, output_file_path)

            return True, output_storage_key, diff_summary, execution_time_ms, stdout_log

        except subprocess.TimeoutExpired:
            execution_time_ms = int((time.time() - start_time) * 1000)
            return False, "", {}, execution_time_ms, f"Execution Error: Subprocess timed out after {timeout_seconds} seconds."

        except subprocess.CalledProcessError as cpe:
            execution_time_ms = int((time.time() - start_time) * 1000)
            return False, "", {}, execution_time_ms, f"Execution Error:\n{cpe.stderr or cpe.stdout}"

        finally:
            # Cleanup temporary script file
            if os.path.exists(temp_script_path):
                os.remove(temp_script_path)

    @staticmethod
    def _calculate_diff(original_path: str, transformed_path: str) -> Dict[str, Any]:
        """
        Calculates differential metrics between original and transformed workbooks using smart header detection.
        """
        if not os.path.exists(transformed_path):
            return {"status": "output_file_not_found"}

        try:
            from app.services.spreadsheet_service import SpreadsheetService
            orig_schema = SpreadsheetService.extract_workbook_schema(original_path)
            trans_schema = SpreadsheetService.extract_workbook_schema(transformed_path)

            orig_rows = orig_schema.total_rows
            trans_rows = trans_schema.total_rows

            sheet_names = [s.name for s in trans_schema.sheets]

            return {
                "original_total_rows": orig_rows,
                "modified_total_rows": trans_rows,
                "rows_delta": trans_rows - orig_rows,
                "common_sheets_modified": sheet_names
            }
        except Exception as e:
            return {"diff_error": str(e)}
