import os
import pandas as pd
from typing import Dict, Any, List
from app.schemas.file import WorkbookSchema, SheetSchema, ColumnSchema

class SpreadsheetService:
    @staticmethod
    def extract_workbook_schema(file_path: str) -> WorkbookSchema:
        """
        Parses an Excel (.xlsx, .xls) or CSV (.csv) file using Pandas and extracts sheet metadata,
        row counts, column data types, and non-null sample values.
        """
        ext = os.path.splitext(file_path)[1].lower()
        sheets_data: List[SheetSchema] = []
        total_rows = 0

        if ext == ".csv":
            header_row = SpreadsheetService._detect_header_row(file_path, ext=".csv")
            df = pd.read_csv(file_path, header=header_row)
            columns_schema = SpreadsheetService._extract_column_schemas(df)
            row_count = len(df)
            total_rows += row_count

            sheets_data.append(SheetSchema(
                name="Sheet1",
                row_count=row_count,
                header_row=header_row,
                columns=columns_schema
            ))
        else:
            # Excel file (.xlsx, .xls)
            excel_file = pd.ExcelFile(file_path)
            for sheet_name in excel_file.sheet_names:
                header_row = SpreadsheetService._detect_header_row(excel_file, sheet_name=sheet_name, ext=".xlsx")
                df = pd.read_excel(excel_file, sheet_name=sheet_name, header=header_row)
                columns_schema = SpreadsheetService._extract_column_schemas(df)
                row_count = len(df)
                total_rows += row_count

                sheets_data.append(SheetSchema(
                    name=sheet_name,
                    row_count=row_count,
                    header_row=header_row,
                    columns=columns_schema
                ))

        return WorkbookSchema(
            total_sheets=len(sheets_data),
            total_rows=total_rows,
            sheets=sheets_data
        )

    @staticmethod
    def _detect_header_row(file_or_excel, sheet_name=None, ext=".xlsx") -> int:
        """
        Scans first 10 rows of raw headerless sheet data to locate the true table header row
        by detecting the row with maximum non-null named label cells.
        """
        try:
            if ext == ".csv":
                df_raw = pd.read_csv(file_or_excel, header=None, nrows=10)
            else:
                df_raw = pd.read_excel(file_or_excel, sheet_name=sheet_name, header=None, nrows=10)
            
            best_row = 0
            max_non_null_count = -1
            
            for r_idx in range(min(10, len(df_raw))):
                row_series = df_raw.iloc[r_idx].dropna()
                valid_count = sum(1 for val in row_series if str(val).strip() != "")
                if valid_count > max_non_null_count:
                    max_non_null_count = valid_count
                    best_row = r_idx
            return best_row
        except Exception:
            return 0

    @staticmethod
    def _extract_column_schemas(df: pd.DataFrame) -> List[ColumnSchema]:
        columns_schema: List[ColumnSchema] = []
        for col_name in df.columns:
            dtype_str = str(df[col_name].dtype)
            
            # Extract sample values (up to 5 non-null values)
            non_null_samples = df[col_name].dropna().head(5).tolist()
            # Convert non-serializable types to python native types
            clean_samples = [
                str(val) if not isinstance(val, (int, float, bool, str)) else val
                for val in non_null_samples
            ]

            columns_schema.append(ColumnSchema(
                name=str(col_name),
                dtype=dtype_str,
                sample_values=clean_samples
            ))
        return columns_schema
