#!/usr/bin/env python

#-----------------------------------------------------------------------
# feed.py
#-----------------------------------------------------------------------

import feedparser
from datetime import datetime
from tangelo.models import Post, User, Widget, CustomPost
from tangelo import db, app, log
import sys

#-----------------------------------------------------------------------

princeton_news_url = 'https://www.princeton.edu/feed'

def updateNews():
    log.info('Starting \'Princeton News\' widget update...')
    MAX_POSTS = None
    try:
        with app.app_context():
            princeton_news_widget = Widget.query.filter_by(alias_name='princeton_news').first()
            if not princeton_news_widget:
                log.critical('Princeton News Widget not found when attempting to update')
            MAX_POSTS = princeton_news_widget.post_limit
    except Exception as e:
        return

    news_posts = None
    try:
        feed = feedparser.parse(princeton_news_url)
        if not feed:
            return
        news_posts_count = min(len(feed.entries), MAX_POSTS)
        if not news_posts_count:
            return

        news_posts = [None] * news_posts_count
        for i, post in enumerate(feed.entries):
            if i == news_posts_count:
                break
            title = post.title
            if not title:
                continue
            author = post.author
            if not author:
                author = 'Office of Communications'
            if post.published_parsed:
                date_published = datetime(*post.published_parsed[:6])
            url = post.link
            news_posts[i] = {'title': title, 'author': author, 'date_published': date_published, 'url': url}

    except Exception as e:
        log.error('Error retrieving new posts for Princeton News widget')
        return
    with app.app_context():
        try:
            princeton_news_widget = Widget.query.filter_by(alias_name='princeton_news').first()
            db.session.query(CustomPost).filter(CustomPost.widget_id==princeton_news_widget.id).delete()
            for post in news_posts:
                news_post = CustomPost(content=post['title'], custom_author=post['author'], url=post['url'], create_dttm= post['date_published'], widget=princeton_news_widget)
                db.session.add(news_post)
            princeton_news_widget.active = True
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error('Error updating daily poem post.', exc_info=True)
            try:
                princeton_news_widget.active = False
                db.session.commit()
            except Exception as e:
                db.session.rollback()
    log.info('Exiting \'Princeton News\' widget update.')

if __name__=="__main__":
    updateNews()
