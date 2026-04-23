from flask import Flask, abort, render_template

from data.characters_py import get_all_characters, get_character


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", characters=get_all_characters())


@app.route("/characters/<slug>")
def character_page(slug: str):
    character = get_character(slug)
    if not character:
        abort(404)
    return render_template("character.html", character=character)


@app.errorhandler(404)
def not_found(_error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
