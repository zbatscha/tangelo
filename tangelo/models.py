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
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.netid}')"

class Widget(db.Model):
    __tablename__ = 'widgets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True, nullable=False)
    description = db.Column(db.Text)
    create_dttm = db.Column(db.DateTime, default=datetime.utcnow)
    creator = db.Column(db.Text, default="Tangelo_admin")
    users = db.relationship("User", secondary="subscriptions")
    posts = db.relationship('Post', backref='widget', lazy='dynamic')

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

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    widget_id = db.Column(db.Integer, db.ForeignKey('widgets.id', ondelete='CASCADE'))
    title = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=True)
    create_dttm = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Post('{self.title}', '{self.body}', '{self.create_dttm}')"
