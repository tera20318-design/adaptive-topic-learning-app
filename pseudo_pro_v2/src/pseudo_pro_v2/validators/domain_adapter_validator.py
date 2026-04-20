from __future__ import annotations

from pathlib import Path

from pseudo_pro_v2.utils import load_json


def validate_domain_adapter(payload: dict, schema_path: Path) -> list[str]:
    schema = load_json(schema_path)
    errors: list[str] = []
    _validate_node(payload, schema, errors, schema)
    return errors


def _validate_node(value, schema: dict, errors: list[str], root: dict, path: str = "$") -> None:
    if "$ref" in schema:
        target = _resolve_ref(root, schema["$ref"])
        _validate_node(value, target, errors, root, path)
        return

    expected_type = schema.get("type")
    if expected_type == "object":
        if not isinstance(value, dict):
            errors.append(f"{path}: expected object")
            return
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{path}.{key}: missing required field")
        if schema.get("additionalProperties") is False:
            allowed = set(schema.get("properties", {}).keys())
            for key in value:
                if key not in allowed:
                    errors.append(f"{path}.{key}: unexpected field")
        properties = schema.get("properties", {})
        for key, child_schema in properties.items():
            if key in value:
                _validate_node(value[key], child_schema, errors, root, f"{path}.{key}")
        property_names = schema.get("propertyNames")
        if property_names:
            for key in value.keys():
                _validate_node(key, property_names, errors, root, f"{path}.<propertyName>")
        return

    if expected_type == "array":
        if not isinstance(value, list):
            errors.append(f"{path}: expected array")
            return
        min_items = schema.get("minItems")
        if min_items is not None and len(value) < min_items:
            errors.append(f"{path}: expected at least {min_items} items")
        if schema.get("uniqueItems"):
            rendered = [repr(item) for item in value]
            if len(rendered) != len(set(rendered)):
                errors.append(f"{path}: expected unique items")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                _validate_node(item, item_schema, errors, root, f"{path}[{index}]")
        return

    if expected_type == "string":
        if not isinstance(value, str):
            errors.append(f"{path}: expected string")
            return
        min_length = schema.get("minLength")
        if min_length is not None and len(value) < min_length:
            errors.append(f"{path}: expected min length {min_length}")

    if expected_type == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            errors.append(f"{path}: expected integer")
            return

    if expected_type == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            errors.append(f"{path}: expected number")
            return

    if expected_type == "boolean":
        if not isinstance(value, bool):
            errors.append(f"{path}: expected boolean")
            return

    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: unexpected enum value `{value}`")


def _resolve_ref(root: dict, ref: str) -> dict:
    parts = ref.lstrip("#/").split("/")
    node = root
    for part in parts:
        node = node[part]
    return node
