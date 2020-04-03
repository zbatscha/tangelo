#!/usr/bin/env python

#-----------------------------------------------------------------------
# populate.py
#-----------------------------------------------------------------------
from tangelo.models import User, Widget, Subscription, Post, AdminAssociation
from users import getUndergraduates

# for ugrad in undergraduates:
undergraduates = getUndergraduates()
test = undergraduates[0]
print(test['first_name'], test['last_name'], test['net_id'], test['email'])
