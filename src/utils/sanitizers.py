import html
from typing import Any, Dict

from pydantic import model_validator


class SanitizationMixin:
    """
    A mixin to provide sanitization for all string fields in a Pydantic model.
    """

    @model_validator(mode="before")
    @classmethod
    def sanitize_all_strings(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        sanitized_data: Dict[str, Any] = {}
        for key, value in data.items():
            if isinstance(value, str):
                sanitized_data[key] = html.escape(value).strip()
            else:
                sanitized_data[key] = value

        return sanitized_data
