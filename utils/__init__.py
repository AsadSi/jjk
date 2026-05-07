"""Utility functions for common Flask route operations."""

from typing import Any, Dict, List, Tuple


def filter_items(
    items: List[Dict[str, Any]],
    search_term: str = "",
    field_filters: Dict[str, str] = None,
    search_fields: List[str] = None,
) -> Tuple[List[Dict[str, Any]], Dict[str, bool]]:
    """
    Filter items by search term and field filters.
    
    Args:
        items: List of items to filter
        search_term: Search term (searches case-insensitively)
        field_filters: Dict of {field_name: filter_value}
        search_fields: List of fields to search in
        
    Returns:
        Tuple of (filtered_items, visibility_dict)
    """
    if field_filters is None:
        field_filters = {}
    if search_fields is None:
        search_fields = ["name"]

    search_lower = search_term.lower() if search_term else ""
    visibility = {}

    for item in items:
        item_slug = item.get("slug", item.get("id"))

        # Check search term
        if search_lower:
            match = any(search_lower in str(item.get(field, "")).lower() for field in search_fields)
            if not match:
                visibility[item_slug] = False
                continue

        # Check field filters
        matches_filters = True
        for filter_field, filter_value in field_filters.items():
            if not filter_value:  # Skip empty filters
                continue

            item_value = item.get(filter_field, [])
            filter_lower = filter_value.lower()

            if isinstance(item_value, list):
                match = any(filter_lower in str(v).lower() for v in item_value)
            else:
                match = filter_lower in str(item_value).lower()

            if not match:
                matches_filters = False
                break

        visibility[item_slug] = matches_filters

    return items, visibility


def get_visible_items(
    items: List[Dict[str, Any]], visibility: Dict[str, bool]
) -> List[Dict[str, Any]]:
    """Get items that are visible according to visibility dict."""
    return [item for item in items if visibility.get(item.get("slug", item.get("id")), False)]


def get_active_filters(filters_dict: Dict[str, str]) -> List[Dict[str, str]]:
    """Convert active filters dict to list format for templates."""
    active = []
    for key, value in filters_dict.items():
        if value:
            active.append(
                {
                    "key": key,
                    "label": key.replace("_", " ").title(),
                    "value": value,
                }
            )
    return active
