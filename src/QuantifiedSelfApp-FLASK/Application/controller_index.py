from flask import render_template
from flask import current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity

'''
# Code to generate random secret_key. Was randomly generating the secret key so that it doesn't redirect to the dashboard 
import random
import string

app.secret_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(25))
'''

# Secret key for session
app.secret_key = "sdivjbfiurnvsdivjbhuulvdkfvfd"
app.config["JWT_SECRET_KEY"] = "vnfeiuerblaseiondfboefubnersd"


# Below are the functions to render html templates on the homepage.
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/About/")
def about():
    return render_template("About.html")


@app.route("/credits/")
def credit():
    return render_template("credits.html")

