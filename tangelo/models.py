#!/usr/bin/env python

#-----------------------------------------------------------------------
# models.py
#-----------------------------------------------------------------------

from tangelo import db, login_manager
from flask_login import UserMixin

#-----------------------------------------------------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    netid = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    middle_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120), nullable=False)
    display_name = db.Column(db.String(30), default='')
    displayed_widgets = db.Column(db.JSON, nullable=True)
    admin_widgets = db.Column(db.ARRAY(db.Integer), nullable=True)

    def __repr__(self):
        return f"User('{self.netid}', '{self.display_name}')"


#-----------------------------------------------------------------------
"""
Initial Testing Data
"""
db.drop_all()
db.create_all()
user_1 = User(netid='zbatscha', email='zbatscha@princeton.edu',
              first_name='Ziv', middle_name='Haim', last_name='Batscha',
              display_name='this_is_my_display_name', displayed_widgets={100: (0, 0), 101: (0, 1)}, admin_widgets=[100, 101])
user_2 = User(netid='rmthorpe', email='rmthorpe@princeton.edu',
              first_name='Ryan', middle_name='', last_name='Thorpe',
              display_name='Ryyyaaannn', displayed_widgets={100: (0, 0), 101: (0, 1), 110: (2,1)}, admin_widgets=[101,110])
user_3 = User(netid='almejia', email='almejia@princeton.edu ',
              first_name='Austin', middle_name='', last_name='Mejia',
              display_name='Auuuussstiiinnn', displayed_widgets={101: (0, 0), 100: (0, 1), 110: (1,1), 105: (2,0)}, admin_widgets=[100,105])
user_4 = User(netid='fawaza', email='fawaza@princeton.edu',
              first_name='Fawaz', middle_name='', last_name='Ahmad',
              display_name='Fawwaaazzz', displayed_widgets={101: (0, 0), 100: (0, 1), 106: (1,1), 105: (2,0)}, admin_widgets=[101,106])
db.session.add(user_1)
db.session.add(user_2)
db.session.add(user_3)
db.session.add(user_4)
db.session.commit()
