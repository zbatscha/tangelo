from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean

POSTGRES_URL="127.0.0.1:5432"
POSTGRES_DB="tangelo_test"
POSTGRES_USER="postgres"
POSTGRES_PW="password"
DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
# DB_URL = 'postgresql+psycopg2://{url}/{db}'.format(url=POSTGRES_URL,db=POSTGRES_DB)

db = create_engine(DB_URL)
base = declarative_base()

class User(base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    netid = Column(String(120), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    first_name = Column(String(120), nullable=False)
    middle_name = Column(String(120))
    last_name = Column(String(120), nullable=False)
    display_name = Column(String(30), default='')
    create_dttm = Column(DateTime, default=datetime.utcnow)
    widgets = relationship("Widget", secondary="subscriptions")
    # posts = relationship("Widget", secondary="posts")
    # posts = relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.netid}')"

class Widget(base):
    __tablename__ = 'widgets'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True, nullable=False)
    description = Column(Text)
    create_dttm = Column(DateTime, default=datetime.utcnow)
    creator = Column( Text, default="Tangelo_admin")
    users = relationship("User", secondary="subscriptions")
    # posts = relationship("Post", secondary="posts")
    #posts = relationship('Post', backref='widget', lazy=True)

    def __repr__(self):
        return f"Widget('{self.name}', '{self.description}')"

class Subscription(base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    widget_id = Column(Integer, ForeignKey('widgets.id'))
    create_dttm = Column(DateTime, default=datetime.utcnow)
    admin = Column(Boolean, unique=False, default=False)
    grid_row = Column(Integer, nullable=False)
    grid_col = Column(Integer, nullable=False)

    user = relationship(User, backref=backref("subscriptions", cascade="all, delete-orphan"))
    widget = relationship(Widget, backref=backref("subscriptions", cascade="all, delete-orphan"))

    __mapper_args__ = {
        'confirm_deleted_rows' : False
    }

    def __repr__(self):
        return f"Subscription('{self.user}', '{self.widget}')"

Session = sessionmaker(db)
session = Session()

base.metadata.drop_all(db)
base.metadata.create_all(db)

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

db.session.commit()

all_widgets = session.query(Widget)
for w in all_widgets:
    for sub in w.subscriptions:
        print(w, sub.user, sub.admin)
