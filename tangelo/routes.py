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

error_msg_global = "hmmm, something\'s not right."

#-----------------------------------------------------------------------

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
    # login and redirect to requested page
    login_user(user)
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('dashboard'))

#-----------------------------------------------------------------------

"""
Log out User current_user.
"""
@app.route('/logout', methods=['GET', 'POST'])
def logout():

    casClient = CASClient()
    casClient.authenticate()
    logout_user()
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
    displayed_widgets = utils.getGridWidgets(current_user)
    if create_widget_form.validate_on_submit():
        try:
            utils.createNewWidget(current_user, create_widget_form)
            flash(f'Your widget has been created!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            flash(e, 'danger')

    flash('Still need to fix form validation without page reload', 'danger')
    return make_response(render_template('dashboard.html', title='Dashboard',
        widget_form=create_widget_form, displayedWidgets=displayed_widgets))

#-----------------------------------------------------------------------
"""
Add a post to a widget
"""
@app.route('/postUpdate', methods=['GET', 'POST'])
def createPost():
    post = request.args.get('post')
    id = request.args.get('id')
    try:
        utils.addPost(current_user, id, post)
        flash(f'Your post has been created!', 'success')
        return redirect(url_for('dashboard'))
    except Exception as e:
        print(e)
        flash(f'Error occured!', 'danger')


#-----------------------------------------------------------------------
"""
Remove subscription from user after widget is dragged to trash/unfollow on left sidebar.
"""
@app.route('/update/removed', methods=['GET','POST'])
def removeSubscription():
    response = jsonify(success=True)
    try:
        if request.method == "POST":
            widgets = request.json.get('widgets')
            for w in widgets:
                utils.removeSubscription(current_user, w['widget_id'])
    except Exception as e:
        flash(e, 'danger')
        response = jsonify(success=False)
    return response

#-----------------------------------------------------------------------

"""
currently not in use.
"""
@app.route('/update/added', methods=['GET','POST'])
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
def addSubscription():
    response = jsonify(success=True)
    if request.method == "POST":
        subscription = request.json.get('subscription')
        try:
            utils.addSubscription(current_user, subscription.get('widget_id'))
        except Exception as e:
            flash(e, 'danger')
            response = jsonify(success=False)
    return response

#-----------------------------------------------------------------------



"""
Not currently in use...
"""
#-----------------------------------------------------------------------

"""
Create a new post with current_user as author, if form is valid.

@app.route('/createpost', methods=['GET', 'POST'])
@login_required
def createPost():
    widget_target_choices = utils.getWidgetChoicesForNewPost(current_user)
    admin_widget_target_choices = utils.getValidWidgetsAdmin(current_user)
    widget_form = createForm.CreateWidget()
    post_form = createForm.CreatePost()
    team_form = createForm.CreateAddTeam()
    post_form.widget_target.choices = widget_target_choices
    team_form.widget_target.choices = admin_widget_target_choices

    if post_form.validate_on_submit():
        try:
            utils.addPost(current_user, post_form)
            flash(f'Your post has been created!', 'success')
            return redirect(url_for('account'))
        except Exception as e:
            print(e)
            flash(f'Error occured!', 'danger')
    return make_response(render_template('account.html', title='Account', widget_form=widget_form, post_form=post_form, team_form=team_form, current_user=current_user))
"""
#-----------------------------------------------------------------------

"""
Add users to a private widget.
"""
@app.route('/addteam', methods=['GET', 'POST'])
@login_required
def addTeam():
    widget_target_choices = utils.getWidgetChoicesForNewPost(current_user)
    admin_widget_target_choices = utils.getValidWidgetsAdmin(current_user)
    widget_form = createForm.CreateWidget()
    post_form = createForm.CreatePost()
    team_form = createForm.CreateAddTeam()
    post_form.widget_target.choices = widget_target_choices
    team_form.widget_target.choices = admin_widget_target_choices


    if team_form.validate_on_submit():
        try:
            addBool = (dict(team_form.add_remove.choices).get(team_form.add_remove.data) == 'Add')
            if addBool:
                utils.addUserClosedWidget(team_form)
                flash(f'{team_form.user.data} has been added to {dict(team_form.widget_target.choices).get(team_form.widget_target.data)}', 'success')
            else:
                utils.removeUserClosedWidget(team_form)
                flash(f'{team_form.user.data} has been removed from {dict(team_form.widget_target.choices).get(team_form.widget_target.data)}', 'success' )
            return redirect(url_for('account'))
        except Exception as e:
            print(e)
            flash(f'Error occured!', 'danger')
    return make_response(render_template('account.html', title='Account', widget_form=widget_form, post_form=post_form, team_form=team_form, current_user=current_user))

#-----------------------------------------------------------------------

"""
Deprecated
"""
@app.route('/about', methods=['GET', 'POST'])
def about():
    return make_response(render_template('about.html', title='About'))

#----------------------------------------------------------------------

"""
Deprecated
"""
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    widget_target_choices = utils.getWidgetChoicesForNewPost(current_user)
    admin_widget_target_choices = utils.getValidWidgetsAdmin(current_user)
    widget_form = createForm.CreateWidget()
    post_form = createForm.CreatePost()
    team_form = createForm.CreateAddTeam()
    post_form.widget_target.choices = widget_target_choices
    team_form.widget_target.choices = admin_widget_target_choices

    return make_response(render_template('account.html', title='Account', widget_form=widget_form, post_form=post_form, team_form=team_form, current_user=current_user))
