#!/usr/bin/env python

#-----------------------------------------------------------------------
# database.py
#-----------------------------------------------------------------------

from sqlite3 import connect
from sys import stderr
from os import path
from widget import Widget
#-----------------------------------------------------------------------

class Database:

    def __init__(self):
        self._connection = None

    def connect(self):
        DATABASE_NAME = 'tangelo.sqlite'
        if not path.isfile(DATABASE_NAME):
            raise Exception('Database {0} not found'.format(DATABASE_NAME))
        self._connection = connect(DATABASE_NAME)

    def disconnect(self):
        self._connection.close()

    def widgetSearch(self, field):

        field = field.lower()

        cursor = self._connection.cursor()

        QUERY_STRING = \
            'select id, title, description from widgets ' + \
            'where title like ? OR description like ?'
        cursor.execute(QUERY_STRING, (field+'%',field+'%'))

        widgets = []
        row = cursor.fetchone()
        while row:
            widget = Widget(int(row[0]), str(row[1]), str(row[2]))
            widgets.append(widget);
            row = cursor.fetchone()
        cursor.close()
        return widgets

#-----------------------------------------------------------------------

# For testing:

if __name__ == '__main__':
    database = Database()
    database.connect()
    widgets = database.widgetSearch('w')
    for widget in widgets:
        print(widget)
    database.disconnect()
    print('need to test database!')
