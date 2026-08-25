import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, JSON
from app.core.database import Base

class File(Base):
    __tablename__ = "files"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    original_name = Column(String(255), nullable=False)
    storage_key = Column(String(255), nullable=False, unique=True)
    mime_type = Column(String(100), nullable=True)
    file_size = Column(Integer, nullable=False, default=0)
    schema_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<File id={self.id} original_name={self.original_name}>"
