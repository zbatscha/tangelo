#!/usr/bin/env python

#-----------------------------------------------------------------------
# run.py
#-----------------------------------------------------------------------

from tangelo import app
from sys import argv

#-----------------------------------------------------------------------

if __name__ == '__main__':

    if len(argv) != 2:
        print('Usage: ' + argv[0] + ' port')
        exit(1)
    app.run(host='localhost', port=int(argv[1]), debug=True)
