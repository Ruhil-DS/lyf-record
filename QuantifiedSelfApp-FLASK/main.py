from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from Application.database import db
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from Application import workers
import os
import celery


# Creating the flask app variable
app = Flask(__name__)


# Initialising the DB using SQLAlchemy, pushing content to the app
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(CELERY_CONFIG={
    'broker_url': 'redis://localhost:6379/1',
    'result_backend': 'redis://localhost:6379/1',
    'timezone': 'Asia/Kolkata'
})
db.init_app(app)
app.app_context().push()


# Celery config
from Application.workers import *
celery_inst = make_celery(app)

api = Api(app)

# Importing the code from the Application module which contains all the necessary code!

from Application.controller_index import *
from Application.controller_dash import *
from Application.controller_celery import *

# ----------------------------
# API, CORS, JWT CONFIG ->
# ----------------------------

CORS(app)
jwt = JWTManager(app)

app.app_context().push()

from Application.api import *


api.add_resource(DashboardAPI, "/api/dashboard/")
api.add_resource(LoginAPI, "/api/login/")
api.add_resource(SignupAPI, "/api/signup/")
api.add_resource(trackersAPI, "/api/trackers/view/",
                 "/api/trackers/create/",
                 "/api/<int:tracker_id>/update/",
                 "/api/<int:tracker_id>/delete/")
api.add_resource(logSpecificAPI, "/api/<int:tracker_id>/details/",
                 "/api/<int:tracker_id>/log/",
                 "/api/<int:tracker_id>/<int:log_id>/update/",
                 "/api/<int:tracker_id>/<int:log_id>/delete/")
api.add_resource(trackerInfoAPI, "/api/<int:tracker_id>/getLogInfo/")
api.add_resource(logInfoAPI, "/api/<int:tracker_id>/<int:log_id>/getLogDetails/")


# ----------------------------
# CONFIG END
# ----------------------------
# Running the app

if __name__ == '__main__':
    app.run(debug=True)
