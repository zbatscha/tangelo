#!/usr/bin/env python

#-----------------------------------------------------------------------
# routes.py
#-----------------------------------------------------------------------

from tangelo import app, db
from tangelo.CASClient import CASClient
from tangelo.tangeloService import getGreetingDayTime
from tangelo.models import User
from flask import request, make_response, abort, redirect, url_for
from flask import render_template, session

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

    username = CASClient().inSession()

    if username:
        username = username.strip()
        html = render_template('index.html',
            ampm=getGreetingDayTime(),
            username=username)
        response = make_response(html)
        return response

    # is user not in session, redirect to login page
    html = render_template('login.html')
    response = make_response(html)
    return response

#-----------------------------------------------------------------------

@app.route('/login', methods=['GET'])
def login():

    username = CASClient().authenticate()
    return redirect(url_for('index'))

#-----------------------------------------------------------------------

@app.route('/logout')
def logout():

    casClient = CASClient()
    casClient.authenticate()
    casClient.logout()

    return redirect(url_for('index'))

#-----------------------------------------------------------------------

@app.route('/about', methods=['GET'])
def about():

    username = CASClient().authenticate()
    username = username.strip()
    html = render_template('about.html',
        ampm=getGreetingDayTime(),
        username=username)
    response = make_response(html)
    return response

    # is user not in session, redirect to login page
    html = render_template('login.html')
    response = make_response(html)
    return response
