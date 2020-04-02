#!/usr/bin/env python

#-----------------------------------------------------------------------
# routes.py
#-----------------------------------------------------------------------

from tangelo import app, db
from tangelo.CASClient import CASClient
from tangelo.tangeloService import getGreetingDayTime
from tangelo.models import User
from flask import request, make_response, abort, redirect, url_for, flash
from flask import render_template, session
from flask_login import login_user, logout_user, login_required, current_user
from tangelo.generic import generic
from tangelo.forms import CreateWidget, CreatePost, CreateAddTeam
from tangelo import model_api

#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/welcome', methods=['GET'])
@app.route('/landing', methods=['GET'])
def welcome():
    if current_user.is_authenticated:
         return redirect(url_for('dashboard'))
    return make_response(render_template("tangelohome.html"))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():

    return make_response(render_template('dashboard.html',
                         ampm=getGreetingDayTime()))

#-----------------------------------------------------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():

    username = CASClient().authenticate()
    user = User.query.filter_by(netid=username).first()
    login_user(user)
    # redirect to requested page
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('dashboard'))

#-----------------------------------------------------------------------

@app.route('/logout', methods=['GET', 'POST'])
def logout():

    casClient = CASClient()
    casClient.authenticate()
    logout_user()
    casClient.logout()

#-----------------------------------------------------------------------

@app.route('/about', methods=['GET', 'POST'])
def about():
    return make_response(render_template('about.html',
                         ampm=getGreetingDayTime()))

#----------------------------------------------------------------------

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    widget_target_choices = model_api.getValidWidgetsPost(current_user)
    admin_widget_target_choices = model_api.getValidWidgetsAdmin(current_user)
    widget_form = CreateWidget()
    post_form = CreatePost()
    team_form = CreateAddTeam()
    post_form.widget_target.choices = widget_target_choices
    team_form.widget_target.choices = admin_widget_target_choices

    return make_response(render_template('account.html', title='Account', widget_form=widget_form, post_form=post_form, team_form=team_form, current_user=current_user))

@app.route('/createwidget', methods=['GET', 'POST'])
@login_required
def createWidget():
    widget_target_choices = model_api.getValidWidgetsPost(current_user)
    admin_widget_target_choices = model_api.getValidWidgetsAdmin(current_user)
    widget_form = CreateWidget()
    post_form = CreatePost()
    team_form = CreateAddTeam()
    post_form.widget_target.choices = widget_target_choices
    team_form.widget_target.choices = admin_widget_target_choices

    if widget_form.validate_on_submit():
        try:
            model_api.addWidget(widget_form)
            flash(f'Your widget has been created!', 'success')
            return redirect(url_for('account'))
        except Exception as e:
            print(e)
            flash(f'Error occured!', 'danger')
    return make_response(render_template('account.html', title='Account', widget_form=widget_form, post_form=post_form, team_form=team_form, current_user=current_user))

@app.route('/createpost', methods=['GET', 'POST'])
@login_required
def createPost():
    widget_target_choices = model_api.getValidWidgetsPost(current_user)
    admin_widget_target_choices = model_api.getValidWidgetsAdmin(current_user)
    widget_form = CreateWidget()
    post_form = CreatePost()
    team_form = CreateAddTeam()
    post_form.widget_target.choices = widget_target_choices
    team_form.widget_target.choices = admin_widget_target_choices

    if post_form.validate_on_submit():
        try:
            model_api.addPost(post_form)
            flash(f'Your post has been created!', 'success')
            return redirect(url_for('account'))
        except Exception as e:
            print(e)
            flash(f'Error occured!', 'danger')
    return make_response(render_template('account.html', title='Account', widget_form=widget_form, post_form=post_form, team_form=team_form, current_user=current_user))

@app.route('/addteam', methods=['GET', 'POST'])
@login_required
def addTeam():
    widget_target_choices = model_api.getValidWidgetsPost(current_user)
    admin_widget_target_choices = model_api.getValidWidgetsAdmin(current_user)
    widget_form = CreateWidget()
    post_form = CreatePost()
    team_form = CreateAddTeam()
    post_form.widget_target.choices = widget_target_choices
    team_form.widget_target.choices = admin_widget_target_choices
    

    if team_form.validate_on_submit():
        try:
            addBool = (dict(team_form.add_remove.choices).get(team_form.add_remove.data) == 'Add')
            print(addBool)
            if addBool:
                model_api.addSubscription(team_form)
                flash(f'{team_form.user.data} has been added to {dict(team_form.widget_target.choices).get(team_form.widget_target.data)}', 'success')
            else:
                model_api.removeSubscription(team_form)
                flash(f'{team_form.user.data} has been removed from {dict(team_form.widget_target.choices).get(team_form.widget_target.data)}', 'success' )
            return redirect(url_for('account'))
        except Exception as e:
            print(e)
            flash(f'Error occured!', 'danger')
    return make_response(render_template('account.html', title='Account', widget_form=widget_form, post_form=post_form, team_form=team_form, current_user=current_user))
        