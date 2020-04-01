#!/usr/bin/env python

#-----------------------------------------------------------------------
# test_db.py
#-----------------------------------------------------------------------

import unittest
from tangelo.models import User, Widget, Subscription, Post, AdminAssociation
from tangelo import app, db

#-----------------------------------------------------------------------

POSTGRES_URL="127.0.0.1:5432"
POSTGRES_DB="tangelo_test"
POSTGRES_USER="postgres"
POSTGRES_PW="password"
TEST_SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2:// \
    {user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW,
                                    url=POSTGRES_URL, db=POSTGRES_DB)

class DBTest(unittest.TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = TEST_SQLALCHEMY_DATABASE_URI
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()
        # create users

        user_1 = User(netid='zbatscha', email='zbatscha@princeton.edu',
                      first_name='Ziv', middle_name='Haim', last_name='Batscha',
                      display_name='this_is_my_display_name')
        user_2 = User(netid='rmthorpe', email='rmthorpe@princeton.edu',
                      first_name='Ryan', middle_name='', last_name='Thorpe',
                      display_name='Ryyyaaannn')
        user_3 = User(netid='almejia', email='almejia@princeton.edu',
                      first_name='Austin', middle_name='', last_name='Mejia',
                      display_name='Auuuussstiiinnn')
        user_4 = User(netid='fawaza', email='fawaza@princeton.edu',
                      first_name='Fawaz', middle_name='', last_name='Ahmad',
                      display_name='Fawwaaazzz')
        user_5 = User(netid='josephoe', email='josephoe@princeton.edu',
                      first_name='Joseph', middle_name='', last_name='Eichenhofer',
                      display_name='Joseph')
        user_6 = User(netid='rdondero', email='rdondero@cs.princeton.edu',
                      first_name='Robert', middle_name='', last_name='Dondero',
                      display_name='Professor Dondero')

        db.session.add(user_1)
        db.session.add(user_2)
        db.session.add(user_3)
        db.session.add(user_4)
        db.session.add(user_5)
        db.session.add(user_6)

        # create widgets

        widget_1 = Widget(name = 'Prospect', description = 'Open clubs')
        widget_2 = Widget(name = 'Dhall', description = 'Today\'s Entrees')
        widget_3 = Widget(name = 'Umbrella', description = 'Yes/No')
        widget_4 = Widget(name = 'Princeton News', description = 'Life at Princeton Updates')

        widget_1.admins.append(user_1)
        widget_1.admins.extend([user_2, user_3])

        db.session.add(widget_1)
        db.session.add(widget_2)
        db.session.add(widget_3)
        db.session.add(widget_4)

        # create subscriptions
        subscription_1 = Subscription(user=user_1, widget=widget_1, grid_location={'row': 2, 'col': 1})
        subscription_2 = Subscription(user=user_1, widget=widget_2, grid_location={'row': 2, 'col': 1})
        subscription_3 = Subscription(user=user_2, widget=widget_2, grid_location={'row': 2, 'col': 1})
        subscription_4 = Subscription(user=user_2, widget=widget_3, grid_location={'row': 2, 'col': 1})
        subscription_5 = Subscription(user=user_3, widget=widget_2, grid_location={'row': 2, 'col': 1})
        subscription_6 = Subscription(user=user_3, widget=widget_4, grid_location={'row': 2, 'col': 1})
        subscription_7 = Subscription(user=user_4, widget=widget_1, grid_location={'row': 2, 'col': 1})
        subscription_8 = Subscription(user=user_4, widget=widget_2, grid_location={'row': 2, 'col': 1})
        subscription_9 = Subscription(user=user_5, widget=widget_4, grid_location={'row': 2, 'col': 1})
        subscription_10 = Subscription(user=user_5, widget=widget_3, grid_location={'row': 2, 'col': 1})
        subscription_11 = Subscription(user=user_6, widget=widget_3, grid_location={'row': 2, 'col': 1})
        subscription_12 = Subscription(user=user_6, widget=widget_4, grid_location={'row': 2, 'col': 1})

        db.session.add(subscription_1)
        db.session.add(subscription_2)
        db.session.add(subscription_3)
        db.session.add(subscription_4)
        db.session.add(subscription_5)
        db.session.add(subscription_6)
        db.session.add(subscription_7)
        db.session.add(subscription_8)
        db.session.add(subscription_9)
        db.session.add(subscription_10)
        db.session.add(subscription_11)
        db.session.add(subscription_12)

        post_1 = Post(content='My First Post!', author=user_1, widget=widget_1)
        post_2 = Post(content='Our Second Post!', author=user_2, widget=widget_1)

        db.session.add(post_1)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        # db.drop_all()

    def test_getAllUsers(self):
        users = User.query.all()
        assert len(users) == 6

    def test_getUser(self):
        user = User.query.filter_by(netid='rdondero').first()
        assert user.email == 'rdondero@cs.princeton.edu'

    def test_updateUserEmail(self):
        user = User.query.filter_by(netid='rdondero').first()
        user.email = 'test@gmail.com'
        db.session.commit()

        user = User.query.filter_by(netid='rdondero').first()
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
        assert len(widgets) == 4

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
        assert len(widgets) == 4

    def test_getWidgetAdmins(self):
        widget_admins = Widget.query.filter_by(name='Prospect').first().admins
        assert len(widget_admins) == 3

    def test_getAdministeredWidgets(self):
        user_admin_widgets = User.query.filter_by(netid='zbatscha').first().widgets_admin
        assert len(user_admin_widgets) == 1
        assert user_admin_widgets[0].name == 'Prospect'

    def test_deleteWidgetMem(self):
        widget = Widget.query.filter_by(name='Prospect').first()
        db.session.delete(widget)
        db.session.commit()

        # ensure no users were deleted
        users = User.query.all()
        assert len(users) == 6

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
        assert len(users) == 6

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
        subscription = Subscription.query.filter_by(user=user).all()
        assert len(subscription) == 2

    def test_deleteSubscription(self):
        user = User.query.filter_by(netid='zbatscha').first()
        widget = Widget.query.filter_by(name='Prospect').first()
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

        widget_admins = Widget.query.filter_by(name='Prospect').first().admins
        assert len(widget_admins) == 2

    def test_getPosts(self):
        # by user
        user = User.query.filter_by(netid='zbatscha').first()
        assert user.posts.first().content == 'My First Post!'
        # by widget
        widget = Widget.query.filter_by(name='Prospect').first()
        assert widget.posts.first().content == 'My First Post!'
