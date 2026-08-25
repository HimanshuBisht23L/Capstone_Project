import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, JSON, Text
from app.core.database import Base

class ExecutionJob(Base):
    __tablename__ = "execution_jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    plan_id = Column(String(36), nullable=False)
    status = Column(String(30), nullable=False, default="PENDING") # PENDING, PROCESSING, SUCCESS, FAILED
    output_file_key = Column(String(255), nullable=True)
    execution_time_ms = Column(Integer, nullable=True, default=0)
    diff_summary = Column(JSON, nullable=True)
    error_log = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<ExecutionJob id={self.id} status={self.status}>"
