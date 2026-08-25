from typing import Dict, Any, List
from app.schemas.plan import ActionPlanPayload

class SecurityService:
    @staticmethod
    def validate_action_plan_against_schema(plan: ActionPlanPayload, schema_json: Dict[str, Any]) -> ActionPlanPayload:
        """
        Validates that all column names referenced in the AI Action Plan actually exist
        in the workbook schema and normalizes column casing & type safety before code synthesis.
        """
        if not schema_json or "sheets" not in schema_json:
            return plan

        # Extract map of lower_case_name -> exact_case_name and lower_case_name -> dtype
        column_case_map = {}
        column_dtypes = {}

        for sheet in schema_json.get("sheets", []):
            raw_cols = sheet.get("columns", [])
            raw_dtypes = sheet.get("dtypes", {})

            for col in raw_cols:
                col_name = col["name"] if isinstance(col, dict) else str(col)
                column_case_map[col_name.lower()] = col_name
                if isinstance(col, dict) and "dtype" in col:
                    column_dtypes[col_name.lower()] = str(col["dtype"]).lower()
            
            if isinstance(raw_dtypes, dict):
                for k, v in raw_dtypes.items():
                    column_dtypes[k.lower()] = str(v).lower()

        invalid_referenced_columns = []
        created_columns = set()

        for op in plan.operations:
            params = op.params or {}
            if op.type == "search_filter" or "keyword" in params:
                continue

            target_col = params.get("target_column")
            if target_col and isinstance(target_col, str):
                created_columns.add(target_col.lower())

            # Validate input reference columns

            for key in ["column", "by"]:
                col_target = params.get(key)
                if col_target and isinstance(col_target, str):
                    lower_col = col_target.lower()
                    if lower_col.startswith("temp_") or lower_col in created_columns:
                        continue
                    elif lower_col in column_case_map:
                        # Auto-correct column casing to match exact workbook header
                        params[key] = column_case_map[lower_col]
                    else:
                        invalid_referenced_columns.append(col_target)

            # Validate calculation expression referenced columns (e.g. df['Q3 Revenue'] + df['Q4 Revenue'])
            expr = params.get("expression")
            if expr and isinstance(expr, str):
                import re
                referenced_in_expr = re.findall(r"df\['([^']+)'\]", expr)
                for ref_col in referenced_in_expr:
                    lower_ref = ref_col.lower()
                    if lower_ref.startswith("temp_") or lower_ref in created_columns:
                        continue
                    elif lower_ref in column_case_map:
                        exact_name = column_case_map[lower_ref]
                        if ref_col != exact_name:
                            params["expression"] = params["expression"].replace(f"df['{ref_col}']", f"df['{exact_name}']")
                    else:
                        invalid_referenced_columns.append(ref_col)


        if invalid_referenced_columns:
            plan.requires_clarification = True
            plan.clarification_message = f"Referenced column(s) {invalid_referenced_columns} do not exist in the uploaded workbook."
            plan.confidence = 0.0
        elif not plan.requires_clarification:
            plan.requires_clarification = False
            plan.clarification_message = None
            plan.confidence = 0.95


        return plan


