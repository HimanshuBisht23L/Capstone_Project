import requests
import os
from typing import Dict, Any, Tuple, Optional

class SheetPilotAPIClient:
    """
    Centralized HTTP API Client for SheetPilot AI FastAPI Gateway.
    All Streamlit communication with the backend is routed through this client.
    """
    
    @staticmethod
    def get_base_url() -> str:
        """Retrieves backend API base URL from environment configuration with fallback."""
        return os.getenv("SHEETPILOT_BACKEND_URL") or os.getenv("BACKEND_URL") or "http://localhost:8000"

    @staticmethod
    def check_health(timeout: int = 3) -> Tuple[bool, Dict[str, Any]]:
        """Queries /health endpoint to check system operational status."""
        base_url = SheetPilotAPIClient.get_base_url()
        try:
            resp = requests.get(f"{base_url}/health", timeout=timeout)
            if resp.status_code == 200:
                return True, resp.json()
            return False, {"error": f"HTTP Error {resp.status_code}: {resp.text}"}
        except requests.exceptions.Timeout:
            return False, {"error": "Backend connection timed out."}
        except requests.exceptions.ConnectionError:
            return False, {"error": f"Could not connect to FastAPI server at {base_url}."}
        except Exception as e:
            return False, {"error": f"Health check failure: {str(e)}"}

    @staticmethod
    def upload_file(file_bytes: bytes, filename: str, timeout: int = 30) -> Tuple[bool, Dict[str, Any]]:
        """Sends Excel/CSV file bytes to /api/v1/files/upload endpoint."""
        base_url = SheetPilotAPIClient.get_base_url()
        try:
            files = {"file": (filename, file_bytes, "application/octet-stream")}
            resp = requests.post(f"{base_url}/api/v1/files/upload", files=files, timeout=timeout)
            if resp.status_code == 200:
                return True, resp.json()
            detail = resp.json().get("detail", resp.text) if resp.headers.get("content-type") == "application/json" else resp.text
            return False, {"error": detail}
        except Exception as e:
            return False, {"error": f"File upload request failed: {str(e)}"}

    @staticmethod
    def generate_plan(file_id: str, prompt: str, timeout: int = 30) -> Tuple[bool, Dict[str, Any]]:
        """Sends file_id and user prompt to /api/v1/agent/plan endpoint."""
        base_url = SheetPilotAPIClient.get_base_url()
        try:
            payload = {"file_id": file_id, "user_prompt": prompt}
            resp = requests.post(f"{base_url}/api/v1/agent/plan", json=payload, timeout=timeout)
            if resp.status_code == 200:
                return True, resp.json()
            detail = resp.json().get("detail", resp.text) if "application/json" in resp.headers.get("content-type", "") else resp.text
            return False, {"error": detail}
        except Exception as e:
            return False, {"error": f"Plan generation request failed: {str(e)}"}

    @staticmethod
    def execute_job(plan_id: str, timeout: int = 10) -> Tuple[bool, Dict[str, Any]]:
        """Triggers sandbox execution via /api/v1/jobs/execute endpoint."""
        base_url = SheetPilotAPIClient.get_base_url()
        try:
            payload = {"plan_id": plan_id}
            resp = requests.post(f"{base_url}/api/v1/jobs/execute", json=payload, timeout=timeout)
            if resp.status_code == 200:
                return True, resp.json()
            detail = resp.json().get("detail", resp.text) if "application/json" in resp.headers.get("content-type", "") else resp.text
            return False, {"error": detail}
        except Exception as e:
            return False, {"error": f"Execution trigger failed: {str(e)}"}

    @staticmethod
    def poll_job_status(job_id: str, timeout: int = 5) -> Tuple[bool, Dict[str, Any]]:
        """Polls /api/v1/jobs/{job_id} for execution metrics, status, and error logs."""
        base_url = SheetPilotAPIClient.get_base_url()
        try:
            resp = requests.get(f"{base_url}/api/v1/jobs/{job_id}", timeout=timeout)
            if resp.status_code == 200:
                return True, resp.json()
            detail = resp.json().get("detail", resp.text) if "application/json" in resp.headers.get("content-type", "") else resp.text
            return False, {"error": detail}
        except Exception as e:
            return False, {"error": f"Job status polling failed: {str(e)}"}

    @staticmethod
    def download_result(job_id: str, timeout: int = 15) -> Tuple[bool, Optional[bytes], str]:
        """Downloads transformed workbook from /api/v1/jobs/results/{job_id}/download endpoint."""
        base_url = SheetPilotAPIClient.get_base_url()
        try:
            resp = requests.get(f"{base_url}/api/v1/jobs/results/{job_id}/download", timeout=timeout)
            if resp.status_code == 200:
                media_type = resp.headers.get("content-type", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                return True, resp.content, media_type
            return False, None, resp.text
        except Exception as e:
            return False, None, str(e)
