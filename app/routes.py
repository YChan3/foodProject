from app import app
from flask import render_template, request, redirect
from app.models import model, formopener

import requests

# resturantApi = "97f9f42fa19bc08f9cfdefb874d94e65"

@app.route('/')
@app.route('/index')
def index():
    # parameters = {"app_id": "$f4118168",
    #               "app_key": "$684f7ea2d63b6584768c1499c1a2407f",
    #               "q":"chicken",
    #               "to":9
    # }

    # response = requests.get("https://api.edamam.com/search", params = parameters)
    # data = response.json()
    # print(type(data))
    # print(data)
    return "Welcome"

@app.route('/search')
def search():
    return render_template("index.html",  len=0)

# This is a menu screen...it's under the 'home.html' file
@app.route('/menu')
def menu():
    return render_template("home.html")

# This is a social media/tweet screen...it's under the 'tweet.html' file
@app.route('/tweet')
def tweet():
    return render_template("tweet.html")

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
            #

# I'm adding in a bunch of pictures for 3 recipes per category/craving/ingredient (assuming your API doesn't work)! Also I'm making a menu! So instead of it just displaying recipes, I think it could be cool to add a more social impact page on food issues... I'm testing it out in the tweet.html file

