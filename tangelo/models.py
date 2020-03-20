#!/usr/bin/env python

#-----------------------------------------------------------------------
# models.py
#-----------------------------------------------------------------------

from tangelo import db

#-----------------------------------------------------------------------

class User(db.Model):
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
