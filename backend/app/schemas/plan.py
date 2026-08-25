from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class PlanRequest(BaseModel):
    file_id: str
    user_prompt: str

class OperationItem(BaseModel):
    type: str # filter, sort, calculate_column, create_sheet
    description: str
    params: Dict[str, Any] = {}

class ActionPlanPayload(BaseModel):
    intent: str
    operations: List[OperationItem] = []
    confidence: float = 0.95
    requires_clarification: bool = False
    clarification_message: Optional[str] = None

class AgentPlanResponse(BaseModel):
    plan_id: str
    request_id: str
    plan: ActionPlanPayload
    generated_code: str
