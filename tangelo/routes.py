#!/usr/bin/env python

#-----------------------------------------------------------------------
# routes.py
#-----------------------------------------------------------------------

from tangelo import app, db, log
from tangelo.CASClient import CASClient
from flask import request, make_response, abort, redirect, url_for, flash
from flask import render_template
from flask_login import login_user, logout_user, login_required, current_user
import tangelo.forms as createForm
from tangelo import utils
import json
from flask import jsonify
import datetime

error_msg_global = "hmmm, something\'s not right."
# beta testing
authorized_users = ['zbatscha', 'rmthorpe', 'almejia', 'fawaza', 'josephoe', 'rdondero',
                    'sazam', 'aarbab', 'cl43', 'tinaas', 'eacruz']

#-----------------------------------------------------------------------

@app.after_request
def add_header(response):
    response.cache_control.private = True
    response.cache_control.public = False
    return response

@app.before_request
def before_request():
    if not request.is_secure and app.env != "development":
        url = request.url.replace("http://", "https://", 1)
        code = 301
        return redirect(url, code=code)

#-----------------------------------------------------------------------

"""
Login landing page. If user previously authenticated, redirect them to
their dashboard.
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
Log in user with Princeton CAS, and set flask_login current_user.
If user does not exist, create a new user account associated with CAS provided
netid. Redirect to next page (or dashboard).
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    # retrieve netid from CAS
    netid = CASClient().authenticate()
    # retrieve user associated with netid
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
Tangelo Dashboard. Render with a user's subscribed widgets.
"""
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    # retrieve user subscriptions and associated display info
    displayed_widgets = utils.getGridWidgets(current_user)
    create_widget_form = createForm.CreateWidget()
    return make_response(render_template('dashboard.html',
                title='Dashboard', widget_form=create_widget_form,
                displayedWidgets=displayed_widgets))

#-----------------------------------------------------------------------

"""
Render the specified template. Route unique to Tangelo admin custom widgets.
"""
@app.route('/renderCustomWidget', methods=['GET', 'POST'])
def renderCustomWidget():
    return make_response(render_template(request.args.get('template')))

#-----------------------------------------------------------------------

"""
Populate left follow sidebar with widgets that conform to user's search.
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
If CreateWidget form is valid on submit, create a new widget with current_user
as admin, and reload page. If form not valid, renders form with errors.
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
            flash(str(e), 'danger')
            return jsonify(success=True)
    return make_response(render_template('createWidget.html',
        widget_form=create_widget_form)), 409

#-----------------------------------------------------------------------

"""
Update the displayed post. Only accessible by widget admins.
"""
@app.route('/postUpdate', methods=['GET', 'POST'])
@login_required
def createPost():
    if request.method == "POST":
        try:
            postData = request.json.get('postData')
            utils.addPost(current_user, postData.get('widgetId'), postData.get('post'))
            flash('Your post has been created!', 'success')
        except Exception as e:
            flash(str(e), 'danger')
        return jsonify(success=True)
    abort(404)

#-----------------------------------------------------------------------

"""
Update a user's birthday.
"""
@app.route('/updateBirthday', methods=['GET', 'POST'])
@login_required
def updateBirthday():
    if request.method == "POST":
        try:
            birthday_str = f"{request.form.get('year')}/{request.form.get('month')}/{request.form.get('day')}"
            birthday = datetime.datetime.strptime(birthday_str, '%Y/%m/%d')
            utils.updateBirthday(current_user, birthday)
        except Exception as e:
            log.error(f'Error updating {current_user} birthday', exc_info=True)
    return redirect(url_for('dashboard'))

#-----------------------------------------------------------------------

"""
Unsubscribe user from specified widget after widget is dragged to and released
over trash/unfollow on left sidebar.
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
Update grid_location of widget on drag and resize.
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

"""
Delete widget administered by current_user. Removes subscription for all
followers.
"""
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
