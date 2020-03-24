# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:48:28 2020

@author: ryant
"""
from tangelo.models import Widget
from flask_login import UserMixin
from tangelo import db, login_manager

class generic():
    
    def __init__(self, title, descrip):
        self._innerWidget = Widget(name = title, description = descrip)
        self._author = db.session.query(User).filter(User.netid== current_user.netid)
        
        
    
    