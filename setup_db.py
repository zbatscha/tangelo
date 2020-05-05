from tangelo import app, db, log
from tangelo.models import User, Widget, Subscription, Post, AdminAssociation, CustomPost
from dataService import news_api, poem_api, princetonNews_api, academic_calendar, covid_api
import sys

def setupTangelo():
    try:
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()

            user_1 = User(netid='tangelo')

            widget_1 = Widget(name='Welcome to Tangelo!', description = 'Here\'s a quick demo to get you started on Tangelo!', style='welcomeWidget.html', type = 'custom')
            widget_2 = Widget(name = '🕒', description = 'Life as a Princeton tiger is hectic. Stay on time with this clock.', style='clock.html', type = 'custom')
            widget_3 = Widget(name = '📅', description = 'Missing deadlines? Get back on track with this date widget.', style='date.html', type = 'custom')
            widget_4 = Widget(name = '🌦️', description = 'Rain or shine, we\'ve got the current weather for you.', style='weather.html', type = 'custom')
            widget_5 = Widget(name = 'News', description = 'Keep up to date with the latest top headlines.', type = 'custom', alias_name = 'news', post_limit=10)
            widget_6 = Widget(name = 'COVID-19', description='The latest numbers on US COVID-19 Cases.', type = 'custom', alias_name="covid")
            widget_7 = Widget(name = 'Poem-a-Day', description = 'A daily poem for you sourced from Poetry Foundation.', type = 'custom', alias_name = 'poems')
            widget_8 = Widget(name = 'Princeton University News', description = 'The latest news and stories from Princeton University.', type = 'custom', alias_name = 'princeton_news', post_limit=10, handle_display='date_published')
            widget_9 = Widget(name = 'Happy Birthday!', description = 'We\'re counting down the days till your birthday celebration!🎉🎂', type = 'custom',
                              style = 'birthday.html')
            widget_10 = Widget(name = 'Princeton Academic Calendar', description = 'Never miss course selection with this handy academic calendar.', type = 'custom', alias_name = 'pton_calendar',  post_limit=10)

            db.session.add(widget_1)
            db.session.add(widget_2)
            db.session.add(widget_3)
            db.session.add(widget_4)
            db.session.add(widget_5)
            db.session.add(widget_6)
            db.session.add(widget_7)
            db.session.add(widget_8)
            db.session.add(widget_9)
            db.session.add(widget_10)

            widget_1.admins.append(user_1)
            widget_2.admins.append(user_1)
            widget_3.admins.append(user_1)
            widget_4.admins.append(user_1)
            widget_5.admins.append(user_1)
            widget_6.admins.append(user_1)
            widget_7.admins.append(user_1)
            widget_8.admins.append(user_1)
            widget_9.admins.append(user_1)
            widget_10.admins.append(user_1)

            db.session.add(user_1)

            db.session.commit()

    except Exception as e:
        db.session.rollback()
        log.error('Failed to setup Tangelo DB!', exc_info=True)

if __name__=="__main__":
    setupTangelo()
    if len(sys.argv) > 1:
        news_api.updateNews()
        poem_api.updatePoem()
        princetonNews_api.updateNews()
        academic_calendar.updateCalendar()
        covid_api.updateCOVIDReport()
