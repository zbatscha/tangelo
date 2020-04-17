#!/usr/bin/env python

"""
Provides methods to perform a request to the tigerbook API to query a Princeton
undergrad by netid.
"""

import hashlib
import random
import requests
import json
from base64 import b64encode
from datetime import datetime
import os
from tangelo.models import User
from tangelo import db
from sys import stderr

def generateHeaders():
    created = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    nonce = ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(32)])
    nonce_bytes = b64encode(bytes(nonce, 'ascii')).decode()

    username = os.environ.get('TIGERBOOK_USERNAME') # use your own netid
    password = os.environ.get('TIGERBOOK_KEY') # use your own from /getkey
    if not username or not password:
        raise Exception('Missing tigerbook key and/or username')
    password_digest = (nonce + created + password).encode('ascii')
    generated_digest = b64encode(hashlib.sha256(password_digest).digest()).decode()
    headers = {
        'Authorization': 'WSSE profile="UsernameToken"',
        'X-WSSE': f'UsernameToken Username="{username}", PasswordDigest="{generated_digest}", Nonce="{nonce_bytes}", Created="{created}"'
    }
    return headers

def getUndergraduate(netid):
    url = 'https://tigerbook.herokuapp.com/api/v1/undergraduates'
    url = os.path.join(url, netid)
    headers = generateHeaders()
    try:
        response = requests.get(
            url=url,
            headers=headers)
        response.raise_for_status()
        undergrad = json.loads(response.content)
        return undergrad
    except requests.exceptions.HTTPError as err:
        print(err)
        return None

def createUser(netid):
    new_user = User(netid=netid)
    undergrad_profile = getUndergraduate(netid)
    if undergrad_profile:
        new_user = User(netid=netid, email=undergrad_profile.get('email'),
                        first_name=undergrad_profile.get('first_name'),
                        last_name=undergrad_profile.get('last_name'),
                        class_year=undergrad_profile.get('class_year'))

    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()
        raise Exception(f'Failed to create user with netid = {netid}') from e

if __name__=="__main__":
    undergrad_profile = getUndergraduate(netid)
    print(undergrad_profile)
    print(undergrad_profile.get('net_id'), undergrad_profile.get('first_name'), undergrad_profile.get('last_name'), undergrad_profile.get('class_year'), undergrad_profile.get('email'))
    undergrad_profile = getUndergraduate('notUndergraduate')
    print(undergrad_profile)

    user = createUser('zbatscha')
    print(user)
