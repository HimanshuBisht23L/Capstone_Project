import os
import uuid
import shutil
from app.core.config import settings

class StorageService:
    @staticmethod
    def save_upload_file(file_bytes: bytes, original_filename: str) -> tuple[str, str]:
        """
        Saves uploaded raw binary bytes to local storage directory with a unique UUID key.
        Returns tuple: (storage_key, absolute_file_path)
        """
        ext = os.path.splitext(original_filename)[1].lower()
        if not ext:
            ext = ".xlsx"
            
        storage_key = f"{uuid.uuid4().hex}{ext}"
        file_path = os.path.join(settings.STORAGE_DIR, storage_key)

        with open(file_path, "wb") as f:
            f.write(file_bytes)

        return storage_key, os.path.abspath(file_path)

    @staticmethod
    def get_file_path(storage_key: str) -> str:
        """
        Returns the absolute file path for a given storage key.
        """
        file_path = os.path.join(settings.STORAGE_DIR, storage_key)
        return os.path.abspath(file_path)

    @staticmethod
    def delete_file(storage_key: str) -> bool:
        """
        Deletes a file from storage if it exists.
        """
        file_path = os.path.join(settings.STORAGE_DIR, storage_key)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
