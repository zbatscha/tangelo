#!/usr/bin/env python

#-----------------------------------------------------------------------
# test_db.py
#-----------------------------------------------------------------------

"""
Provides methods for unittesting the SQLALchemy+postgres db table relationships
and deletion cascades.
"""

import unittest
from tangelo.models import User, Widget, Subscription, Post, AdminAssociation
import tangelo.user_utils as user_utils
import tangelo.utils as utils
from tangelo import app, db
import sys
import os

#-----------------------------------------------------------------------

class DBTest(unittest.TestCase):

    def create_app(self):
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

        # create users
        user_1 = User(netid='zbatscha', email='zbatscha@princeton.edu',
                      first_name='Ziv', last_name='Batscha',
                      display_name='this_is_my_display_name')
        user_2 = User(netid='rmthorpe', email='rmthorpe@princeton.edu',
                      first_name='Ryan', last_name='Thorpe',
                      display_name='Ryyyaaannn')
        user_3 = User(netid='almejia', email='almejia@princeton.edu',
                      first_name='Austin', last_name='Mejia',
                      display_name='Auuuussstiiinnn')
        user_4 = User(netid='fawaza', email='fawaza@princeton.edu',
                      first_name='Fawaz', last_name='Ahmad',
                      display_name='Fawwaaazzz')

        db.session.add(user_1)
        db.session.add(user_2)
        db.session.add(user_3)
        db.session.add(user_4)

        # create widgets
        widget_1 = Widget(name = 'Ziv Widget', description = '')
        widget_2 = Widget(name = 'Ryan Widget', description = 'Just for Ziv')
        widget_3 = Widget(name = '-------', description = '')

        db.session.add(widget_1)
        db.session.add(widget_2)
        db.session.add(widget_3)

        # create subscriptions
        subscription_1 = Subscription(user=user_1, widget=widget_1, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})

        subscription_2 = Subscription(user=user_2, widget=widget_2, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})
        subscription_3 = Subscription(user=user_2, widget=widget_3, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})

        subscription_4 = Subscription(user=user_3, widget=widget_3, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})

        subscription_5 = Subscription(user=user_4, widget=widget_3, grid_location={'x': 0, 'y': 0, 'width': 6, 'height': 2})

        db.session.add(subscription_1)
        db.session.add(subscription_2)
        db.session.add(subscription_3)
        db.session.add(subscription_4)
        db.session.add(subscription_5)

        # manage admins
        widget_1.admins.append(user_1)
        widget_2.admins.append(user_2)
        widget_3.admins.append(user_3)


        post_1 = Post(content='This is a post!', author=user_1, widget=widget_1)
        post_2 = Post(content='This is another post!', author=user_2, widget=widget_2)

        db.session.add(post_1)
        db.session.add(post_2)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_getAllUsers(self):
        users = User.query.all()
        assert len(users) == 4

    def test_getUser(self):
        user = User.query.filter_by(netid='zbatscha').first()
        assert user.email == 'zbatscha@princeton.edu'

    def test_updateUserEmail(self):
        user = User.query.filter_by(netid='zbatscha').first()
        user.email = 'test@gmail.com'
        db.session.commit()

        user = User.query.filter_by(netid='zbatscha').first()
        assert user.email == 'test@gmail.com'

    def test_deleteUserMem(self):
        # delete user loaded from memory, check if user deleted
        user = User.query.filter_by(netid='zbatscha').first()
        db.session.delete(user)
        db.session.commit()
        user = User.query.filter_by(netid='zbatscha').first()
        assert not user

        # check that administrators table reflects removed association
        widget_admin = AdminAssociation.query.filter_by(user_id=1).all()
        assert not widget_admin

        # check that subscriptions table reflects removed association
        subscriptions = Subscription.query.filter_by(user_id=1).first()
        assert not subscriptions

        # check that posts table reflects removed association
        posts = Post.query.filter_by(author_id=1).first()
        assert not posts

        # check that all widgets remain
        widgets = Widget.query.all()
        assert len(widgets) == 3

    def test_deleteUserDB(self):
        # delete user directly from db, check if user deleted
        db.session.query(User).filter(User.id==1).delete()
        db.session.commit()
        user = User.query.filter_by(netid='zbatscha').first()
        assert not user

        # check that administrators table reflects removed association
        widget_admin = AdminAssociation.query.filter_by(user_id=1).all()
        assert not widget_admin

        # check that subscriptions table reflects removed association
        subscriptions = Subscription.query.filter_by(user_id=1).first()
        assert not subscriptions

        # check that posts table reflects removed association
        posts = Post.query.filter_by(author_id=1).first()
        assert not posts

        # check that all widgets remain
        widgets = Widget.query.all()
        assert len(widgets) == 3

    def test_getWidgetAdmins(self):
        widget_admins = Widget.query.filter_by(name='Ziv Widget').first().admins
        assert len(widget_admins) == 1

    def test_getAdministeredWidgets(self):
        user_admin_widgets = User.query.filter_by(netid='zbatscha').first().widgets_admin
        assert len(user_admin_widgets) == 1
        assert user_admin_widgets[0].name == 'Ziv Widget'

    def test_deleteWidgetMem(self):
        widget = Widget.query.filter_by(name='Ziv Widget').first()
        db.session.delete(widget)
        db.session.commit()

        # ensure no users were deleted
        users = User.query.all()
        assert len(users) == 4

        # ensure that all posts were deleted
        posts = Post.query.filter_by(widget_id=1).all()
        assert not posts

        # ensure that all subscriptions were deleted
        all_subscriptions = Subscription.query.all()
        for sub in all_subscriptions:
            assert sub.widget_id != 1

        # ensure that all admin associations were deleted
        all_admin_associations = AdminAssociation.query.all()
        for admin_association in all_admin_associations:
            assert admin_association.widget_id != 1

    def test_deleteWidgetDB(self):
        db.session.query(Widget).filter(Widget.id==1).delete()
        db.session.commit()

        # ensure no users were deleted
        users = User.query.all()
        assert len(users) == 4

        # ensure that all posts were deleted
        posts = Post.query.filter_by(widget_id=1).all()
        assert not posts

        # ensure that all subscriptions were deleted
        all_subscriptions = Subscription.query.all()
        for sub in all_subscriptions:
            assert sub.widget_id != 1

        # ensure that all admin associations were deleted
        all_admin_associations = AdminAssociation.query.all()
        for admin_association in all_admin_associations:
            assert admin_association.widget_id != 1

    def test_getSubscriptions(self):
        user = User.query.filter_by(netid='zbatscha').first()
        subscriptions = user.subscriptions
        assert len(subscriptions) == 1

    def test_updateSubscription(self):
        subscription = Subscription.query.filter_by(user_id=1).filter_by(widget_id=1).first()
        subscription.grid_location = {'x': 0, 'y': 10, 'width': 3, 'height': 2}
        db.session.commit()

    def test_deleteSubscription(self):
        user = User.query.filter_by(netid='zbatscha').first()
        widget = Widget.query.filter_by(name='Prospect Ave').first()
        subscriptions = Subscription.query.filter_by(user_id=user.id).filter_by(widget=widget).all()
        for sub in subscriptions:
            db.session.delete(sub)
        db.session.commit()

        # check that user was not deleted
        user = User.query.filter_by(netid='zbatscha').first()
        assert user

        # note!! removing subscription does not update admin association or posts made by that user


    def test_removeWidgetAdminMem(self):
        admin = AdminAssociation.query.filter_by(user_id=1).filter_by(widget_id=1).first()
        # print(admin)
        db.session.delete(admin)
        db.session.commit()

        # note!! removing admin does not remove posts made by that user, thats likely a good thing

        widget_admins = Widget.query.filter_by(name='Ziv Widget').first().admins
        assert len(widget_admins) == 0

    def test_getPosts(self):
        # by user
        user = User.query.filter_by(netid='zbatscha').first()
        assert user.posts.first().content == 'This is a post!'
        # by widget
        widget = Widget.query.filter_by(name='Ziv Widget').first()
        assert widget.posts.first().content == 'This is a post!'

    def test_createUserExist(self):
        user = user_utils.createUser('cl43')
        print(user)

    def test_createUserNotExist(self):
        user = user_utils.createUser('doesNotExist')
        print(user)
