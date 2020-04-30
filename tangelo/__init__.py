#!/usr/bin/env python

#-----------------------------------------------------------------------
# __init__.py
#-----------------------------------------------------------------------

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import logging
import os

#-----------------------------------------------------------------------

logging.basicConfig(format='[%(asctime)-23s] %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    level=logging.INFO)

app = Flask('tangelo', template_folder='./templates', static_folder="./static")

log = logging.getLogger('tangelo')

"""
export POSTGRES variables and SECRET_KEY key to environment and remove!
"""

app.config['SECRET_KEY'] = 'passwordstring'
#os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:asdf1234$@127.0.0.1:5432/tangelo_test' 
#os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = None

# import routes here to avoid circular import
from tangelo import routes
