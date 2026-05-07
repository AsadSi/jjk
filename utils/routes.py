"""Route helpers and decorators for common patterns."""

from typing import Any, Callable, Dict, Optional
from flask import abort, render_template


def detail_route(data_getter: Callable, template_name: str) -> Callable:
    """
    Decorator that handles standard detail page routes.
    
    Usage:
        @app.route("/items/<slug>")
        @detail_route(get_item, "item.html")
        def item_page(slug: str, item: Dict[str, Any]):
            return render_template_with_nav(template_name, item=item)
    """

    def decorator(view_func: Callable) -> Callable:
        def wrapper(slug: str, *args, **kwargs):
            data = data_getter(slug)
            if not data:
                abort(404)
            return view_func(slug, data, *args, **kwargs)

        wrapper.__name__ = view_func.__name__
        return wrapper

    return decorator


def render_template_with_nav(template_name: str, **context) -> str:
    """Shortcut to render template with nav included."""
    return render_template(template_name, **context)
