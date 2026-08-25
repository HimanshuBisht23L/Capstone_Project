from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ExecutionTriggerRequest(BaseModel):
    plan_id: str

class ExecutionTriggerResponse(BaseModel):
    job_id: str
    status: str # PENDING, PROCESSING
    message: str

class JobStatusResponse(BaseModel):
    job_id: str
    plan_id: str
    status: str # PENDING, PROCESSING, SUCCESS, FAILED
    execution_time_ms: Optional[int] = 0
    diff_summary: Optional[Dict[str, Any]] = None
    error_log: Optional[str] = None
    created_at: datetime
