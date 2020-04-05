#!/usr/bin/env python

"""
Provides methods to perform a request to the tigerbook API to query a Princeton
undergrad by netid.
"""

import hashlib
import random
import requests
import json
from base64 import b64encode, b64decode
from datetime import datetime
import os

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

if __name__=="__main__":

    undergrad = getUndergraduate('cl43')
    print(undergrad)
