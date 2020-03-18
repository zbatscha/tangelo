#!/usr/bin/env python

#-----------------------------------------------------------------------
# widget.py
#-----------------------------------------------------------------------

class Widget:

    def __init__(self, id, title, description):
        self._id = id
        self._title = title
        self._description = description

    def __str__(self):
        return self._title + '\n' + self._description

    def getId(self):
        return self._id

    def getTitle(self):
        return self._title

    def getDescription(self):
        return self._description
