#!/usr/bin/env python

#-----------------------------------------------------------------------
# poem.py
# Author: Ziv Batscha
#-----------------------------------------------------------------------

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from tangelo.models import Post, User, Widget, CustomPost
from tangelo import db, app

#-----------------------------------------------------------------------
poem_url = 'https://www.poetryfoundation.org/poems/poem-of-the-day'

def getPoem():
    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = Request(poem_url, headers=hdr)
    page = urlopen(req)
    soup = BeautifulSoup(page, 'html.parser')

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

    with app.app_context():
        try:
            tangelo = User.query.filter_by(netid='tangelo').first()
            poem_widget = Widget.query.filter_by(alias_name='poems').first()
            poem_post = CustomPost(content=poem, custom_author=poem_author, widget=poem_widget)
            db.session.add(poem_post)
            db.session.commit()
        except Exception as e:
            print(e)

if __name__=='__main__':

    getPoem()
