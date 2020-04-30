from tangelo import app, db
from tangelo.models import User, Widget, Subscription, Post, AdminAssociation, CustomPost
from tangelo.WHO_RSS import covid_data
import news_api
import poem_api
import princetonNews_api
import academic_calendar

with app.app_context():
    db.drop_all()
    db.create_all()

    user_1 = User(netid='tangelo')

    widget_1 = Widget(name='Welcome to Tangelo!',
                      style=' \
                          <div class = \"centerPanelWidget\" id=\"step2\"> \
                            <h3 class = \"genericTitle\">Welcome to Tangelo!</h3> \
                            <hr class = \"genericDivider\"> \
                            <div class = \"GenericPost\"> \
                                <a class = \"GenericPoster\">@tangelo</a> We\'re glad you\'re here. \
                            </div> <br>\
                            <div class=\"row text-center\"> \
                                <div class=\"col-12\"> \
                                    <a class=\"btn btn-large btn-success\" href=\"#\" onclick=\"startIntro();\">How It Works</a> \
                                </div> \
                             </div> \
                          </div>', description = 'Here\'s a quick demo to get you started on Tangelo!', type = 'custom')
    widget_2 = Widget(name = '🕒', description = 'Life as a Princeton tiger is hectic. Stay on time with this clock.', style='<link rel=\"stylesheet\" href=\"../static/clock.css\"/><script type=\"text/javascript\" src=\"../static/clock.js\"></script><div id=\"centerPanelClock\"><h1 id=\"time\"></h1></div>', type = 'custom')
    widget_3 = Widget(name = '📅', description = 'Missing deadlines? Get back on track with this date widget.', style='<link rel=\"stylesheet\" href=\"../static/date.css\"/><script type=\"text/javascript\" src=\"../static/date.js\"></script><div id=\"centerPanelDate\"><h1 id = \"date\"></h1></div>', type = 'custom')
    widget_4 = Widget(name = '🌦️', description = 'Rain or shine, we\'ve got the current weather for you.', style='<link rel=\"stylesheet\" href=\"../static/weather.css\"/><script type=\"text/javascript\" src=\"../static/weather.js\"></script><div id=\"centerPanelWeather\"><h1 id=\"temperature\">One moment, we\'re getting some weathery goodness</h1><h1 id=\"sky\"></h1></div>', type = 'custom')

    widget_5 = Widget(name = 'News', description = 'Keep up to date with the latest top headlines.', type = 'custom', alias_name = 'news', post_limit=10)

    us_data = covid_data('US')
    outputString = us_data.number_day_decreasing_confirmed()
    widget_6 = Widget(name = 'COVID-19', description='The latest numbers on US COVID-19 Cases.', style='<link rel=\"stylesheet\" href=\"../static/genericWidget.css\"/><div class=\"centerPanelWidget\"><h3 class = \"genericTitle\"><center>Covid-19 Cases Update</center></h3><hr class = \"genericDivider\"><div class = \"GenericPost\"><a class = \"GenericPoster\">@Johns Hopkins CSSE</a>'+outputString+'</div>', type = 'custom')
    widget_7 = Widget(name = 'Poem-a-Day', description = 'A daily poem for you sourced from Poetry Foundation.', type = 'custom', alias_name = 'poems')
    widget_8 = Widget(name = 'Princeton University News', description = 'The latest news and stories from Princeton University.', type = 'custom', alias_name = 'princeton_news', post_limit=10)
    widget_9 = Widget(name = 'Happy Birthday!', description = 'We\'re counting down the days till your birthday celebration!🎉🎂')
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

news_api.updateNews()
poem_api.updatePoem()
princetonNews_api.updateNews()
academic_calendar.updateCalendar()
