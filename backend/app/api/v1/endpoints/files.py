from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.file import File as DBFile
from app.schemas.file import FileUploadResponse
from app.services.storage_service import StorageService
from app.services.spreadsheet_service import SpreadsheetService

router = APIRouter()

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    Accepts an Excel (.xlsx, .xls) or CSV (.csv) workbook upload up to 50MB.
    Saves file to disk, extracts schema using Pandas, and persists DB record.
    """
    allowed_exts = [".xlsx", ".xls", ".csv"]
    filename = file.filename or "workbook.xlsx"
    ext = filename[filename.rfind("."):].lower() if "." in filename else ""

    if ext not in allowed_exts:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file extension '{ext}'. Allowed extensions: .xlsx, .xls, .csv"
        )

    # Read binary bytes
    file_bytes = await file.read()
    file_size = len(file_bytes)

    if file_size > 50 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds maximum limit of 50MB.")

    # 1. Save binary file to disk
    storage_key, absolute_path = StorageService.save_upload_file(file_bytes, filename)

    try:
        # 2. Extract Schema Metadata using Pandas
        schema_info = SpreadsheetService.extract_workbook_schema(absolute_path)

        # 3. Create DB File ORM Record
        db_file = DBFile(
            original_name=filename,
            storage_key=storage_key,
            mime_type=file.content_type or "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            file_size=file_size,
            schema_json=schema_info.model_dump()
        )
        db.add(db_file)
        await db.commit()
        await db.refresh(db_file)

        return FileUploadResponse(
            file_id=db_file.id,
            original_name=db_file.original_name,
            file_size=db_file.file_size,
            schema_info=schema_info,
            created_at=db_file.created_at
        )

    except Exception as e:
        StorageService.delete_file(storage_key)
        raise HTTPException(status_code=500, detail=f"Spreadsheet processing failure: {str(e)}")
