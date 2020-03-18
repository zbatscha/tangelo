#!/usr/bin/env python

#-----------------------------------------------------------------------
# tangelo.py
#-----------------------------------------------------------------------

from sys import argv
from database import Database
from tangeloService import getGreetingDayTime
from flask import Flask, request, make_response, abort, redirect, url_for
from flask import render_template, session
from CASClient import CASClient

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates')

app.secret_key = b'\xa1\xef\x97\xe0\xa3\xbe\xe8\xbcb\xaf\x81]Np`B'

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

@app.route('/logout', methods=['GET'])
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

#-----------------------------------------------------------------------

if __name__ == '__main__':
    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='localhost', port=int(argv[1]), debug=True)
