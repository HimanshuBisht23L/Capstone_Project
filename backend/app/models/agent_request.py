import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON, Text, Float, Boolean
from app.core.database import Base

class AgentRequest(Base):
    __tablename__ = "agent_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    file_id = Column(String(36), nullable=False)
    user_prompt = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class DBActionPlan(Base):
    __tablename__ = "action_plans"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    request_id = Column(String(36), nullable=False)
    intent = Column(Text, nullable=False)
    operations = Column(JSON, nullable=False)
    confidence = Column(Float, nullable=False, default=0.95)
    requires_clarification = Column(Boolean, default=False)
    clarification_message = Column(Text, nullable=True)
    generated_code = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
