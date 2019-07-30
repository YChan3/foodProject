from app import app
from flask import render_template, request, redirect
from app.models import model, formopener

import requests

# restaurantApi = "97f9f42fa19bc08f9cfdefb874d94e65"

@app.route('/')
@app.route('/index')
def index():
    # parameters = {"q":"chinese",
    #               "count":9,
    #               "radius":8000,
    #               "sort":"rating",
    #               "order":"desc",
    #               "entity_id":280,
    #               "entity_type":"city"
    # }

    # headers = {"user-key":"97f9f42fa19bc08f9cfdefb874d94e65"}

    # response = requests.get("https://developers.zomato.com/api/v2.1/search", headers = headers, params = parameters)
    # data = response.json()
    # return data
    return "hi"

@app.route('/search')
def search():
    return render_template("index.html",  len=0)

# This is a menu screen...it's under the 'home.html' file
@app.route('/menu')
def menu():
    return render_template("home.html")

# This is the about page...it's under the 'about.html' file
@app.route('/about')
def about():
    return redirect("https://www.fintechfocus.com/")

# This is a social media/tweet screen...it's under the 'tweet.html' file
@app.route('/tweet')
def tweet():
    return render_template("tweet.html")


@app.route('/restaurants', methods = ['GET','POST'])
def restaurants():
    if request.method == "GET":
        return render_template("restaurants.html",  len=0)
    else:
        geoKey = "SdGzhhEFAKAcwxVZAbGnGtpiuz5WnnGA"

        term = request.form["term"].strip()
        distance = 0
        if request.form["distance"].strip().isdecimal():
            distance = int(request.form["distance"].strip())
        user_address = request.form["address"].strip()

        lat = None
        lng = None

        latlng_params = {"key":geoKey,
                          "outFormat":"json",
                          "location":user_address,
                          "maxResults":1
        }

        latlng = requests.get("https://www.mapquestapi.com/geocoding/v1/address?", params = latlng_params)
        latlng_data = latlng.json()

        if latlng_data["results"][0]["locations"]:
            lat = latlng_data["results"][0]["locations"][0]["latLng"]["lat"]
            lng = latlng_data["results"][0]["locations"][0]["latLng"]["lng"]

        headers = {"user-key":"97f9f42fa19bc08f9cfdefb874d94e65"}

        location_params = {}

        if not lat is None:
            location_params["lat"] = lat
            location_params["lon"] = lng

        location_response = requests.get("https://developers.zomato.com/api/v2.1/geocode",headers=headers, params = location_params)
        location_data = location_response.json()

        entity_type = location_data["location"]["entity_type"]
        entity_id = location_data["location"]["entity_id"]

        images = []
        names = []
        links = []
        location = []

        parameters = {"q":term,
                      "count":9,
                      "radius":distance,
                      "sort":"rating",
                      "order":"desc",
                      "entity_type":entity_type,
                      "entity_id":entity_id
        }

        if not lat is None:
            parameters["lat"] = lat
            parameters["lon"] = lng

        response = requests.get("https://developers.zomato.com/api/v2.1/search",headers=headers, params = parameters)
        data = response.json()
        # print(data)
        for dic in data["restaurants"]:
            names.append(dic["restaurant"]["name"].strip())
            images.append(dic["restaurant"]["featured_image"])
            links.append(dic["restaurant"]["url"])
            location.append(dic["restaurant"]["location"]["address"])
        if not names:
            return "Template for ingredient not found"
        # return data
        return render_template("restaurants.html", term = term, len = len(names), names = names, images = images, links = links)

@app.route('/results', methods = ['GET','POST'])
def result():
    if request.method == "GET":
        return redirect("/search")
    else:
        ingredient = request.form["ingredient"].strip()
        images = []
        recipes = []
        links = []

        parameters = {"app_id": "$f4118168",
                  "app_key": "$684f7ea2d63b6584768c1499c1a2407f",
                  "q":ingredient,
                  "to":9
        }

        response = requests.get("https://api.edamam.com/search", params = parameters)
        data = response.json()
        for dic in data["hits"]:
            recipes.append(dic["recipe"]["label"].strip())
            images.append(dic["recipe"]["image"])
            links.append(dic["recipe"]["url"])
        if not recipes:
            return "Template for ingredient not found"
        return render_template("index.html", craving = ingredient, len = len(recipes), recipes = recipes, images = images, links = links)