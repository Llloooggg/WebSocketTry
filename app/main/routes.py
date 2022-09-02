import json

from flask import render_template

from . import main


@main.route("/")
def index():
    with open("data/data.json") as json_file:
        data = json.load(json_file)["data"]
    return render_template("index.html", data=data)
