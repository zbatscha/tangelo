#!/usr/bin/env python

#-----------------------------------------------------------------------
# feed.py
#-----------------------------------------------------------------------

import feedparser

#-----------------------------------------------------------------------

url = 'https://www.princeton.edu/feed'
feed = feedparser.parse(url)

feed_title = feed['feed']['title']
feed_description = feed['feed']['subtitle']

for post in feed.entries:
    print(post)
    print(post.title)
    print(post.published_parsed)
