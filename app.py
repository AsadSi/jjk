import os

from flask import Flask, abort, render_template, request

from data.abilities import get_all_cursed_spirits
from data.arcs import get_all_arcs, get_arc
from data.characters_py import get_all_characters, get_character
from data.locations import get_all_locations, get_location
from data.techniques import get_all_techniques, get_technique

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
app.url_map.strict_slashes = False


def _character_matches_filters(character, search_lower: str, affiliation: str) -> bool:
    """Same rules as client-side filter on the characters page."""
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


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/characters")
def characters_list():
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
    character = get_character(slug)
    if not character:
        abort(404)
    return render_template("character.html", character=character)


@app.route("/techniques")
def techniques():
    return render_template(
        "techniques.html",
        techniques=get_all_techniques(),
        spirits=get_all_cursed_spirits(),
    )


@app.route("/techniques/<slug>")
def technique_page(slug: str):
    technique = get_technique(slug)
    if not technique:
        abort(404)
    return render_template("technique.html", technique=technique)


@app.route("/arcs")
def arcs_list():
    return render_template("arcs.html", arcs=get_all_arcs())


@app.route("/arcs/<slug>")
def arc_page(slug: str):
    arc = get_arc(slug)
    if not arc:
        abort(404)
    return render_template("arc.html", arc=arc)


@app.route("/locations")
def locations():
    return render_template("locations.html", locations=get_all_locations())


@app.route("/locations/<slug>")
def location_page(slug: str):
    location = get_location(slug)
    if not location:
        abort(404)
    return render_template("location.html", location=location)


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
