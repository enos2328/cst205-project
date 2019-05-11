"""
    File Name: API.py
    Name:   Magnus Harboe
            Athena Enosara
            Andrew Marmolejo
            Guadalupe Cisneros
    Due Date: 5 / 13 / 19
    Description: This program uses the spoonacular api to find recipes that fits what the user have in their fridge.
"""
from flask import Flask, render_template
import requests
import json
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

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


############################
### WHERE IS MAIN PAGE?? ###
############################
@app.route('/')
def main_page():
    return render_template('index.html')


########################
### RECIPE LIST PAGE ###
########################
@app.route('/recipes')
def main():
    try:
        r = requests.get(endpoint, params=payload, headers=headers)
        data = r.json()
    except:
        print('please try again')
    return render_template('recipes.html', data=data)  # redering the html template and also passing the information it gathered from the API

########################
## PICKED RECIPE PAGE ##
########################
@app.route('/recipes/<int:recipe_id>')
def recipe(recipe_id):
    endpoint = f'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{recipe_id}/information'
    payload = {
            'id': recipe_id
        }
    try:
        r = requests.get(endpoint, params=payload, headers=headers)
        data2 = r.json()
    except:
        print('please try again')
    return render_template('recipes_info.html', data=data2)  # redering the html template and also passing the information it gathered from the API


########################
## FAQ + CONTACT PAGE ##
########################
@app.route('/faq_page')
def faq_page():
    return render_template('search.html')

##################
## CONTACT PAGE ##
##################
@app.route('/contact')
def contact():
     return render_template('contact.html')
    
##################
## SEARCH PAGE? ##
##################
@app.route('/search')
def search():
    return redner_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
