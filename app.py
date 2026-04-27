from flask import Flask, abort, render_template

from data.characters_py import get_all_characters, get_character
from data.arcs import get_all_arcs, get_arc
from data.locations import get_all_locations, get_location
from data.abilities import get_all_cursed_spirits, get_cursed_spirit, get_all_techniques, get_technique


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", characters=get_all_characters())


# Characters routes
@app.route("/characters")
def characters():
    return render_template("characters.html", characters=get_all_characters())


@app.route("/characters/<slug>")
def character_page(slug: str):
    character = get_character(slug)
    if not character:
        abort(404)
    return render_template("character.html", character=character)


# Story Arcs routes
@app.route("/arcs")
def arcs():
    return render_template("arcs.html", arcs=get_all_arcs())


@app.route("/arcs/<slug>")
def arc_page(slug: str):
    arc = get_arc(slug)
    if not arc:
        abort(404)
    return render_template("arc.html", arc=arc)


# Locations routes
@app.route("/locations")
def locations():
    return render_template("locations.html", locations=get_all_locations())


@app.route("/locations/<slug>")
def location_page(slug: str):
    location = get_location(slug)
    if not location:
        abort(404)
    return render_template("location.html", location=location)


# Cursed Spirits routes
@app.route("/cursed-spirits")
def cursed_spirits():
    return render_template("cursed_spirits.html", spirits=get_all_cursed_spirits())


@app.route("/cursed-spirits/<slug>")
def cursed_spirit_page(slug: str):
    spirit = get_cursed_spirit(slug)
    if not spirit:
        abort(404)
    return render_template("cursed_spirit.html", spirit=spirit)


# Techniques routes
@app.route("/techniques")
def techniques():
    return render_template("techniques.html", techniques=get_all_techniques())


@app.route("/techniques/<slug>")
def technique_page(slug: str):
    tech = get_technique(slug)
    if not tech:
        abort(404)
    return render_template("technique.html", technique=tech)


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
