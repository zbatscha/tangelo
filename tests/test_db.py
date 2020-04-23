#!/usr/bin/env python

#-----------------------------------------------------------------------
# test_db.py
#-----------------------------------------------------------------------

import unittest
from tangelo.models import User, Widget, Subscription, Post, AdminAssociation
import tangelo.user_utils as user_utils
from news_collector import news_object 
from tangelo.WHO_RSS import covid_data
from tangelo import app, db
import sys
import os

#-----------------------------------------------------------------------

class DBTest(unittest.TestCase):

    def create_app(self):
        # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        return app

    def setUp(self):
        db.drop_all()
        db.create_all()

        # create users
        # user_1 = User(netid='zbatscha', email='zbatscha@princeton.edu',
        #               first_name='Ziv', last_name='Batscha',
        #               display_name='this_is_my_display_name')
        # user_2 = User(netid='rmthorpe', email='rmthorpe@princeton.edu',
        #               first_name='Ryan', last_name='Thorpe',
        #               display_name='Ryyyaaannn')
        # user_3 = User(netid='almejia', email='almejia@princeton.edu',
        #               first_name='Austin', last_name='Mejia',
        #               display_name='Auuuussstiiinnn')
        # user_4 = User(netid='fawaza', email='fawaza@princeton.edu',
        #               first_name='Fawaz', last_name='Ahmad',
        #               display_name='Fawwaaazzz')
        # user_5 = User(netid='josephoe', email='josephoe@princeton.edu',
        #               first_name='Joseph', last_name='Eichenhofer',
        #               display_name='Joseph')
        # user_6 = User(netid='rdondero', email='rdondero@cs.princeton.edu',
        #               first_name='Robert', last_name='Dondero',
        #               display_name='Professor Dondero')

        # db.session.add(user_1)
        # db.session.add(user_2)
        # db.session.add(user_3)
        # db.session.add(user_4)
        # db.session.add(user_5)
        # db.session.add(user_6)

        # create widgets

        # widget_1 = Widget(name = 'Ziv Thoughts.', description = '')
        widget_1 = Widget(name = "Welcome to Tangelo", description = "")
        # widget_2 = Widget(name = 'Ryan\'s Isolation Song of the Day', description = 'Just for Ziv')
        # widget_3 = Widget(name = 'How styling king saves the day', description = '')
        # widget_4 = Widget(name = 'My favorite fruit of the hour, by Fawaz', description = '')
        # widget_5 = Widget(name = 'Saturday Drawful Nights', description = '8pm every friday, zoom in.')
        # widget_6 = Widget(name = 'An A+ for Tangelo?', description = 'Help us')
        # widget_7 = Widget(name = 'Prospect Ave', description = 'Open clubs')
        # widget_8 = Widget(name = 'Princeton News', description = 'Life at Princeton Updates')
        # widget_9 = Widget(name = 'Tangelo Zoom Room', description = '')
        widget_10 = Widget(name = 'Clock', description = '', style='<link rel=\\"stylesheet\\" href=\\"../static/clock.css\\"/><script type=\\"text/javascript\\" src=\\"../static/clock.js\\"></script><div id=\\"centerPanelClock\\"><h1 id=\\"time\\"></h1><br><h1 id = \\"date\\"></h1></div>')
        widget_11 = Widget(name = 'Weather', description = '', style='<link rel=\\"stylesheet\\" href=\\"../static/weather.css\\"/><script type=\\"text/javascript\\" src=\\"../static/weather.js\\"></script><div id=\\"centerPanelWeather\\"><h1 id=\\"temperature\\">One moment, we\'re getting some weathery goodness</h1><h1 id=\\"sky\\"></h1></div>')

        news = news_object()
        title = news.titles()[0]
        author = news.source()[0]
        url = news.urls()[0]
        widget_12 = Widget(name = 'News', description = "Headlines for the Day", style='<link rel=\\"stylesheet\\" href=\\"../static/genericWidget.css\\"/><div class=\\"centerPanelWidget\\"><h3 class = \\"genericTitle\\"><center>News</center></h3><hr class = \\"genericDivider\\"><div class = \\"GenericPost\\"><a class = \\"GenericPoster\\">@'+author+'</a>'+title+'</div><a href='+url+'>Click here for more information</a></div>')

        us_data = covid_data("US")
        outputString = us_data.number_day_decreasing_confirmed()
        widget_13 = Widget(name = 'Covid-19 Case Number Update', description="Tracks the number of new COVID-19 Cases Everyday", style='<link rel=\\"stylesheet\\" href=\\"../static/genericWidget.css\\"/><div class=\\"centerPanelWidget\\"><h3 class = \\"genericTitle\\"><center>Covid-19 Case Number Update</center></h3><hr class = \\"genericDivider\\"><div class = \\"GenericPost\\"><a class = \\"GenericPoster\\">@Johns Hopkins CSSE</a>'+outputString+'</div>')
        db.session.add(widget_13)
        # # widget_1.admins.append(user_1)
        # widget_2.admins.append(user_2)
        # widget_3.admins.append(user_3)
        # widget_4.admins.append(user_4)
        # widget_7.admins.append(user_3)
        #
        db.session.add(widget_1)
        # db.session.add(widget_2)
        # db.session.add(widget_3)
        # db.session.add(widget_4)
        # db.session.add(widget_5)
        # db.session.add(widget_6)
        # db.session.add(widget_7)
        # db.session.add(widget_8)
        # db.session.add(widget_9)
        db.session.add(widget_10)
        db.session.add(widget_11)
        db.session.add(widget_12)

        # # create subscriptions
        # # subscription_1 = Subscription(user=user_1, widget=widget_1, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})
        # # subscription_2 = Subscription(user=user_1, widget=widget_2, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})
        # # subscription_3 = Subscription(user=user_1, widget=widget_3, grid_location={'x': 0, 'y': 0, 'width': 6, 'height': 2})
        #
        # subscription_4 = Subscription(user=user_2, widget=widget_1, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})
        # subscription_5 = Subscription(user=user_2, widget=widget_2, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})
        # subscription_6 = Subscription(user=user_2, widget=widget_3, grid_location={'x': 0, 'y': 0, 'width': 6, 'height': 2})
        #
        # subscription_7 = Subscription(user=user_3, widget=widget_1, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})
        # subscription_8 = Subscription(user=user_3, widget=widget_2, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})
        # subscription_9 = Subscription(user=user_3, widget=widget_3, grid_location={'x': 0, 'y': 0, 'width': 6, 'height': 2})
        #
        # subscription_10 = Subscription(user=user_4, widget=widget_1, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})
        # subscription_11 = Subscription(user=user_4, widget=widget_2, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})
        # subscription_12 = Subscription(user=user_4, widget=widget_3, grid_location={'x': 0, 'y': 0, 'width': 6, 'height': 2})
        #
        # subscription_13 = Subscription(user=user_5, widget=widget_1, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})
        # subscription_14 = Subscription(user=user_5, widget=widget_2, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})
        # subscription_15 = Subscription(user=user_5, widget=widget_3, grid_location={'x': 0, 'y': 0, 'width': 6, 'height': 2})
        #
        # subscription_16 = Subscription(user=user_6, widget=widget_1, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})
        # subscription_17 = Subscription(user=user_6, widget=widget_2, grid_location={'x': 6, 'y': 0, 'width': 6, 'height': 2})
        # subscription_18 = Subscription(user=user_6, widget=widget_3, grid_location={'x': 0, 'y': 0, 'width': 6, 'height': 2})
        #
        #
        # # db.session.add(subscription_1)
        # # db.session.add(subscription_2)
        # # db.session.add(subscription_3)
        # db.session.add(subscription_4)
        # db.session.add(subscription_5)
        # db.session.add(subscription_6)
        # db.session.add(subscription_7)
        # db.session.add(subscription_8)
        # db.session.add(subscription_9)
        # db.session.add(subscription_10)
        # db.session.add(subscription_11)
        # db.session.add(subscription_12)
        # db.session.add(subscription_13)
        # db.session.add(subscription_14)
        # db.session.add(subscription_15)
        # db.session.add(subscription_16)
        # db.session.add(subscription_17)
        # db.session.add(subscription_18)
        #
        # post_1 = Post(content='THIS THURSDAY, FRIDAY, AND SATURDAY COME SEE MY DANCE SHOW!!! I\'m only in it for 1 piece but I will definitely evaluate our friendship on it :)', author=user_3, widget=widget_7)
        # # post_2 = Post(content='I wanna do a cartwheel. But real casual like. Not enough to make a big deal out of it, but I know everyone saw it. One stunning, gorgeous cartwheel.', author=user_1, widget=widget_1)
        #
        # db.session.add(post_1)
        # # db.session.add(post_2)
        user_1 = User(netid='tangelo')
        widget_1.admins.append(user_1)
        widget_10.admins.append(user_1)
        widget_11.admins.append(user_1)
        post_1 = Post(content='We\'re glad you\'re here.', author=user_1, widget=widget_1)

        db.session.add(user_1)
        db.session.add(post_1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        # db.drop_all()
        # db.create_all()

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
        assert len(widgets) == 9

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
        assert len(widgets) == 9

    def test_getWidgetAdmins(self):
        widget_admins = Widget.query.filter_by(name='Prospect Ave').first().admins
        assert len(widget_admins) == 1

    def test_getAdministeredWidgets(self):
        user_admin_widgets = User.query.filter_by(netid='zbatscha').first().widgets_admin
        assert len(user_admin_widgets) == 1
        assert user_admin_widgets[0].name == 'www.creedthoughts.gov.www/creedthoughts.'

    def test_deleteWidgetMem(self):
        widget = Widget.query.filter_by(name='Prospect Ave').first()
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
        subscriptions = user.subscriptions
        assert len(subscriptions) == 3

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

        widget_admins = Widget.query.filter_by(name='Prospect Ave').first().admins
        assert len(widget_admins) == 2

    def test_getPosts(self):
        # by user
        user = User.query.filter_by(netid='zbatscha').first()
        assert user.posts.first().content == 'My First Post!'
        # by widget
        widget = Widget.query.filter_by(name='Prospect Ave').first()
        assert widget.posts.first().content == 'My First Post!'

    def test_createUser(self):
        user = user_utils.createUser('cl43')
        print(user)
        user = user_utils.createUser('doesNotExist')
        print(user)
