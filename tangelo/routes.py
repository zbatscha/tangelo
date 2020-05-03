#!/usr/bin/env python

#-----------------------------------------------------------------------
# routes.py
#-----------------------------------------------------------------------

from tangelo import app, db, log
from tangelo.CASClient import CASClient
from tangelo.tangeloService import getGreetingDayTime
from tangelo.models import User, Widget, Subscription
from flask import request, make_response, abort, redirect, url_for, flash
from flask import render_template, session
from flask_login import login_user, logout_user, login_required, current_user
import tangelo.forms as createForm
from tangelo import utils
import json
from flask import jsonify
from tangelo.weather_api import getWeather
import datetime

error_msg_global = "hmmm, something\'s not right."
# beta testing
authorized_users = ['zbatscha', 'rmthorpe', 'almejia', 'fawaza', 'josephoe', 'rdondero']

#-----------------------------------------------------------------------

@app.after_request
def add_header(response):
    response.cache_control.private = True
    response.cache_control.public = False
    return response

"""
Landing page. If user logged in, redirect them to their ashboard.
"""
@app.route('/', methods=['GET'])
@app.route('/welcome', methods=['GET'])
@app.route('/landing', methods=['GET'])
def welcome():
    if current_user.is_authenticated:
         return redirect(url_for('dashboard'))
    return make_response(render_template("tangelohome.html"))

#-----------------------------------------------------------------------

"""
Log in user with Princeton CAS.
"""
@app.route('/login', methods=['GET', 'POST'])
def login():

    netid = CASClient().authenticate()
    user = utils.getUser(netid)
    if not user:
        return redirect(url_for('welcome'))
    if netid not in authorized_users:
        return make_response(render_template("tangelohome.html"))
    # login and redirect to requested page
    user.authenticated = True
    login_user(user)
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('dashboard'))

#-----------------------------------------------------------------------

@app.route('/renderCustomWidget', methods=['GET', 'POST'])
def renderCustomWidget():
    return make_response(render_template(request.args.get('template')))

"""
Log out User current_user.
"""
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    logout_user()
    casClient = CASClient()
    casClient.authenticate()
    casClient.logout()

#-----------------------------------------------------------------------

"""
Tangelo Dashboard
"""
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    displayed_widgets = utils.getGridWidgets(current_user)
    create_widget_form = createForm.CreateWidget()
    return make_response(render_template('dashboard.html',
                title='Dashboard', widget_form=create_widget_form,
                displayedWidgets=displayed_widgets))

#-----------------------------------------------------------------------

"""
Populate widgets that conform to user's search in the left follow sidebar.
"""
@app.route('/getSearchWidgets', methods=['GET'])
@login_required
def getSearchFollowWidgets():
    text = request.args.get('text')
    availableWidgets = utils.getAvailableFollowWidgets(current_user, text)
    return make_response(render_template("availableWidgets.html",
        availableWidgets = availableWidgets))

#-----------------------------------------------------------------------

"""
Create a new widget with current_user as admin, if form is valid.
"""
@app.route('/createwidget', methods=['POST'])
@login_required
def createWidget():
    create_widget_form = createForm.CreateWidget()
    if create_widget_form.validate_on_submit():
        try:
            utils.createNewWidget(current_user, create_widget_form)
            flash(f'Your widget has been created!', 'success')
            return jsonify(success=True)
        except Exception as e:
            flash(e, 'danger')
            return jsonify(success=True)
    return make_response(render_template('createWidget.html', widget_form=create_widget_form)), 409

#-----------------------------------------------------------------------
"""
Add a post to a widget
"""
@app.route('/postUpdate', methods=['GET', 'POST'])
@login_required
def createPost():
    if request.method == "POST":
        try:
            postData = request.json.get('postData')
            utils.addPost(current_user, postData.get('widgetId'), postData.get('post'))
            flash('Your post has been created!', 'success') # not flashing on redirect
        except Exception as e:
            flash(str(e), 'danger') # not flashing on redirect
        return jsonify(success=True)
    abort(404)


@app.route('/updateBirthday', methods=['GET', 'POST'])
@login_required
def updateBirthday():
    if request.method == "POST":
        try:
            birthday_str = f"{request.form.get('year')}/{request.form.get('month')}/{request.form.get('day')}"
            birthday = datetime.datetime.strptime(birthday_str, '%Y/%m/%d')
            utils.updateBirthday(current_user, birthday)
        except Exception as e:
            print(e)
    return redirect(url_for('dashboard'))

#-----------------------------------------------------------------------
"""
Remove subscription from user after widget is dragged to trash/unfollow on left sidebar.
"""
@app.route('/update/removed', methods=['GET','POST'])
@login_required
def removeSubscription():
    response = jsonify(success=True)
    try:
        if request.method == "POST":
            widgets = request.json.get('widgets')
            for w in widgets:
                utils.removeSubscription(current_user, w['widget_id'])
    except Exception as e:
        flash(e.args[0], 'danger')
        response = jsonify(success=False), 500
    return response

#-----------------------------------------------------------------------

"""
currently not in use.
"""
@app.route('/update/added', methods=['GET','POST'])
@login_required
def addedSubscription():
    response = jsonify(success=True)
    try:
        if request.method == "POST":
            widgets = request.json.get('widgets')
    except Exception as e:
        print(e)
        flash(f'Error occured!', 'danger')
        response = jsonify(success=False)
    return response

#-----------------------------------------------------------------------

"""
Change grid_location/size of widget.
"""
@app.route('/update/change', methods=['GET','POST'])
@login_required
def changeSubscription():
    response = jsonify(success=True)
    try:
        if request.method == "POST":
            widgets = request.json.get('widgets')
            for w in widgets:
                utils.updateSubscriptionLocation(current_user, w['widget_id'], w['grid_location'])
    except Exception as e:
        # don't flash errors on changes
        response = jsonify(success=False)
    return response

#-----------------------------------------------------------------------

"""
Subscribe current_user to selected widget.
"""
@app.route('/addSubscription', methods=['GET','POST'])
@login_required
def addSubscription():
    response = jsonify(success=True)
    if request.method == "POST":
        subscription = request.json.get('subscription')
        try:
            utils.addSubscription(current_user, subscription.get('widget_id'))
        except Exception as e:
            flash(e.args[0], 'danger')
            response = jsonify(success=False)
    return response

#-----------------------------------------------------------------------

@app.route('/deleteWidget', methods=['GET', 'POST'])
@login_required
def deleteWidget():
    widget_name = ''
    try:
        delete_request = request.json.get('widget')
        widget_id = delete_request.get('widgetId')
        widget_name = utils.deleteWidget(current_user, widget_id)
        if not widget_name:
            return jsonify(success=False), 500
    except Exception as e:
        flash(error_msg_global, 'danger')
        return jsonify(success=False), 500
    flash(f'Successfully deleted {widget_name}', 'success')
    return jsonify(success=True), 200

@app.route('/updateWeather', methods=['GET', 'POST'])
@login_required
def updateWeather():
    weather_info = None
    try:
        coordinates = request.json.get('coordinates')
        if not coordinates:
            raise Exception('Error')
        weather_info = getWeather(coordinates.get('lat'), coordinates.get('long'))
    except Exception as e:
        pass
    if weather_info:
        return json.dumps(weather_info), 200
    return jsonify(success=False), 500
