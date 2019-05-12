"""
    File Name: API.py
    Name:   Magnus Harboe
            Athena Enosara
            Andrew Marmolejo
            Guadalupe Cisneros
    Due Date: 5 / 13 / 19
    Description: This program uses the spoonacular api to find recipes that fits what the user have in their fridge.
"""
from flask import Flask, render_template, flash, redirect, url_for
import requests
import json
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFError
from wtforms import PasswordField, StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'csumb-otter'    #   USED FOR FORMS
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

accounts = []   #   TO SAVE ACCOUNTS

api_key = "4889bc9e24mshb28791c820806bep1256c2jsn921e1c55af76"

endpoint = "https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/findByIngredients"

headers = {
    "X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
    "X-RapidAPI-Key": api_key
}

#################################
###     CLASS DEFINITIONS     ###
#################################
class Account_Info(FlaskForm):
    """  Class used for FlaskForm used for loging in & creating account """
    user_id = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login_options = [('1', 'Log In'), ('2', 'Create Account')]
    create_login = SelectField('Creating an Account or Logging In', choices = login_options, validators = [DataRequired()])
    submit = SubmitField('Submit')
class Add_Recipe(FlaskForm):
    """  Class for FlaskForm used to add a recipe to your 'account' """
    user_id = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    ingredients = StringField('Ingredients', validators=[DataRequired()])
    directions = StringField('Directions', validators=[DataRequired()])
    submit = SubmitField('Submit')
class Search_API(FlaskForm): 
    """   Class for FlaskForm used to search for recipe"""
    search_ingredients = StringField('Ingredients', validators=[DataRequired()])
    search_options = [('1', 'Method #1'), ('2', 'Method #2')]
    search_type = SelectField('Select A Search Method', choices = search_options, validators = [DataRequired()])
    submit = SubmitField('Submit')

##############################
###       FUNCTIONS        ###
##############################
#   STORES ACCOUNT INFORMATION INTO accounts LIST
def store_account(my_username, my_password):
    listofusernames = []    #   USED TO CHECK IF USERNAME ALREADY EXISTS

    count = 0
    #   SAVES CURRENT USERNAMES INTO listofusernames LIST
    for account in accounts:    
        listofusernames.append(accounts[count]['name'])
        count += 1
    
    #   IF USERNAME DOES NOT EXIST IN listofusernames LIST, IT WILL ADD INFORMATION TO accounts LIST
    if my_username not in listofusernames: 
        accounts.append(dict(
            name = my_username,
            pw = my_password,
            recipes = [] 
        ))  
#   ADDS NEW RECIPE TO THE USER'S recipes LIST
def add_recipe(my_username, my_password, my_title, my_ingredients, my_directions):
    count = 0   
    #   ITERATE THROUGHT accounts LIST
    for account in accounts:
    #   IF my_username MATCHES A NAME IN accounts LIST, IT WILL SAVE RECIPE INFORMATION
        if accounts[count]['name'] == my_username:
            accounts[count]['recipes'].append(dict(
                    title = my_title, 
                    ingredients = my_ingredients,
                    directions = my_directions
                ))
        count += 1





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
@app.route('/faq')
def faq_page():
    return render_template('faq.html')

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
    return render_template('search.html')


if __name__ == '__main__':
    app.run(debug=True)
