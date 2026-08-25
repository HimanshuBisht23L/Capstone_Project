from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime

class ColumnSchema(BaseModel):
    name: str
    dtype: str
    sample_values: List[Any] = []

class SheetSchema(BaseModel):
    name: str
    row_count: int
    header_row: int = 0
    columns: List[ColumnSchema] = []

class WorkbookSchema(BaseModel):
    total_sheets: int
    total_rows: int
    sheets: List[SheetSchema] = []

class FileUploadResponse(BaseModel):
    file_id: str
    original_name: str
    file_size: int
    schema_info: WorkbookSchema
    created_at: datetime
