"""Narrow, dependency-free validation of repository-owned JSON schemas.

The supported JSON-Schema subset is intentionally small and explicit.  The
``x-forbidden-recursive-keys`` extension closes the data-redaction boundary at
every nested object, something a shallow field allowlist cannot guarantee.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "system" / "schemas"


class SchemaValidationError(ValueError):
    """Raised when a caller requires a persisted artifact to validate."""


def named_schema_path(name: str) -> Path:
    path = SCHEMA_DIR / f"{name}.schema.json"
    if not path.is_file():
        raise SchemaValidationError(f"unknown tracked schema: {name}")
    return path


def load_named_schema(name: str) -> dict[str, Any]:
    value = json.loads(named_schema_path(name).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SchemaValidationError(f"tracked schema is not an object: {name}")
    return value


def _type_matches(value: Any, expected: str) -> bool:
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, False)


def _validate(value: Any, schema: dict[str, Any], *, path: str, errors: list[str]) -> None:
    expected = schema.get("type")
    if isinstance(expected, str) and not _type_matches(value, expected):
        errors.append(f"{path}: expected {expected}")
        return
    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    enum = schema.get("enum")
    if isinstance(enum, list) and value not in enum:
        errors.append(f"{path}: expected one of {enum!r}")
    if isinstance(value, str):
        pattern = schema.get("pattern")
        if isinstance(pattern, str) and re.fullmatch(pattern, value) is None:
            errors.append(f"{path}: does not match required pattern")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        if isinstance(minimum, (int, float)) and value < minimum:
            errors.append(f"{path}: below minimum {minimum}")
        if isinstance(maximum, (int, float)) and value > maximum:
            errors.append(f"{path}: above maximum {maximum}")
    if isinstance(value, dict):
        forbidden = schema.get("x-forbidden-recursive-keys", [])
        if isinstance(forbidden, list):
            forbidden_keys = {item for item in forbidden if isinstance(item, str)}
            for key in sorted(value):
                if key in forbidden_keys:
                    errors.append(f"{path}.{key}: forbidden recursive key")
        required = schema.get("required", [])
        if isinstance(required, list):
            for key in required:
                if isinstance(key, str) and key not in value:
                    errors.append(f"{path}: missing required field {key}")
        properties = schema.get("properties", {})
        if not isinstance(properties, dict):
            properties = {}
        additional = schema.get("additionalProperties", True)
        for key, child in value.items():
            child_path = f"{path}.{key}"
            if key in properties and isinstance(properties[key], dict):
                child_schema = dict(properties[key])
            elif additional is False:
                errors.append(f"{child_path}: unexpected field")
                continue
            elif isinstance(additional, dict):
                child_schema = dict(additional)
            else:
                child_schema = {}
            if isinstance(forbidden, list) and "x-forbidden-recursive-keys" not in child_schema:
                child_schema["x-forbidden-recursive-keys"] = forbidden
            _validate(child, child_schema, path=child_path, errors=errors)
    if isinstance(value, list):
        items = schema.get("items")
        if isinstance(items, dict):
            for index, child in enumerate(value):
                _validate(child, items, path=f"{path}[{index}]", errors=errors)


def validate_document(document: Any, schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    _validate(document, schema, path="$", errors=errors)
    return errors


def validate_named(document: Any, name: str) -> list[str]:
    return validate_document(document, load_named_schema(name))


def require_valid_named(document: Any, name: str) -> None:
    errors = validate_named(document, name)
    if errors:
        raise SchemaValidationError(f"{name} validation failed: {'; '.join(errors)}")
