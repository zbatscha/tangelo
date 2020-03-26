from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, Boolean

POSTGRES_URL="127.0.0.1:5432"
POSTGRES_DB="tangelo_test"
# POSTGRES_USER="postgres"
# POSTGRES_PW="password"
# DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
DB_URL = 'postgresql+psycopg2://{url}/{db}'.format(url=POSTGRES_URL,db=POSTGRES_DB)

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
user_3 = User(netid='almejia', email='almejia@princeton.edu ',
              first_name='Austin', middle_name='', last_name='Mejia',
              display_name='Auuuussstiiinnn')
user_4 = User(netid='fawaza', email='fawaza@princeton.edu',
              first_name='Fawaz', middle_name='', last_name='Ahmad',
              display_name='Fawwaaazzz')

session.add(user_1)
session.add(user_2)
session.add(user_3)
session.add(user_4)

widget_1 = Widget(name = 'Prospect', description = 'Open clubs')
widget_2 = Widget(name = 'Dhall', description = 'Today\'s Entrees')
widget_3 = Widget(name = 'Umbrella', description = 'Yes/No')
widget_4 = Widget(name = 'Princeton News', description = 'Life at Princeton Updates')

session.add(widget_1)
session.add(widget_2)
session.add(widget_3)
session.add(widget_4)

subscription_1 = Subscription(user=user_1, widget=widget_1, admin=True, grid_row=2, grid_col=1)
subscription_2 = Subscription(user=user_1, widget=widget_2, admin=False, grid_row=0, grid_col=2)
subscription_3 = Subscription(user=user_2, widget=widget_2, admin=False, grid_row=0, grid_col=0)
subscription_4 = Subscription(user=user_2, widget=widget_3, admin=True, grid_row=1, grid_col=0)
subscription_5 = Subscription(user=user_3, widget=widget_2, admin=False, grid_row=1, grid_col=1)
subscription_6 = Subscription(user=user_3, widget=widget_4, admin=True, grid_row=0, grid_col=1)
subscription_7 = Subscription(user=user_4, widget=widget_1, admin=True, grid_row=0, grid_col=1)
subscription_8 = Subscription(user=user_4, widget=widget_2, admin=False, grid_row=1, grid_col=0)

session.add(subscription_1)
session.add(subscription_2)
session.add(subscription_3)
session.add(subscription_4)
session.add(subscription_5)
session.add(subscription_6)
session.add(subscription_7)
session.add(subscription_8)

session.commit()

#user = session.query(User).filter(User.netid=='zbatscha').first()
#session.delete(user)

# widget = session.query(Widget).filter(Widget.name=='Prospect').first()
# session.delete(widget)
# session.commit()
'''
all_users = session.query(User)
for us in all_users:
    print(us, ':')
    for sub in us.subscriptions:
        print(sub.widget, f'Grid_Row: {sub.grid_row}', f'Grid_Col: {sub.grid_col}', f'Admin: {sub.admin}')
'''
all_widgets = session.query(Widget)
for w in all_widgets:
    for sub in w.subscriptions:
        print(w, sub.user, sub.admin)
