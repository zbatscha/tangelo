#Credit to News API for API Key
import requests
from tangelo.models import CustomPost, Widget, User
from tangelo import app, db, log
import re

error_msg_global = "hmmm, something\'s not right."
MAX_POSTS = 10
def updateNews():
    log.info('Starting \'News\' widget update...')
    news_url = ('http://newsapi.org/v2/top-headlines?country=us&apiKey=02f90cf35f2b4176a559db2847011096')

    try:
        response = requests.get(news_url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        log.error('Failed to update \'News\' widget.', exc_info=True)
        return
    articles = data.get('articles')
    if not articles:
        return
    new_articles = []
    for i, article in enumerate(articles):
        if i >= MAX_POSTS:
            break
        if not article:
            continue
        title = article.get('title')
        title = re.sub(r'-\s*[^-]+$', '', title).strip()
        source = article.get('source')
        if source:
            source = source.get('name')
            # source = re.sub(r'\.com.*$', '', source).strip()

        url = article.get('url')
        new_articles.append({'title': title, 'source': source, 'url': url})


    with app.app_context():
        news_widget = None
        try:
            news_widget = Widget.query.filter_by(alias_name='news').first()
            if not news_widget:
                log.critical('News widget not found')
                return
        except Exception as e:
            log.error('Error retrieving News Widget', exc_info=True)
            return
        try:
            db.session.query(CustomPost).filter(CustomPost.widget_id==news_widget.id).delete()
            for a in new_articles:
                article_post = CustomPost(content=a['title'], custom_author=a['source'], url=a['url'], widget=news_widget)
                db.session.add(article_post)
            news_widget.active = True
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            log.error('Error updating News Widget')
            try:
                news_widget.active = False
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                log.error('Error updating News Widget active status')
    log.info('Exiting \'News\' widget update.')


if __name__ =='__main__':
    updateNews()
