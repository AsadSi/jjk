from flask import Flask, abort, render_template, request

from data.characters_py import get_all_characters, get_character
from data.arcs import get_all_arcs, get_arc
from data.locations import get_all_locations, get_location
from data.abilities import get_all_cursed_spirits, get_cursed_spirit, get_all_techniques, get_technique


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/characters")
def characters_list():
    characters = get_all_characters()
    search_query = request.args.get('search', '').lower()
    affiliation_filter = request.args.get('affiliation', '')
    
    # Filter by search query
    if search_query:
        characters = [c for c in characters if search_query in c['name'].lower() or search_query in c.get('jpName', '').lower()]
    
    # Filter by affiliation
    if affiliation_filter:
        characters = [c for c in characters if any(affiliation_filter.lower() in aff.lower() for aff in c.get('affiliations', []))]
    
    # Get unique affiliations for filter dropdown
    all_affiliations = set()
    for c in get_all_characters():
        all_affiliations.update(c.get('affiliations', []))
    
    return render_template("characters.html", 
                         characters=characters, 
                         search_query=search_query,
                         affiliation_filter=affiliation_filter,
                         all_affiliations=sorted(list(all_affiliations)))


@app.route("/characters/<slug>")
def character_page(slug: str):
    character = get_character(slug)
    if not character:
        abort(404)
    return render_template("character.html", character=character)


@app.route("/techniques")
def techniques():
    return render_template("techniques.html", techniques=get_all_techniques(), spirits=get_all_cursed_spirits())


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
