import os

from flask import Flask, abort, render_template, request

from data.abilities import get_all_cursed_spirits
from data.arcs import get_all_arcs, get_arc
from data.base import BaseDataModel
from data.characters_py import get_all_characters, get_character
from data.locations import get_all_locations, get_location
from data.techniques import get_all_techniques, get_technique
from utils import filter_items, get_active_filters

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.url_map.strict_slashes = False


def _character_matches_filters(character, search_lower: str, affiliation: str) -> bool:
    """Check if character matches search and affiliation filters."""
    if search_lower:
        name_ok = search_lower in character["name"].lower()
        jp_ok = search_lower in character.get("jpName", "").lower()
        if not name_ok and not jp_ok:
            return False
    if affiliation:
        aff_l = affiliation.lower()
        if not any(aff_l in a.lower() for a in character.get("affiliations", [])):
            return False
    return True


def _render_list_page(template_name, all_items, filters_config):
    """
    Generic handler for list pages with filters.
    
    Args:
        template_name: Template file to render
        all_items: List of items to display
        filters_config: Dict with keys: search_fields, filter_fields
    """
    search_term = request.args.get("search", "").strip()
    filter_dict = {}
    for field in filters_config.get("filter_fields", []):
        filter_dict[field] = request.args.get(field, "").strip()

    # Filter items
    items, visibility = filter_items(
        all_items,
        search_term=search_term,
        field_filters=filter_dict,
        search_fields=filters_config.get("search_fields", ["name"]),
    )

    visible_count = sum(1 for v in visibility.values() if v)
    active_filters = get_active_filters({k: v for k, v in filter_dict.items() if v})

    # Get unique values for filter dropdowns
    filter_options = {}
    for field in filters_config.get("filter_fields", []):
        filter_options[field] = BaseDataModel.get_all_unique_values(all_items, field)

    context = {
        "items": items,
        "search_query": search_term,
        "item_visibility": visibility,
        "visible_count": visible_count,
        "active_filters": active_filters,
        "filter_options": filter_options,
    }
    context.update(filter_dict)

    return render_template(template_name, **context)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/characters")
def characters_list():
    """List all characters with search and affiliation filters."""
    characters = get_all_characters()
    search_raw = request.args.get("search", "").strip()
    search_lower = search_raw.lower()
    affiliation_filter = request.args.get("affiliation", "").strip()

    all_affiliations = set()
    for c in characters:
        all_affiliations.update(c.get("affiliations", []))

    visibility = {
        c["slug"]: _character_matches_filters(c, search_lower, affiliation_filter)
        for c in characters
    }
    visible_count = sum(1 for v in visibility.values() if v)

    return render_template(
        "characters.html",
        characters=characters,
        search_query=search_raw,
        affiliation_filter=affiliation_filter,
        character_visibility=visibility,
        visible_count=visible_count,
        all_affiliations=sorted(list(all_affiliations)),
    )


@app.route("/characters/<slug>")
def character_page(slug: str):
    """Display individual character detail page."""
    character = get_character(slug)
    if not character:
        abort(404)
    return render_template("character.html", character=character)


@app.route("/techniques")
def techniques():
    """List all techniques and cursed spirits."""
    return render_template(
        "techniques.html",
        techniques=get_all_techniques(),
        spirits=get_all_cursed_spirits(),
    )


@app.route("/techniques/<slug>")
def technique_page(slug: str):
    """Display individual technique detail page."""
    technique = get_technique(slug)
    if not technique:
        abort(404)
    return render_template("technique.html", technique=technique)


@app.route("/arcs")
def arcs_list():
    """List all story arcs."""
    return render_template("arcs.html", arcs=get_all_arcs())


@app.route("/arcs/<slug>")
def arc_page(slug: str):
    """Display individual arc detail page."""
    arc = get_arc(slug)
    if not arc:
        abort(404)
    return render_template("arc.html", arc=arc)


@app.route("/locations")
def locations():
    """List all locations."""
    return render_template("locations.html", locations=get_all_locations())


@app.route("/locations/<slug>")
def location_page(slug: str):
    """Display individual location detail page."""
    location = get_location(slug)
    if not location:
        abort(404)
    return render_template("location.html", location=location)


@app.errorhandler(404)
def not_found(_error):
    """Handle 404 errors."""
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
