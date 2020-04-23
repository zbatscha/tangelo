#!/usr/bin/env python

"""
utils.py

Provides methods for accessing and manipulating tables:
User, Widget, Subscription, AdminAssociation, Post.
"""

#-----------------------------------------------------------------------

from tangelo import db, app, log
from tangelo.models import User, Widget, Post, Subscription
import tangelo.user_utils as user_utils
from sqlalchemy import desc

error_msg_global = "hmmm, something\'s not right."

#-----------------------------------------------------------------------

def getUser(netid):
    """
    User associated with provided `netid`. If netid does not exist in
    database, creates a new User, and subscribes new User to `welcome` Widget.

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
        log.info(f'User with netid = \"{netid}\" does not exist. Creating User...')
        user = user_utils.createUser(netid)
        if user:
            log.info(f'Subscribing {user} to Welcome widget...')
            try:
                addSubscription(user, 1)
            except:
                log.critical(f'Failed to subscribe new user {user} to Welcome widget.', exc_info=True)

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
    """
    Checks if current_user is an administrator if widget with primary_key = widget_id.

    Parameters
    ----------
    current_user : User
    widget_id : int

    Returns
    -------
    bool
        True if current_user is an admin. False otherwise.

    """
    widget = Widget.query.get(widget_id)
    return (current_user in widget.admins)

#-----------------------------------------------------------------------

def addSubscription(current_user, widget_id, grid_location={'x': 0, 'y': 0, 'width': 6, 'height': 2}):
    """
    Subscribe User current_user to widget with primary_key = widget_id.
    Set initial grid_location.

    Parameters
    ----------
    current_user : User
    widget_id : int
    grid_location : dict

    Returns
    -------
    None

    """
    # validate widget_id
    try:
        widget_id = int(widget_id)
    except:
        log.critical(f'{current_user} attempted to subscribe with non-int widget_id.')
        raise Exception(f'{error_msg_global}')

    widget = Widget.query.get(widget_id)
    if not widget:
        log.error(f'{current_user} attempted to subscribe to non-existing widget with id = \"{widget_id}\".')
        raise Exception(f'{error_msg_global}')
    if widget in current_user.widgets:
        log.info(f'{current_user} attempted to re-subscribe to existing {widget}.')
        raise Exception(f'{error_msg_global} You are already subscribed to {widget.name}.')

    try:
        new_subscription = Subscription(user=current_user, widget_id=widget_id,
                                    grid_location=grid_location)
        db.session.add(new_subscription)
        db.session.commit()
        log.info(f'{current_user} subscribed to {widget}.')

    except Exception as e:
        db.session.rollback()
        log.warning(f'Failed to subscribe {current_user} to {widget}.', exc_info=True)
        raise Exception(error_msg_global)

#-----------------------------------------------------------------------

def removeSubscription(current_user, widget_id):
    """
    Unsubscribe User current_user to widget with primary_key = widget_id.

    Parameters
    ----------
    current_user : User
    widget_id : int

    Returns
    -------
    None

    """
    subscription = None
    widget = None
    try:
        widget_id = int(widget_id)
        widget = Widget.query.get(widget_id)

        if not widget:
            log.error(f'Failed to remove subscription for {current_user}. widget_id = {widget_id} does not exist.')
            raise Exception(error_msg_global)

        subscription = Subscription.query.filter_by(user=current_user, widget=widget).first()
        if not subscription:
            log.error(f'{current_user} tried unsubscribing from non-existing subscription of {widget}')
            raise Exception(error_msg_global)

        db.session.delete(subscription)
        db.session.commit()
        log.info(f'{current_user} unsubscribed from {widget}')
    except Exception as e:
        db.session.rollback()
        log.error(f'Error removing subscription for widget {widget_id}. Rolling back.')
        raise Exception(error_msg_global + f'\"{widget.name}\" cannot be removed.')

#-----------------------------------------------------------------------

def updateSubscriptionLocation(current_user, widget_id, grid_location):
    """
    Update widget grid_location.

    Parameters
    ----------
    current_user : User
    widget_id : int
    grid_location : dict

    Returns
    -------
    None

    """
    subscription = None
    widget = None
    try:
        widget_id = int(widget_id)
        widget = Widget.query.get(widget_id)

        if not widget:
            log.error(f'Failed to update subscription for {current_user}. widget_id = {widget_id} does not exist.')
            return

        subscription = Subscription.query.filter_by(user=current_user, widget=widget).first()
        if not subscription:
            log.error(f'Error updating location: {current_user} not subscribed to {widget}.')
            return

        subscription.grid_location = grid_location
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        log.error(f'Error updating location for {subscription}. Rolling back.', exc_info=True)

#-----------------------------------------------------------------------

def getAvailableFollowWidgets(current_user, widgetSearchText):
    """
    Return all widgets that conform to widgetSearchText that current_user is
    not currently subscribed to.

    Parameters
    ----------
    current_user : User
    widgetSearchText : str

    Returns
    -------
    list(Widget)
        List of Widget objects that are available for current_user to follow.

    """
    widgets = Widget.query.filter(Widget.name.ilike('%'+widgetSearchText+'%')).all()
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
        log.info(f'{current_user} creating new widget...')
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
        log.info(f'Success: {current_user} created a new widget: {widget}.')
    except Exception as e:
        db.session.rollback()
        log.error(f'Failed to create a widget for admin {current_user}.',
            exc_info=True)
        raise Exception(f'{error_msg_global} Could not create \"{form.name.data}\" :( ')

#-----------------------------------------------------------------------

def getPost(widget_id):
    """
    Return the most recent post for Widget with primary_key of `widget_id`.

    Parameters
    ----------
    widget_id : int

    Returns
    -------
    dict
        Dictionary containing an `author` key and `content` key.

    """
    post = Post.query.filter_by(widget_id=widget_id).order_by(desc(Post.create_dttm)).first()
    if not post:
        return {'content': '', 'author': ''}
    author = User.query.get(post.author_id)
    post = {'content': post.content, 'author': author.netid}
    return post

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










"""
Methods not yet in use....
"""
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
