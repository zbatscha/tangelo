#!/usr/bin/env python

#-----------------------------------------------------------------------
# tangeloService.py
#-----------------------------------------------------------------------

from time import strftime

def getGreetingDayTime():

    hour = int(strftime('%H'))
    if hour < 12:
        return 'morning'
    if hour >= 12 and hour < 17:
        return 'afternoon'
    if hour >= 17 and hour <= 21:
        return 'evening'
    return 'night'
