# Code Organization & Component Refactoring

## Overview

This project has been refactored to follow industry standards for code organization, reusability, and maintainability. The refactoring includes reusable template components, utilities for common operations, and consolidated CSS patterns.

## Directory Structure

### Templates (`templates/`)

- **`base.html`** - Main layout template with navigation, theme handling, and cursor effects
- **`partials/`** - Reusable component templates:
  - `nav.html` - Navigation component (unchanged)
  - `card.html` - Generic card component for displaying items
  - `hero.html` - Reusable hero section for page headers
  - `grid.html` - Generic grid layout wrapper
  - `filter-bar.html` - Reusable filter/search panel

### Static Files (`static/`)

- **`css/style.css`** - Core styling (colors, typography, layout)
- **`css/components.css`** - **NEW** Reusable component styles (grids, cards, filters)
- **`js/main.js`** - Client-side functionality

### Backend (`data/`, `utils/`)

- **`data/base.py`** - **NEW** Base data model class with common methods
- **`utils/__init__.py`** - **NEW** Utility functions for filtering and transformation
- **`utils/routes.py`** - **NEW** Flask route helpers and decorators

---

## Key Changes

### 1. Reusable Template Components

Instead of duplicating HTML across templates, common patterns are now in `partials/`:

#### Card Component (`card.html`)
```jinja
{% include "partials/card.html" %}
```
Pass context:
- `href` - Link destination
- `title` - Card title
- `jp_name` - Japanese name (optional)
- `card_image` - Image URL (optional)
- `card_fields` - List of field objects with `label`, `value`, `type`
- `card_description` - Description text
- `card_tags` - List of tags
- `card_action` - CTA text (default: "View more →")

#### Hero Section (`hero.html`)
```jinja
{% include "partials/hero.html" %}
```
Pass context:
- `hero_kanji` - Large background kanji character
- `hero_eyebrow` - Small text above title (optional)
- `hero_title_main` - Main title text
- `hero_title_em` - Title emphasis text (italic)
- `hero_subtitle` - Subtitle text

#### Grid Layout (`grid.html`)
```jinja
{% include "partials/grid.html" %}
```
Pass context:
- `section_id` - HTML id for the section
- `section_label` - Label above grid
- `grid_items` - Items to display
- `grid_type` - 'card', 'standard', or 'timeline'
- `empty_state` - Object with `title`, `message`, `action` (optional)

#### Filter Bar (`filter-bar.html`)
```jinja
{% include "partials/filter-bar.html" %}
```
Pass context:
- `filter_id` - Unique filter identifier
- `filters` - List of filter objects with `id`, `name`, `label`, `type`, etc.
- `form_action` - Form action URL
- `visible_count` - Number of visible results
- `active_filters` - List of active filters

### 2. Data Model Base Class

`data/base.py` provides common methods used by all data models:

```python
from data.base import BaseDataModel

# Find by slug
item = BaseDataModel.find_by_slug(characters, "yuji")

# Find by id
item = BaseDataModel.find_by_id(characters, "yuji")

# Get all unique values for a field
affiliations = BaseDataModel.get_all_unique_values(characters, "affiliations")
```

### 3. Flask Route Utilities

`utils/__init__.py` provides filtering and transformation functions:

```python
from utils import filter_items, get_active_filters

# Filter items with multiple criteria
items, visibility = filter_items(
    all_items,
    search_term="gojo",
    field_filters={"affiliations": "Tokyo"},
    search_fields=["name", "jpName"]
)

# Get active filters for display
active = get_active_filters({"affiliation": "Tokyo", "grade": ""})
```

### 4. Organized CSS Components

`static/css/components.css` consolidates reusable styles:

- **Grid Layouts**
  - `.grid--standard` - Responsive 1→2→3→4 column grid
  - `.grid--card` - Card-specific grid with consistent spacing
  - `.grid--timeline` - Linear list layout for sequential content

- **Card Components**
  - `.card` - Base card styles
  - `.card-image` - Image handling with overlay
  - `.card-header` - Title and metadata
  - `.card-tags` - Tag styling
  - `.link-text` - CTA styling

- **Filter Panel**
  - `.filter-panel` - Container
  - `.filter-row` - Input row layout
  - `.filter-input` / `.filter-select` - Input styling
  - `.filter-status` - Active filter display
  - `.filter-tag` - Tag styling

- **Empty State**
  - `.empty-state` - No results messaging

### 5. Simplified Flask Routes

`app.py` now uses a generic `_render_list_page()` function instead of duplicated filter logic:

```python
@app.route("/characters")
def characters_list():
    return _render_list_page(
        "characters.html",
        get_all_characters(),
        {
            "search_fields": ["name", "jpName"],
            "filter_fields": ["affiliations"],
        },
    )
```

---

## Benefits

✅ **DRY (Don't Repeat Yourself)** - Single source of truth for patterns  
✅ **Maintainability** - Easier to update UI consistently  
✅ **Scalability** - Add new pages quickly with existing components  
✅ **Performance** - Consolidated CSS reduces file transfers  
✅ **Consistency** - Enforces design patterns across templates  
✅ **Type Safety** - Base classes and utility functions clarify data structures  

---

## Adding a New List Page

To add a new resource (e.g., "items"):

### 1. Add route in `app.py`:
```python
@app.route("/items")
def items_list():
    return _render_list_page(
        "items.html",
        get_all_items(),
        {
            "search_fields": ["name", "jpName"],
            "filter_fields": ["category"],  # if applicable
        },
    )
```

### 2. Create `templates/items.html`:
```jinja
{% extends "base.html" %}
{% block content %}
{% include "partials/nav.html" %}

{% include "partials/hero.html" with context %}

{# Context: hero_kanji, hero_title_main, hero_subtitle, etc. #}

<section id="items-list">
  <p class="section-label reveal">All Items</p>
  
  {% include "partials/filter-bar.html" with context %}
  
  <div class="grid grid--card" id="items-grid">
    {% for item in items %}
      {% set href = "/items/" + item.slug %}
      {% set title = item.name %}
      {% set jp_name = item.jpName %}
      {% set card_description = item.description %}
      {% include "partials/card.html" %}
    {% endfor %}
  </div>
</section>
{% endblock %}
```

### 3. Provide template context:
```python
context = {
    "hero_kanji": "字",
    "hero_title_main": "Items",
    "hero_subtitle": "Browse all items",
    "items": items,
    "search_query": search_term,
    # ... other context
}
```

---

## Extending Components

All components are designed to be flexible. For example, the card component:

- Shows image only if `card_image` is provided
- Shows tags only if `card_tags` is provided
- Supports custom field layouts via `card_fields`
- Can be styled with `card_type` class

This means you can use the same component for different types of items with different data.

---

## Migration Guide

If updating existing templates to use new components:

1. **Extract hero sections** → Use `partials/hero.html`
2. **Replace card HTML** → Use `partials/card.html` with loop
3. **Remove inline grid CSS** → Replace with `.grid`, `.grid--card`, etc.
4. **Move filter HTML** → Use `partials/filter-bar.html`

All existing functionality is preserved; only the HTML structure has been refactored for reusability.

---

## Questions?

This refactoring follows industry best practices from:
- React component patterns (reusability, props)
- Django template inheritance and inclusion
- CSS methodology (SMACSS, BEM-inspired naming)
- Python utility/helper function patterns
