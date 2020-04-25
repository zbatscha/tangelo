#Credit to News API for API Key
import requests
from tangelo.models import CustomPost, Widget, User
from tangelo import app, db, log

error_msg_global = "hmmm, something\'s not right."
MAX_POSTS = 1
def updateNews():

    news_url = ('http://newsapi.org/v2/top-headlines?country=us&apiKey=02f90cf35f2b4176a559db2847011096')

    try:
        response = requests.get(news_url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as err:
        log.error('Error updating news widget', exc_info=True)
        raise Exception(error_msg_global)
    articles = data.get('articles')
    if not articles:
        return
    for i, article in enumerate(articles):
        if i >= MAX_POSTS:
            break
        if not article:
            continue
        title = article.get('title')
        content = article.get('content')
        source = article.get('source')
        if source:
            source = source.get('name')
        url = article.get('url')


        with app.app_context():
                try:
                    news_widget = Widget.query.filter_by(alias_name='news').first()
                    if news_widget:
                        article_post = CustomPost(content=title, custom_author=source, widget=news_widget)
                        db.session.add(article_post)
                        db.session.commit()
                except Exception as e:
                    print(e)
                    break
                    db.session.rollback()
                    pass

if __name__ =='__main__':
    updateNews()
