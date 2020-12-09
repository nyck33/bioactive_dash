# external imports
import dash
import dash_bootstrap_components as dbc
import os
from flask_login import LoginManager, UserMixin
from flask_mongoengine import MongoEngine

import random

# local imports
from utilities.auth import db, User as base
from utilities.config import engine, config_str, Config, config_dict

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    prevent_initial_callbacks=True,
)
#access the Flask application instance
server = app.server
app.config.suppress_callback_exceptions = False
#app.css.config.serve_locally = True
#app.scripts.config.serve_locally = True
app.title = 'Micronutrients and Bioactive'


# config
config_mode = config_dict['Debug']
server.config.from_object(config_mode)
server.config.update(
    SECRET_KEY='make this key random or hard to guess',
    SQLALCHEMY_DATABASE_URI=config_str,
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db_mongo=MongoEngine()
db_mongo.init_app(server)
db.init_app(server)

# for testing mongo connection
from models import (
    CNFFoodName, CNFConversionFactor, CNFNutrientAmount,
    CNFYieldAmount, CNFRefuseAmount
)



#todo: test mongo
def test_db():
    print(f'init.py test_db()')
    count=0
    for foodsource in CNFFoodName.objects:
        print(foodsource.description)
        count+=1
        if count > 10:
            break
test_db()

# Setup the LoginManager for the server
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


# Create User class with UserMixin
class User(UserMixin, base):
    pass


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

