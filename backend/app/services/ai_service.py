import json
import re
from typing import Dict, Any
from app.core.config import settings
from app.schemas.plan import ActionPlanPayload, OperationItem

try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

class AIService:
    @staticmethod
    async def generate_action_plan(user_instruction: str, schema_json: Dict[str, Any]) -> ActionPlanPayload:
        """
        Calls Google Gemini API (or rule-based parser fallback) to convert user natural language instruction
        into a structured ActionPlanPayload.
        """
        api_key = settings.GEMINI_API_KEY
        if HAS_GEMINI and api_key and api_key != "your_gemini_api_key_here":
            try:
                return await AIService._call_gemini_api(user_instruction, schema_json, api_key)
            except Exception as e:
                print(f"⚠️ Gemini API call failed: {e}. Falling back to rule-based parser.")

        # Fallback to Rule-Based Natural Language Intent Parser
        return AIService._rule_based_parser(user_instruction, schema_json)

    @staticmethod
    async def _call_gemini_api(user_instruction: str, schema_json: Dict[str, Any], api_key: str) -> ActionPlanPayload:
        genai.configure(api_key=api_key)


        prompt = f"""
You are an expert AI Data Scientist assistant for SheetPilot AI.
Convert the user's natural language instruction into a JSON object matching this schema:
{{
  "intent": "High level intent summary",
  "confidence": 0.95,
  "requires_clarification": false,
  "clarification_message": null,
  "operations": [
    {{
      "type": "search_filter | replace_text | filter | sort | calculate_column | create_sheet | rename_column | delete_column",
      "description": "Human readable description",
      "params": {{
        "column": "column_name (or null)",
        "keyword": "search_keyword",
        "old_value": "target_text_to_find",
        "new_value": "replacement_text",
        "operator": "> | < | == | >=",
        "value": "string value or number",
        "by": "column_name",
        "ascending": true,
        "target_column": "new_column_name",
        "expression": "df['ColumnA'] * 1.1 or df['Salary'].mean()"
      }}
    }}
  ]
}}

CRITICAL INSTRUCTIONS FOR FILTER OPERATIONS:
- If the prompt specifies multiple category values (e.g., Department is IT / Software and Finance), set "operator": "isin" and "value": ["IT / Software", "Finance"].
- If the target column contains a single text string (e.g., Department == 'IT / Software', Status == 'active'), set "operator": "==" and "value": "the string value".
- NEVER use numeric comparison operators (>, <) on text/string columns.


User Workbook Schema JSON:
{json.dumps(schema_json)}

User Natural Language Instruction:
"{user_instruction}"

Respond ONLY with valid raw JSON.
"""
        # Multi-model fallback sequence for API resilience
        last_error = None
        for model_name in ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-flash-latest", "gemini-pro"]:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                text = response.text.strip()
                if text.startswith("```"):
                    text = re.sub(r"^```[a-z]*", "", text, flags=re.MULTILINE)
                    text = text.rstrip("`").strip()

                data = json.loads(text)
                return ActionPlanPayload(**data)
            except Exception as e:
                last_error = e

        raise last_error

    @staticmethod
    def _rule_based_parser(user_instruction: str, schema_json: Dict[str, Any]) -> ActionPlanPayload:
        """
        Deterministic rule-based intent parser fallback when Gemini API key is offline or rate-limited.
        """
        instruction_lower = user_instruction.lower()
        operations = []
        
        # Get first sheet columns if available
        first_sheet_cols = []
        if schema_json and "sheets" in schema_json and len(schema_json["sheets"]) > 0:
            raw_cols = schema_json["sheets"][0].get("columns", [])
            first_sheet_cols = [c["name"] if isinstance(c, dict) else str(c) for c in raw_cols]

        # 0. Text Replacement Detection
        replace_match = re.search(r"(?:change|replace|update)\s+[\"']?([a-zA-Z0-9\s_-]+?)[\"']?\s+(?:with|to)\s+[\"']?([a-zA-Z0-9\s_-]+?)[\"']?(?:,|\s+and|\s+then|\s+filter|\s+where|\s+calculate|\s+sort|$)", user_instruction, re.IGNORECASE)
        if replace_match:
            old_val = replace_match.group(1).strip()
            new_val = replace_match.group(2).strip()
            rep_col = None
            for col in first_sheet_cols:
                if col.lower() in instruction_lower:
                    rep_col = col
                    break
            operations.append(OperationItem(
                type="replace_text",
                description=f"Replace '{old_val}' with '{new_val}'",
                params={"column": rep_col, "old_value": old_val, "new_value": new_val}
            ))

        # 1. Status & Categorical Field Equality Filters (Multiple Clauses Support)
        # Split instruction into clauses to handle multiple filters cleanly
        clauses = re.split(r",|\s+and\s+|\s+then\s+", user_instruction, flags=re.IGNORECASE)
        for clause in clauses:
            clause_str = clause.strip()
            # Match "where <Field> is <Value>" or "<Field> is <Value>"
            status_match = re.search(r"(?:where\s+)?([a-zA-Z0-9\s/_-]+?)\s+(?:is|are|==|=)\s+[\"']?([a-zA-Z0-9\s/()_-]+?)[\"']?$", clause_str, re.IGNORECASE)

            if status_match:
                raw_field = status_match.group(1).strip()
                val_str = status_match.group(2).strip()
                
                # Skip if value is a numeric comparison phrase (use word boundaries so 'overdue' isn't matched by 'over')
                if re.search(r"\b(greater|less|above|below|exceeding|exceeds|over|under|more)\b", val_str, re.IGNORECASE):
                    continue


                target_status_col = None
                for col in first_sheet_cols:
                    if col.lower() == raw_field.lower() or col.lower() in raw_field.lower() or raw_field.lower() in col.lower():
                        target_status_col = col
                        break

                if target_status_col and not any(op.params and op.params.get("column") == target_status_col for op in operations):
                    # Split on " or " or " and " (do NOT split on "/")
                    if " or " in val_str.lower() or " and " in val_str.lower():
                        sub_vals = [v.strip() for v in re.split(r"\s+or\s+|\s+and\s+", val_str, flags=re.IGNORECASE) if v.strip()]
                        if len(sub_vals) > 1:
                            operations.append(OperationItem(
                                type="filter",
                                description=f"Filter rows where {target_status_col} in {sub_vals}",
                                params={"column": target_status_col, "operator": "isin", "value": sub_vals}
                            ))
                        else:
                            operations.append(OperationItem(
                                type="filter",
                                description=f"Filter rows where {target_status_col} == '{val_str}'",
                                params={"column": target_status_col, "operator": "==", "value": val_str}
                            ))
                    else:
                        operations.append(OperationItem(
                            type="filter",
                            description=f"Filter rows where {target_status_col} == '{val_str}'",
                            params={"column": target_status_col, "operator": "==", "value": val_str}
                        ))


        # Multi-Category Department Filtering
        dept_keywords = ["IT / Software", "Finance", "Sales", "Human Resources", "Marketing", "Customer Support", "Operations", "Production", "Legal"]
        found_depts = [d for d in dept_keywords if d.lower() in instruction_lower]

        if len(found_depts) > 1 and not any(op.params and op.params.get("column") == "Department" for op in operations):
            operations.append(OperationItem(
                type="filter",
                description=f"Filter rows where Department in {found_depts}",
                params={"column": "Department", "operator": "isin", "value": found_depts}
            ))
        elif len(found_depts) == 1 and not any(op.params and op.params.get("column") == "Department" for op in operations):
            operations.append(OperationItem(
                type="filter",
                description=f"Filter rows where Department == '{found_depts[0]}'",
                params={"column": "Department", "operator": "==", "value": found_depts[0]}
            ))

        # Dynamic Numeric Filter Detection (Extract column immediately preceding comparison keyword)
        num_match = re.search(r"([a-zA-Z0-9\s_()%.-]+?)\s+(?:is|are|==|=)?\s*(?:>|<|>=|<=|greater than|less than|above|exceeding|exceeds|is over|over)\s*(\d+(?:,\d+)*(?:\.\d+)?)", user_instruction, re.IGNORECASE)
        if num_match:
            raw_num_col = num_match.group(1).strip()
            # Extract last word/phrase after 'and', 'or', 'where', or ','
            raw_num_col = re.split(r"\s+and\s+|\s+or\s+|,|\s+where\s+", raw_num_col, flags=re.IGNORECASE)[-1].strip()
            val = float(num_match.group(2).replace(',', ''))
            op_sym = ">" if any(k in instruction_lower for k in [">", "greater", "above", "exceeding", "exceeds", "over"]) else ("<" if any(k in instruction_lower for k in ["<", "less", "below", "under"]) else "==")
            
            filter_num_col = None
            for col in first_sheet_cols:
                if col.lower() == raw_num_col.lower() or col.lower() in raw_num_col.lower() or raw_num_col.lower() in col.lower():
                    filter_num_col = col
                    break
            
            if not filter_num_col:
                for col in first_sheet_cols:
                    if col.lower() in instruction_lower:
                        filter_num_col = col
                        break

            if filter_num_col and not any(op.params and op.params.get("column") == filter_num_col and op.params.get("operator") == op_sym for op in operations):
                operations.append(OperationItem(
                    type="filter",
                    description=f"Filter rows where {filter_num_col} {op_sym} {val}",
                    params={"column": filter_num_col, "operator": op_sym, "value": val}
                ))




        # 2. Calculation Column Creation
        if ("net_pay" in instruction_lower or "net pay" in instruction_lower) and not "net_payment_made" in instruction_lower:
            sal_present = [c for c in first_sheet_cols if "sal" in c.lower()]
            if sal_present:
                base_col = "Base Salary" if "Base Salary" in first_sheet_cols else sal_present[0]
                hra_col = "HRA Allowance" if "HRA Allowance" in first_sheet_cols else (first_sheet_cols[1] if len(first_sheet_cols) > 1 else base_col)
                tds_col = "TDS Tax (10%)" if "TDS Tax (10%)" in first_sheet_cols else (first_sheet_cols[2] if len(first_sheet_cols) > 2 else base_col)
                operations.append(OperationItem(
                    type="calculate_column",
                    description="Calculate Net_Pay (Base Salary + HRA Allowance - TDS Tax)",
                    params={"target_column": "Net_Pay", "expression": f"df['{base_col}'] + df['{hra_col}'] - df['{tds_col}']"}
                ))

        if "net_payment_made" in instruction_lower:
            gross_col = "Gross Payment" if "Gross Payment" in first_sheet_cols else (first_sheet_cols[0] if first_sheet_cols else "Gross")
            tds_ded_col = "TDS Deducted" if "TDS Deducted" in first_sheet_cols else (first_sheet_cols[1] if len(first_sheet_cols) > 1 else gross_col)
            operations.append(OperationItem(
                type="calculate_column",
                description="Calculate Net_Payment_Made (Gross Payment - TDS Deducted)",
                params={"target_column": "Net_Payment_Made", "expression": f"df['{gross_col}'] - df['{tds_ded_col}']"}
            ))

        if ("hra_bonus" in instruction_lower or "bonus" in instruction_lower) and any("sal" in c.lower() for c in first_sheet_cols):
            pct_match = re.search(r'(\d+)%', user_instruction)
            pct = float(pct_match.group(1)) / 100.0 if pct_match else 0.10
            sal_col = "Base Salary" if "Base Salary" in first_sheet_cols else [c for c in first_sheet_cols if "sal" in c.lower()][0]
            target_bonus_col = "HRA_Bonus" if "hra" in instruction_lower else "Bonus_Amount"
            operations.append(OperationItem(
                type="calculate_column",
                description=f"Calculate {int(pct*100)}% {target_bonus_col} on {sal_col}",
                params={"target_column": target_bonus_col, "expression": f"df['{sal_col}'] * {pct}"}
            ))

        # General Percentage Column Calculation (e.g., "calculate 18% GST_Expense on Amount")
        pct_calc_match = re.search(r"(\d+(?:\.\d+)?)%\s+([a-zA-Z0-9_-]+)\s+on\s+([a-zA-Z0-9\s_()%.-]+)", user_instruction, re.IGNORECASE)
        if pct_calc_match:
            pct_val = float(pct_calc_match.group(1)) / 100.0
            target_col = pct_calc_match.group(2).strip()
            source_raw = pct_calc_match.group(3).strip()
            source_raw = re.split(r"\s+and\s+|\s+or\s+|,|\s+then\s+|\s+calculate\s+|\s+sort\s+|\s+in\s+", source_raw, flags=re.IGNORECASE)[0].strip()
            
            source_col = None
            for col in first_sheet_cols:
                if col.lower() == source_raw.lower() or col.lower() in source_raw.lower() or source_raw.lower() in col.lower():
                    source_col = col
                    break
            
            if not source_col:
                num_candidates = [c for c in first_sheet_cols if any(k in c.lower() for k in ["amount", "salary", "val", "price", "revenue", "payment"])]
                if num_candidates:
                    source_col = num_candidates[0]
            
            if source_col and not any(op.params and op.params.get("target_column") == target_col for op in operations):
                operations.append(OperationItem(
                    type="calculate_column",
                    description=f"Calculate {pct_calc_match.group(1)}% {target_col} on {source_col}",
                    params={"target_column": target_col, "expression": f"df['{source_col}'] * {pct_val}"}
                ))

            
        # Natural Language Addition Calculations (e.g., "Calculate H2_Revenue adding Q3 Revenue and Q4 Revenue")
        add_matches = re.finditer(r"calculate\s+([a-zA-Z0-9_-]+?)\s+(?:by\s+)?adding\s+([a-zA-Z0-9\s_()%.-]+)", user_instruction, re.IGNORECASE)
        for m in add_matches:
            target_col = m.group(1).strip()
            col_phrase = m.group(2).strip()
            col_phrase = re.split(r",|\s+and\s+sort|\s+then|\s+calculate", col_phrase, flags=re.IGNORECASE)[0].strip()
            
            matched_cols = []
            for col in first_sheet_cols:
                if col.lower() in col_phrase.lower():
                    matched_cols.append(col)
            
            if matched_cols:
                expr = " + ".join([f"df['{c}']" for c in matched_cols])
                if not any(op.params and op.params.get("target_column") == target_col for op in operations):
                    operations.append(OperationItem(
                        type="calculate_column",
                        description=f"Calculate {target_col} adding {' + '.join(matched_cols)}",
                        params={"target_column": target_col, "expression": expr}
                    ))

        # Natural Language Subtraction Calculations (e.g., "calculate Net_Operating_Income subtracting COGS Expenses and Operating Overhead from Gross Revenue")
        sub_match = re.search(r"calculate\s+([a-zA-Z0-9_-]+?)\s+(?:by\s+)?subtracting\s+([a-zA-Z0-9\s_()%.-]+?)\s+from\s+([a-zA-Z0-9\s_()%.-]+)", user_instruction, re.IGNORECASE)
        if sub_match:
            target_col = sub_match.group(1).strip()
            sub_from_raw = sub_match.group(2).strip()
            base_raw = sub_match.group(3).strip()
            base_raw = re.split(r",|\s+and\s+sort|\s+then|\s+calculate", base_raw, flags=re.IGNORECASE)[0].strip()
            
            sub_cols = []
            base_col = None
            for col in first_sheet_cols:
                if col.lower() in sub_from_raw.lower():
                    sub_cols.append(col)
                if col.lower() in base_raw.lower():
                    base_col = col
                
            if sub_cols and base_col:
                sub_expr = " - ".join([f"df['{c}']" for c in sub_cols])
                expr = f"df['{base_col}'] - {sub_expr}"
                if not any(op.params and op.params.get("target_column") == target_col for op in operations):
                    operations.append(OperationItem(
                        type="calculate_column",
                        description=f"Calculate {target_col} ({base_col} - {' - '.join(sub_cols)})",
                        params={"target_column": target_col, "expression": expr}
                    ))






        if "total_gst" in instruction_lower or ("cgst" in instruction_lower and "sgst" in instruction_lower):
            operations.append(OperationItem(
                type="calculate_column",
                description="Calculate Total_GST (CGST + SGST)",
                params={"target_column": "Total_GST", "expression": "df['CGST (9%)'] + df['SGST (9%)']"}
            ))

        if any(k in instruction_lower for k in ["average", "avg", "mean"]):
            target_avg_col = None
            avg_match = re.search(r"calculate\s+([a-zA-Z0-9_-]+)\s+(?:for|on)", user_instruction, re.IGNORECASE)
            if avg_match:
                target_avg_col = avg_match.group(1).strip()
            
            calc_col = None
            # Check previously created numeric target columns first
            created_targets = [op.params.get("target_column") for op in operations if op.type == "calculate_column" and op.params and op.params.get("target_column")]
            if created_targets:
                calc_col = created_targets[-1]
            
            # If not found, look for numeric columns in schema
            if not calc_col:
                for col in first_sheet_cols:
                    if any(k in col.lower() for k in ["sal", "amount", "revenue", "value", "payment", "price", "score", "tds", "deduct", "gross", "rate"]):
                        calc_col = col
                        break
            
            # Exclude known non-numeric text columns
            text_kw = ["stream", "department", "name", "status", "category", "code", "id", "location", "state", "result", "type", "method"]
            if calc_col and any(k in calc_col.lower() for k in text_kw) and not calc_col in created_targets:
                num_cols = [c for c in first_sheet_cols if any(k in c.lower() for k in ["sal", "amount", "revenue", "value", "payment", "price", "score", "tds", "deduct", "gross", "rate"])]
                if num_cols:
                    calc_col = num_cols[0]

            calc_col = calc_col or "Value"
            final_target = target_avg_col or f"Average_{calc_col}"
            
            if not any(op.params and op.params.get("target_column") == final_target for op in operations):
                operations.append(OperationItem(
                    type="calculate_column",
                    description=f"Calculate {final_target} for filtered rows",
                    params={"target_column": final_target, "expression": f"df['{calc_col}'].mean()"}
                ))




        # Natural Language Multiplication Calculations (e.g., "Calculate Total_Inventory_Value multiplying Unit Price by Quantity in Stock")
        mult_match = re.search(r"calculate\s+([a-zA-Z0-9_-]+?)\s+(?:by\s+)?multiply(?:ing)?\s+([a-zA-Z0-9\s_()%.-]+?)\s+by\s+([a-zA-Z0-9\s_()%.-]+)", user_instruction, re.IGNORECASE)
        if mult_match:
            target_col = mult_match.group(1).strip()
            col1_raw = mult_match.group(2).strip()
            col2_raw = mult_match.group(3).strip()
            col2_raw = re.split(r",|\s+and\s+sort|\s+then|\s+calculate|\s+filter", col2_raw, flags=re.IGNORECASE)[0].strip()
            
            c1, c2 = None, None
            for col in first_sheet_cols:
                if col.lower() in col1_raw.lower(): c1 = col
                if col.lower() in col2_raw.lower(): c2 = col
                
            if c1 and c2:
                if not any(op.params and op.params.get("target_column") == target_col for op in operations):
                    operations.append(OperationItem(
                        type="calculate_column",
                        description=f"Calculate {target_col} ({c1} * {c2})",
                        params={"target_column": target_col, "expression": f"df['{c1}'] * df['{c2}']"}
                    ))

        # Natural Language Division Calculations (e.g., "calculate Outstanding_Ratio dividing Balance Due by Billed Amount")
        div_match = re.search(r"calculate\s+([a-zA-Z0-9_-]+?)\s+(?:by\s+)?divid(?:ing)?\s+([a-zA-Z0-9\s_()%.-]+?)\s+by\s+([a-zA-Z0-9\s_()%.-]+)", user_instruction, re.IGNORECASE)
        if div_match:
            target_col = div_match.group(1).strip()
            col1_raw = div_match.group(2).strip()
            col2_raw = div_match.group(3).strip()
            col2_raw = re.split(r",|\s+and\s+sort|\s+then|\s+calculate|\s+filter", col2_raw, flags=re.IGNORECASE)[0].strip()
            
            c1, c2 = None, None
            for col in first_sheet_cols:
                if col.lower() in col1_raw.lower(): c1 = col
                if col.lower() in col2_raw.lower(): c2 = col
                
            if c1 and c2:
                if not any(op.params and op.params.get("target_column") == target_col for op in operations):
                    operations.append(OperationItem(
                        type="calculate_column",
                        description=f"Calculate {target_col} ({c1} / {c2})",
                        params={"target_column": target_col, "expression": f"df['{c1}'] / df['{c2}']"}
                    ))

        # 3. Explicit Sort Detection with Column Extraction
        if "sort" in instruction_lower or "order" in instruction_lower:
            asc = False if ("descending" in instruction_lower or "desc" in instruction_lower) else True
            sort_col = None
            
            calculated_target_cols = [op.params.get("target_column") for op in operations if op.type == "calculate_column" and op.params and op.params.get("target_column")]
            all_sortable = list(first_sheet_cols) + calculated_target_cols

            # Extract column after "sort by" or "order by"
            sort_by_match = re.search(r"(?:sort|order)(?:\s+the\s+table)?\s+by\s+([a-zA-Z0-9\s_()%.-]+?)(?:\s+in|\s+ascending|\s+descending|\s+desc|\s+asc|$)", user_instruction, re.IGNORECASE)
            if sort_by_match:
                raw_sort_txt = sort_by_match.group(1).strip().lower()
                for col in all_sortable:
                    if col.lower() in raw_sort_txt or raw_sort_txt in col.lower():
                        sort_col = col
                        break
            
            if not sort_col:
                for col in all_sortable:
                    if col.lower() in instruction_lower:
                        sort_col = col

            sort_col = sort_col or (first_sheet_cols[0] if first_sheet_cols else "Sheet1")
            operations.append(OperationItem(
                type="sort",
                description=f"Sort table by {sort_col} ({'ascending' if asc else 'descending'})",
                params={"by": sort_col, "ascending": asc}
            ))


        if not operations:
            return ActionPlanPayload(
                intent=f"Ambiguous or unsupported instruction: '{user_instruction}'",
                operations=[],
                confidence=0.0,
                requires_clarification=True,
                clarification_message="Unable to interpret instruction safely. Please specify column names and action intent (e.g. Filter, Calculate, Sort)."
            )

        return ActionPlanPayload(
            intent=f"Executed natural language instruction: '{user_instruction}'",
            operations=operations,
            confidence=0.95
        )




