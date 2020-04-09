#!/usr/bin/env python

#-----------------------------------------------------------------------
# __init__.py
#-----------------------------------------------------------------------

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates', static_folder="./static")

"""
export POSTGRES variables and SECRET_KEY key to environment and remove!
"""

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# import routes here to avoid circular import
from tangelo import routes
