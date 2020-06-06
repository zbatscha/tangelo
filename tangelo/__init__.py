#!/usr/bin/env python

#-----------------------------------------------------------------------
# __init__.py
#-----------------------------------------------------------------------

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
import logging
import os

#-----------------------------------------------------------------------

logging.basicConfig(format='[%(asctime)-23s] %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    level=logging.INFO)

app = Flask('tangelo', template_folder='./templates', static_folder="./static")
csrf = CSRFProtect(app)

log = logging.getLogger('tangelo')

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = None

moment = Moment(app)

# import routes here to avoid circular import
from tangelo import routes
