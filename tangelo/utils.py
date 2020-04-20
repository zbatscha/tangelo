#!/usr/bin/env python

"""
utils.py

Provides methods for getting and manipulating database objects:
User, Widget, Subscription, etc.
"""

from tangelo.models import User, Widget, Post, Subscription
from tangelo import db, app
import tangelo.user_utils as user_utils
from sqlalchemy import desc

#-----------------------------------------------------------------------

def getUser(netid):
    """
    User associated with provided `netid`. If netid does not exist in
    database, creates a new User, and subscribed new User to `welcome` Widget.

    Parameters
    ----------
    netid : str

    Returns
    -------
    User
        User associated with `netid`.

    """
    user = User.query.filter_by(netid=netid).first()
    if not user:
        user = user_utils.createUser(netid)
        try:
            welcome_widget = Subscription(user=user, widget_id=1,
                                            grid_location={'x': 0, 'y': 0, 'width': 6, 'height': 2})
            db.session.add(welcome_widget)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    return user

#-----------------------------------------------------------------------

def getGridWidgets(current_user):
    """
    All widgets to be displayed on a user's dashboard.

    Parameters
    ----------
    current_user : User

    Returns
    -------
    list(dict)
        A list of widget-associated dictionaries, where keys are `widget_id`,
        gridstack `grid_location`, displayed widget `content`, the most recent
        post `widget_post`, and unique css/js `widget_style` if any.

    """
    subscriptions = Subscription.query.filter_by(user_id=current_user.id).all()
    displayed = [{
        'widget_id': sub.widget_id,
        'grid_location': sub.grid_location,
        'widget_name': sub.widget.name,
        'widget_post': getPost(sub.widget_id),
        'widget_style': sub.widget.style,
        'widget_admin': isAdmin(current_user, sub.widget_id)}
        for sub in subscriptions if sub.grid_location]

    return displayed

#-----------------------------------------------------------------------

def isAdmin(current_user, widget_id):
    widget = Widget.query.get(widget_id).first()
    return (current_user in widget.admins)

#-----------------------------------------------------------------------

def addSubscription(current_user, subscription):

    widget = Widget.query.get(subscription['widget_id'])
    if not widget:
        raise Exception('This widget does not exist.')
    if widget in current_user.widgets:
        raise Exception('You already have this widget.')
    try:
        new_follow = Subscription(user=current_user, widget_id=subscription['widget_id'],
                                    grid_location=subscription['grid_location'])
        db.session.add(new_follow)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise Exception(e)


def removeSubscription(current_user, widget_id):
    try:
        subscription = Subscription.query.filter_by(user_id=current_user.id).filter_by(widget_id=widget_id).first()
        if not subscription:
            raise Exception('Current user not subscribed to this widget.')
        db.session.delete(subscription)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f'Error removing subscription for widget {widget_id}. Rolling back.') from e

def updateSubscriptionLocation(current_user, widget_id, grid_location):
    subscription = Subscription.query.filter_by(user=current_user).filter_by(widget_id=widget_id).first()
    if not subscription:
        raise Exception(f'User not subscribed to widget {widget_id}. Error updating location.')
    try:
        subscription.grid_location = grid_location
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(f'Error updating location for widget {widget_id}. Rolling back.') from e

#-----------------------------------------------------------------------


def getAvailableFollowWidgets(current_user, searchName):
    widgets = Widget.query.filter(Widget.name.ilike('%'+searchName+'%')).all()
    not_subscribed = [widget for widget in widgets if current_user not in widget.users]
    return not_subscribed

#-----------------------------------------------------------------------

def createNewWidget(current_user, form):
    """
    Create a new widget with current_user as admin.

    Parameters
    ----------
    current_user : User
    form : CreateWidget

    Returns
    -------
    None

    """
    try:
        widget = Widget(name=form.name.data,
                        description=form.description.data,
                        access_type=form.access_type.data,
                        post_type=form.post_type.data)

        # place new widgets in top left corner of admins dashboard
        default_widget_location = {'x': 0, 'y': 0, 'width': 6, 'height': 2}
        subscription = Subscription(user=current_user, widget=widget,
                                    grid_location=default_widget_location)
        # current_user is the admin of the new widget
        widget.admins.append(current_user)
        db.session.add(widget)
        db.session.add(subscription)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise Exception(e)

#-----------------------------------------------------------------------

def addPost(current_user, form):
    """
    Create a new post with `current_user` as author.

    Parameters
    ----------
    current_user : User
    form : CreatePost

    Returns
    -------
    None

    """
    try:
        # check if valid widget
        widget = Widget.query.filter_by(id=form.widget_target.data).first()
        if not widget:
            raise Exception('Selected widget does not exist.')
        post = Post(content=form.content.data,
                    author=current_user,
                    widget=widget)
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(e)

#-----------------------------------------------------------------------


def addUserClosedWidget(form):
    """
    Allow admins to add a user to a closed (private or secret) widget.

    Parameters
    ----------
    form : CreateAddTeam

    Returns
    -------
    None

    """
    try:
        user = User.query.filter_by(netid=form.user.data).first()
        # check if valid widget
        widget = Widget.query.filter_by(id=form.widget_target.data).first()
        if not widget:
            raise Exception('Selected widget does not exist.')
        sub = Subscription(user=user, widget=widget)
        db.session.add(sub)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise Exception(e)

#-----------------------------------------------------------------------
"""
Critical: add validation check on CreateAddTeam form.
Admin should not be able to remove themself if they are the only admin.
"""
def removeUserClosedWidget(current_user, form):
    """
    Allow admins to remove a user from a closed (private or secret) widget.

    Parameters
    ----------
    form : CreateAddTeam

    Returns
    -------
    None

    """
    try:
        subscription = Subscription.query.filter_by(user_id=form.user.data).filter_by(widget_id=form.widget_target.data).first()
        if not subscription:
            raise Exception('Selected user not subscribed to this widget.')
        db.session.delete(subscription)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(e)

#-----------------------------------------------------------------------


def getWidgetChoicesForNewPost(current_user):
    """
    Return list of widgets that current user can post to.

    Parameters
    ----------
    current_user : User

    Returns
    -------
    list(tuple(int, str))
        A list of tuples representing valid widgets, where first element of
        tuple is the widget_id, and the second is the name of the widget.

    """
    all_widgets = current_user.widgets
    choices = []
    for widget in all_widgets:
        if widget.post_type == 'public' or current_user in widget.admins:
            choices.append((widget.id, widget.name))
    return choices

#-----------------------------------------------------------------------


def getValidWidgetsAdmin(current_user):
    """
    Return list of widgets that current user is an admin of.

    Parameters
    ----------
    current_user : User

    Returns
    -------
    list(tuple(int, str))
        A list of tuples representing administered widgets, where first element of
        tuple is the widget_id, and the second is the name of the widget.

    """
    all_widgets = current_user.widgets_admin
    choices = []
    for widget in all_widgets:
        choices.append((widget.id, widget.name))
    return choices

#-----------------------------------------------------------------------

"""
return the most recent post for now
"""
def getPost(widget_id):
    """
    Return the most recent post for Widget with primary_key of `widget_id`.

    Parameters
    ----------
    widget_id : int

    Returns
    -------
    dict(str:str)
        Dictionary containing an `author` key and `content` key.

    """
    post = Post.query.filter_by(widget_id=widget_id).order_by(desc(Post.create_dttm)).first()
    if not post:
        return {'content': '', 'author': ''}
    author = User.query.get(post.author_id)
    post = {'content': post.content, 'author': author.netid}
    return post
