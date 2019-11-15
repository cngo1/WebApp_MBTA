"""
Application that helps find the nearest station and whether or not it is wheel chair accessible.
"""

from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/mbta_helper/", methods = ["GET", "POST"])
def location():
    if request.method == "POST":
        place_name = str(request.form["location"])
        station_name, wheelchair_accessible = find_stop_near(place_name)
        value = ""
        if station_place:
            if wheelchair == 2:
                value = 'Inacessible'
            elif wheelchair == 1:
                value = "Accessible"
            else:
                value = "No information"
            return render_template("return_message.html", place_name = place_name, station_name=station_name, wheelchair_accessible=wheelchair_accessible)
        else:
            return render_template("mbta_helper.html", error=True)
        return render_template("mbta_helper.html", error=None)
