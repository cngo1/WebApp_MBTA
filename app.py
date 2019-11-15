"""
Application that helps find the nearest station and whether or not it is wheel chair accessible.
"""

from flask import Flask, render_template, request
from mbta_helper import find_stop_near

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mbta_helper/", methods = ["GET", "POST"])
def location():
    if request.method == "POST":
        place_name = str(request.form["location"])
        station, wheelchair = find_stop_near(place_name)
        value = ""
        if station:
            if wheelchair == "Inaccessible":
                value = "Inaccessible"
            elif wheelchair == "Accessible":
                value = "Accessible"
            else:
                value = "No information"
            return render_template("return_message.html", place_name=place_name, station=station, wheelchair=wheelchair)
        else:
            return render_template("next.html", error=True)
    return render_template("next.html", error=None)
