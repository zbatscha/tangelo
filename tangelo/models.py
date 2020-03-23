#!/usr/bin/env python

#-----------------------------------------------------------------------
# models.py
#-----------------------------------------------------------------------

from tangelo import db, login_manager
from flask_login import UserMixin
from tangelo.models_service import JSONEncodedDict
from datetime import datetime

#-----------------------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    middle_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120), nullable=False)
    display_name = db.Column(db.String(30), default='')
    create_dttm = db.Column(db.DateTime, default=datetime.utcnow)
    widgets = db.relationship("Widget", secondary="subscriptions")
    # posts = db.relationship("Widget", secondary="posts")
    # posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.netid}')"

class Widget(db.Model):
    __tablename__ = 'widgets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text)
    create_dttm = db.Column(db.DateTime, default=datetime.utcnow)
    users = db.relationship("User", secondary="subscriptions")
    # posts = db.relationship("Post", secondary="posts")
    #posts = db.relationship('Post', backref='widget', lazy=True)

    def __repr__(self):
        return f"Widget('{self.name}', '{self.description}')"

class Subscription(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id'))
    create_dttm = db.Column(db.DateTime, default=datetime.utcnow)
    admin = db.Column(db.Boolean, unique=False, default=False)
    grid_row = db.Column(db.Integer, nullable=False)
    grid_col = db.Column(db.Integer, nullable=False)

    user = db.relationship(User, backref=db.backref("subscriptions", cascade="all, delete-orphan"))
    widget = db.relationship(Widget, backref=db.backref("subscriptions", cascade="all, delete-orphan"))

    __mapper_args__ = {
        'confirm_deleted_rows' : False
    }

    def __repr__(self):
        return f"Subscription('{self.user}', '{self.widget}')"

# class Post(db.Model):
#     __tablename__ = 'posts'
#     id = db.Column(db.Integer, primary_key=True)
#     author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id'), nullable=False)
#     title = db.Column(db.String(120), nullable=False)
#     content = db.Column(db.Text, nullable=True)
#     create_dttm = db.Column(db.DateTime, default=datetime.utcnow)
#
#     author = db.relationship(User, backref=db.backref("posts", cascade="all, delete-orphan"))
#     widget = db.relationship(Widget, backref=db.backref("posts", cascade="all, delete-orphan"))
#
#
#     def __repr__(self):
#         return f"Post('{self.title}', '{self.date_posted}')"


# db.drop_all()
# db.create_all()
# user_1 = User(netid='zbatscha', email='zbatscha@princeton.edu',
#               first_name='Ziv', middle_name='Haim', last_name='Batscha',
#               display_name='this_is_my_display_name')
# user_2 = User(netid='rmthorpe', email='rmthorpe@princeton.edu',
#               first_name='Ryan', middle_name='', last_name='Thorpe',
#               display_name='Ryyyaaannn')
# user_3 = User(netid='almejia', email='almejia@princeton.edu ',
#               first_name='Austin', middle_name='', last_name='Mejia',
#               display_name='Auuuussstiiinnn')
# user_4 = User(netid='fawaza', email='fawaza@princeton.edu',
#               first_name='Fawaz', middle_name='', last_name='Ahmad',
#               display_name='Fawwaaazzz')
# db.session.add(user_1)
# db.session.add(user_2)
# db.session.add(user_3)
# db.session.add(user_4)
#
# widget_1 = Widget(name = 'Prospect', description = 'Open clubs')
# widget_2 = Widget(name = 'Dhall', description = 'Today\'s Entrees')
# widget_3 = Widget(name = 'Umbrella', description = 'Yes/No')
# widget_4 = Widget(name = 'Princeton News', description = 'Life at Princeton Updates')
#
# db.session.add(widget_1)
# db.session.add(widget_2)
# db.session.add(widget_3)
# db.session.add(widget_4)
#
# subscription_1 = Subscription(user=user_1, widget=widget_1, admin=True, grid_row=2, grid_col=1)
# subscription_2 = Subscription(user=user_1, widget=widget_2, admin=False, grid_row=0, grid_col=2)
# subscription_3 = Subscription(user=user_2, widget=widget_2, admin=False, grid_row=0, grid_col=0)
# subscription_4 = Subscription(user=user_2, widget=widget_3, admin=True, grid_row=1, grid_col=0)
# subscription_5 = Subscription(user=user_3, widget=widget_2, admin=False, grid_row=1, grid_col=1)
# subscription_6 = Subscription(user=user_3, widget=widget_4, admin=True, grid_row=0, grid_col=1)
# subscription_7 = Subscription(user=user_4, widget=widget_1, admin=True, grid_row=0, grid_col=1)
# subscription_8 = Subscription(user=user_4, widget=widget_2, admin=False, grid_row=1, grid_col=0)
#
# db.session.add(subscription_1)
# db.session.add(subscription_2)
# db.session.add(subscription_3)
# db.session.add(subscription_4)
# db.session.add(subscription_5)
# db.session.add(subscription_6)
# db.session.add(subscription_7)
# db.session.add(subscription_8)
#
# db.session.commit()
#
# #user = db.session.query(User).filter(User.netid=='zbatscha').first()
# #db.session.delete(user)
#
# # widget = db.session.query(Widget).filter(Widget.name=='Prospect').first()
# # db.session.delete(widget)
# # db.session.commit()


all_users = User.query.all()
for us in all_users:
    print(us, ':')
    for sub in us.subscriptions:
        print(sub.widget, f'Grid_Row: {sub.grid_row}', f'Grid_Col: {sub.grid_col}', f'Admin: {sub.admin}')

all_widgets = Widget.query.all()
for w in all_widgets:
    print(w, w.users)
