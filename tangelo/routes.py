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
from tangelo.forms import CreateWidget, WidgetPost
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
    form = WidgetPost()
    if form.validate_on_submit():
        # model_api.addPost(form)
        # flash(f'Your Post has been created!', 'success')
        flash(f'Still Working on this!', 'danger')
        return redirect(url_for('account'))
    return make_response(render_template('account.html', current_user=current_user, form=form))

#----------------------------------------------------------------------

@app.route('/create', methods=['GET', 'POST'])
@login_required
def createWidget():
    form = CreateWidget()
    if form.validate_on_submit():
        try:
            model_api.addWidget(form)
            flash(f'Your Widget has been created!', 'success')
            return redirect(url_for('account'))
        except Exception as e:
            print(e)
            flash(f'Error occured! Check stderr', 'danger')
    return make_response(render_template('create.html', title='Create Your Widget!', form=form))
