#!/usr/bin/env python

#-----------------------------------------------------------------------
# poem.py
# Author: Ziv Batscha
#-----------------------------------------------------------------------

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from tangelo.models import Post, User, Widget, CustomPost
from tangelo import db, app, log

#-----------------------------------------------------------------------

daily_url = 'https://www.poetryfoundation.org/poems/poem-of-the-day'

def getPoem():

    soup = None
    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        # get daily poem url
        req = Request(daily_url, headers=hdr)
        page = urlopen(req, timeout = 10)
        soup = BeautifulSoup(page, 'html.parser')
        a_div = soup.find('div', attrs={'class': 'c-feature'}).find('a', recursive=False)
        poem_url = a_div['href']
        # get daily poem
        req = Request(poem_url, headers=hdr)
        page = urlopen(req, timeout = 10)
        soup = BeautifulSoup(page, 'html.parser')
    except Exception as e:
        log.error('Error retrieving daily poem.', exc_info=True)
        return

    try:
        poem_body = soup.findAll("div", {"class": "o-poem"})
        poem_body_soup = poem_body[0]
        divs = poem_body_soup.findAll("div")
        poem_body = []
        for line in divs:
            poem_body.append(line.text.strip())
        poem_body = "\n".join(poem_body).strip()

        poem_title_div = soup.find('div', {"class": "c-feature-hd"})
        poem_title = poem_title_div.find('h1').text
        poem_title = poem_title.strip()

        poem_author_div = soup.find('div', {"class": "c-feature-sub"})
        poem_author = poem_author_div.find('a').text
        poem_author = poem_author.strip()

        poem = '\n' + poem_title + '\n\n' + poem_body

    except Exception as e:
        log.error('Error scraping daily poem.', exc_info=True)
        print('here')
        return

    with app.app_context():
        try:
            tangelo = User.query.filter_by(netid='tangelo').first()
            poem_widget = Widget.query.filter_by(alias_name='poems').first()
            db.session.query(CustomPost).filter(CustomPost.widget_id==poem_widget.id).delete()
            poem_post = CustomPost(content=poem, custom_author=poem_author, widget=poem_widget)
            db.session.add(poem_post)
            poem_widget.active = True
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error('Error updating daily poem post.', exc_info=True)
            try:
                poem_widget.active = False
                db.session.commit()
            except Exception as e:
                db.session.rollback()


if __name__=='__main__':

    getPoem()
