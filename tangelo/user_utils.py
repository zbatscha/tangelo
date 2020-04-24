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
from tangelo import log

#-----------------------------------------------------------------------

def generateHeaders():
    """
    Build a TigerBook API request header

    Parameters
    ----------
    None

    Returns
    -------
    dict
        TigerBook API authorization request header.

    """
    created = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    nonce = ''.join([random.choice('0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(32)])
    nonce_bytes = b64encode(bytes(nonce, 'ascii')).decode()

    username = 'rmthorpe'
    #os.environ.get('TIGERBOOK_USERNAME') # use your own netid
    password = 'd87d91d362c0c51262e276bec6ae8cd0'
    #os.environ.get('TIGERBOOK_KEY') # use your own from /getkey
    if not username or not password:
        raise Exception('Missing tigerbook key and/or username')
    password_digest = (nonce + created + password).encode('ascii')
    generated_digest = b64encode(hashlib.sha256(password_digest).digest()).decode()
    headers = {
        'Authorization': 'WSSE profile="UsernameToken"',
        'X-WSSE': f'UsernameToken Username="{username}", PasswordDigest="{generated_digest}", \
         Nonce="{nonce_bytes}", Created="{created}"'
    }
    return headers

#-----------------------------------------------------------------------

def getUndergraduate(netid):
    """
    Get the undergraduate profile associated with `netid`, if exists.
    Otherwise, returns None.

    Parameters
    ----------
    netid : str

    Returns
    -------
    dict
        Princeton undergraduate profile with key-value pairs associated with
        `netid`.

    """
    try:
        log.info(f'Initiating TigerBook Request for netid = \"{netid}\".')
        url = 'https://tigerbook.herokuapp.com/api/v1/undergraduates'
        url = os.path.join(url, netid)
        headers = generateHeaders()
        response = requests.get(
            url=url,
            headers=headers)
        response.raise_for_status()
        undergrad = json.loads(response.content)
        return undergrad
    except requests.exceptions.HTTPError as e:
        log.warning(f'TigerBook Undergraduate profile not found for netid = \"{netid}\": ' + str(e))
        return None

#-----------------------------------------------------------------------

def createUser(netid):
    """
    Create a new user with `netid`. Populate account info if `netid`
    associated with an undergraduate student.

    Parameters
    ----------
    netid : str

    Returns
    -------
    User
        New User associated with `netid`.

    """
    new_user = None
    undergrad_profile = getUndergraduate(netid)
    if undergrad_profile:
        new_user = User(netid=netid, email=undergrad_profile.get('email'),
                        first_name=undergrad_profile.get('first_name'),
                        last_name=undergrad_profile.get('last_name'),
                        class_year=undergrad_profile.get('class_year'))
    else:
        new_user = User(netid=netid)

    try:
        db.session.add(new_user)
        db.session.commit()
        log.info(f'New {new_user} created!')
        return new_user
    except Exception as e:
        db.session.rollback()
        msg = f'Failed to create user account with netid = \"{netid}\"'
        log.critical(msg, exc_info=True)
        return None

#-----------------------------------------------------------------------

if __name__=="__main__":
    # existing user
    netid = 'zbatscha'
    undergrad_profile = getUndergraduate(netid)
    print(undergrad_profile)
    print(undergrad_profile.get('net_id'), undergrad_profile.get('first_name'),
        undergrad_profile.get('last_name'), undergrad_profile.get('class_year'),
        undergrad_profile.get('email'))

    # non-existing user
    undergrad_profile = getUndergraduate('notUndergraduate')
    print(undergrad_profile)

    # user = createUser('zbatscha')
    # print(user)
