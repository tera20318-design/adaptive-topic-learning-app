from __future__ import annotations

import csv
from pathlib import Path


def validate_claim_ledger_rows(rows: list[dict], schema_path: Path) -> list[str]:
    return _validate_rows(rows, schema_path)


def validate_citation_ledger_rows(rows: list[dict], schema_path: Path) -> list[str]:
    return _validate_rows(rows, schema_path)


def _validate_rows(rows: list[dict], schema_path: Path) -> list[str]:
    with schema_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        schema_rows = list(reader)

    errors: list[str] = []
    required_columns = [item["column_name"] for item in schema_rows if item["required"] == "true"]

    for index, row in enumerate(rows):
        for column in required_columns:
            if column not in row:
                errors.append(f"row {index}: missing column `{column}`")

        for schema_row in schema_rows:
            column = schema_row["column_name"]
            if column not in row:
                continue
            errors.extend(_validate_value(index, column, row[column], schema_row))

    return errors


def _validate_value(index: int, column: str, value, schema_row: dict) -> list[str]:
    errors: list[str] = []
    declared_type = schema_row["type"]
    allowed_values = [item for item in schema_row["allowed_values"].split("|") if item]

    if declared_type == "string" and not isinstance(value, str):
        errors.append(f"row {index}: `{column}` should be string")
    elif declared_type == "integer" and not isinstance(value, int):
        errors.append(f"row {index}: `{column}` should be integer")
    elif declared_type == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            errors.append(f"row {index}: `{column}` should be number")
    elif declared_type == "boolean" and not isinstance(value, bool):
        errors.append(f"row {index}: `{column}` should be boolean")
    elif declared_type.startswith("list[") and not isinstance(value, list):
        errors.append(f"row {index}: `{column}` should be list")
    elif declared_type == "enum" and value not in allowed_values:
        errors.append(f"row {index}: `{column}` has unexpected value `{value}`")

    if declared_type.startswith("list[enum]") and isinstance(value, list):
        invalid = [item for item in value if item not in allowed_values]
        if invalid:
            errors.append(f"row {index}: `{column}` contains unexpected values {invalid}")

    return errors
