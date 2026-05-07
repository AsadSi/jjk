"""Base classes and interfaces for data models."""

from typing import Any, Dict, List, Optional


class BaseDataModel:
    """Base class for all data models - provides common structure."""

    @staticmethod
    def get_slug_field() -> str:
        """Returns the field name used as slug identifier."""
        return "slug"

    @staticmethod
    def get_id_field() -> str:
        """Returns the field name used as id identifier."""
        return "id"

    @classmethod
    def find_by_slug(cls, data_list: List[Dict[str, Any]], slug: str) -> Optional[Dict[str, Any]]:
        """Generic method to find item by slug."""
        slug_field = cls.get_slug_field()
        for item in data_list:
            if item.get(slug_field) == slug:
                return item
        return None

    @classmethod
    def find_by_id(cls, data_list: List[Dict[str, Any]], item_id: str) -> Optional[Dict[str, Any]]:
        """Generic method to find item by id."""
        id_field = cls.get_id_field()
        for item in data_list:
            if item.get(id_field) == item_id:
                return item
        return None

    @classmethod
    def get_all_unique_values(
        cls, data_list: List[Dict[str, Any]], field: str
    ) -> List[str]:
        """Get all unique values for a given field across all items."""
        values = set()
        for item in data_list:
            field_value = item.get(field)
            if isinstance(field_value, list):
                values.update(field_value)
            elif field_value:
                values.add(field_value)
        return sorted(list(values))
