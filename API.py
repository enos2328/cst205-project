"""
    File Name: API.py
    Name: Magnus Harboe
    Date: 5 / 1 / 19
    Description: This program uses the spoonacular api to find recipes that fits what the user have in their fridge.
"""
from flask import Flask, render_template
import requests
import json
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/home')
def main():
    return render_template('index.html')


@app.route('/recipes')
def recipes():
    ingredients = ['chicken', 'rice']
    rank = 2
    payload = {
        'fillIngredients': False,
        'ingredients': ingredients,
        'limitLicense': False,
        'number': 5,
        'ranking': rank
    }

    api_key = "4889bc9e24mshb28791c820806bep1256c2jsn921e1c55af76"

    endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

    headers = {
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "X-RapidAPI-Key": api_key
    }
    try:
        r = requests.get(endpoint, params=payload, headers=headers)
        data = r.json()
    except:
        print('please try again')
    return render_template('recipes.html', data=data)  # redering the html template and also passing the information it gathered from the API


@app.route('/recipes/<int:recipe_id>')
def recipe(recipe_id):
    endpoint = f'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipe_id}/information'
    api_key = "4889bc9e24mshb28791c820806bep1256c2jsn921e1c55af76"
    payload = {
        'id': recipe_id
    }
    headers = {
        "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
        "X-RapidAPI-Key": api_key
    }

    try:
        r = requests.get(endpoint, params=payload, headers=headers)
        data = r.json()
    except:
        print('please try again')
    return render_template('recipes_info.html', data=data)  # redering the html template and also passing the information it gathered from the API


if __name__ == '__main__':
    app.run(debug=True)

