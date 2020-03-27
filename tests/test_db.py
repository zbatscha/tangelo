#!/usr/bin/env python

#-----------------------------------------------------------------------
# test_db.py
#-----------------------------------------------------------------------

import unittest
from tangelo.models import User, Widget, Subscription, Post
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

        db.session.add(widget_1)
        db.session.add(widget_2)
        db.session.add(widget_3)
        db.session.add(widget_4)

        # create subscriptions

        subscription_1 = Subscription(user=user_1, widget=widget_1, admin=False, grid_row=2, grid_col=1)
        subscription_2 = Subscription(user=user_1, widget=widget_2, admin=False, grid_row=0, grid_col=2)
        subscription_3 = Subscription(user=user_2, widget=widget_2, admin=False, grid_row=0, grid_col=0)
        subscription_4 = Subscription(user=user_2, widget=widget_3, admin=True, grid_row=1, grid_col=0)
        subscription_5 = Subscription(user=user_3, widget=widget_2, admin=False, grid_row=1, grid_col=1)
        subscription_6 = Subscription(user=user_3, widget=widget_4, admin=True, grid_row=0, grid_col=1)
        subscription_7 = Subscription(user=user_4, widget=widget_1, admin=True, grid_row=0, grid_col=1)
        subscription_8 = Subscription(user=user_4, widget=widget_2, admin=False, grid_row=1, grid_col=0)
        subscription_9 = Subscription(user=user_5, widget=widget_4, admin=False, grid_row=0, grid_col=1)
        subscription_10 = Subscription(user=user_5, widget=widget_3, admin=False, grid_row=1, grid_col=0)
        subscription_11 = Subscription(user=user_6, widget=widget_3, admin=False, grid_row=0, grid_col=1)
        subscription_12 = Subscription(user=user_6, widget=widget_4, admin=False, grid_row=1, grid_col=0)

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


        post_1 = Post(title='My First Post!', body='Did this work?', author=user_1, widget=widget_1)
        db.session.add(post_1)

        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

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

    def test_deleteUser(self):
        # check if user deleted
        user = User.query.filter_by(netid='zbatscha').first()
        db.session.delete(user)
        db.session.commit()
        user = User.query.filter_by(netid='zbatscha').first()
        assert not user
        # once user deleted, check that subscriptions are also deleted
        subscriptions = Subscription.query.all()
        for sub in subscriptions:
            if sub.user.netid == 'zbatscha':
                raise Exception('Subscriptions should also be deleted')

    def test_getSubscriptions(self):
        user = User.query.filter_by(netid='zbatscha').first()
        subscription = Subscription.query.filter_by(user=user).all()
        assert len(subscription) == 2

    def test_deleteSubscription(self):
        user = User.query.filter_by(netid='zbatscha').first()
        widget = Widget.query.filter_by(name='Prospect').first()
        subscription = Subscription.query.filter_by(user=user).filter_by(widget=widget).all()
        for sub in subscription:
            db.session.delete(sub)
        db.session.commit()
        user = User.query.filter_by(netid='zbatscha').first()
        assert user

    def test_updateWidgetAdmin(self):
        user = User.query.filter_by(netid='zbatscha').first()
        widget = Widget.query.filter_by(name='Prospect').first()
        subscription = Subscription.query.filter_by(user=user).filter_by(widget=widget).all()
        assert len(subscription) == 1
        sub = subscription[0]
        assert sub.admin == False
        sub.admin = True
        db.session.commit()
        user = User.query.filter_by(netid='zbatscha').first()
        widget = Widget.query.filter_by(name='Prospect').first()
        subscription = Subscription.query.filter_by(user=user).filter_by(widget=widget).first()
        assert subscription.admin

    def test_getPosts(self):
        # by user
        user = User.query.filter_by(netid='zbatscha').first()
        assert user.posts.first().title == 'My First Post!'
        # by widget
        widget = Widget.query.filter_by(name='Prospect').first()
        assert widget.posts.first().title == 'My First Post!'

        # by user, delete user, post still there?
