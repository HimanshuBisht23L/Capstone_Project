import os
import io
import pandas as pd
from typing import Optional, List, Tuple

BENCHMARK_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "docs", "test_datasets")

class DataLoader:
    """
    Data Loader utility for parsing Excel/CSV bytes and accessing local benchmark datasets.
    """
    
    @staticmethod
    def load_dataframe_from_bytes(file_bytes: bytes, filename: str) -> Optional[pd.DataFrame]:
        """Converts Excel or CSV bytes stream into a Pandas DataFrame."""
        try:
            buffer = io.BytesIO(file_bytes)
            if filename.endswith(".csv"):
                return pd.read_csv(buffer)
            elif filename.endswith((".xlsx", ".xls")):
                return pd.read_excel(buffer, sheet_name=0)
            return None
        except Exception as e:
            print(f"Error parsing file bytes: {e}")
            return None

    @staticmethod
    def get_benchmark_datasets() -> List[str]:
        """Returns sorted list of available benchmark datasets in docs/test_datasets/."""
        if not os.path.exists(BENCHMARK_DIR):
            return []
        files = [f for f in os.listdir(BENCHMARK_DIR) if f.endswith((".xlsx", ".csv"))]
        return sorted(files)

    @staticmethod
    def load_benchmark_dataset(filename: str) -> Tuple[Optional[bytes], Optional[pd.DataFrame]]:
        """Loads raw bytes and DataFrame preview for a named benchmark dataset."""
        file_path = os.path.join(BENCHMARK_DIR, filename)
        if not os.path.exists(file_path):
            return None, None
        
        try:
            with open(file_path, "rb") as f:
                raw_bytes = f.read()
            df = DataLoader.load_dataframe_from_bytes(raw_bytes, filename)
            return raw_bytes, df
        except Exception as e:
            print(f"Error loading benchmark dataset {filename}: {e}")
            return None, None
