from flask import Flask, render_template
from flask_bootstrap import Bootstrap

"""
Athena Enosara
Partners: Andrew Marmolejo, Magnus Harboe, Andrew M., Guadalupe
Due Date: May 13, 2019
Final Project

Description: 
"""
app = Flask(__name__)
bootstrap = Bootstrap(app)

#################################
### APP ROUTE FOR SEARCH PAGE ###
#################################
@app.route('/')
def home():
	return render_template('search.html')

if __name__== '__main__':
    app.run(debug=True)


"""
Deliverables
This one wasn't too difficult. I did do the `{% %}` part a little wrong to begin with, but Andrew helped me out with that one. I went too much into the html part it turned out. Then I kept running into a problem with the second page where the image wasn't showing up, but with a second pair of eyes (Andrew) we figured out a simple solution where it was just that I forgot to pass the title and filename through the template.
"""