#!/usr/bin/env python

#-----------------------------------------------------------------------
# __init__.py
#-----------------------------------------------------------------------

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates')

"""
export POSTGRES variables and SECRET_KEY key to environment and remove!
"""
POSTGRES_URL="127.0.0.1:5432"
POSTGRES_DB="tangelo_test"
POSTGRES_USER="postgres"
POSTGRES_PW="password$"
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
                                                        user=POSTGRES_USER,
                                                        pw=POSTGRES_PW,
                                                        url=POSTGRES_URL,
                                                        db=POSTGRES_DB)

app.config['SECRET_KEY'] = b'\xa1\xef\x97\xe0\xa3\xbe\xe8\xbcb\xaf\x81]Np`B'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# import routes here to avoid circular import
from tangelo import routes
