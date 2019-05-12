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
    return render_template('index.html', account_created = False)


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
## SEARCH PAGE  ##
##################
@app.route('/search', methods=['GET','POST']) 
def search():
    search_api_form = Search_API()  #   CREATES A Search_API() OBJECT

    #   IF search_api_form WAS SUMBITTED, RUNS THE CODE
    if search_api_form.validate_on_submit():
        user_input_list = search_api_form.search_ingredients.data.split()   # SPLITS THE USER INPUT (INGREDIENTS) INTO A STRING
        rank = search_api_form.search_type.data     #   SAVES THE SEARCH TYPE 1 OR 2 THE USER CHOSE
        payload = {     # FOR API SEARCH
            'fillIngredients': False,
            'ingredients': user_input_list,
            'limitLicense': False,
            'number': 5,
            'ranking': rank
        }
        try:
            r = requests.get(endpoint, params=payload, headers=headers)
            data = r.json()
        except:
            print('please try again')
        print('searched API')   #   PRINTS TO TERMINAL
        return render_template('recipes.html', data=data) 
    return render_template('search.html', search_api_form=search_api_form)


##################
## LOG IN PAGE  ##
##################
@app.route('/login', methods=['GET','POST']) 
def login():
    login_account_form = Account_Info() #   CREATES Account_Info OBJECT

    #   IF login_account_form FORM WAS SUBMITTED 
    if login_account_form.validate_on_submit():
        #   IF USER CHOSE THE LOG IN OPTION
        if login_account_form.create_login.data == '1':
            u_name = login_account_form.user_id.data    #   SAVES THE USER NAME TO PASS IN render_template
            print('logged in')  # PRINTS TO TERMINAL
            return render_template('yourrecipes.html', accounts=accounts, username=u_name)
        #   ELSE, THE USER CHOSE THE CREATE ACCOUNT OPTION
        else:
            store_account(login_account_form.user_id.data, login_account_form.password.data)    #   CREATES AN ACCOUNT
            print(accounts) #   PRINTS TO TERMINAL
            return render_template('index.html', account_created = True)
    return render_template('login.html', login_account_form=login_account_form)



if __name__ == '__main__':
    app.run(debug=True)
