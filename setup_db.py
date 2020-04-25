from tangelo import app, db
from tangelo.models import User, Widget, Subscription, Post, AdminAssociation, CustomPost
from tangelo.WHO_RSS import covid_data
import news_api
import poem_api

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
                          </div>', description = 'Tangelo Demo!', type = 'custom')
    widget_2 = Widget(name = '🕒', description = '', style='<link rel=\"stylesheet\" href=\"../static/clock.css\"/><script type=\"text/javascript\" src=\"../static/clock.js\"></script><div id=\"centerPanelClock\"><h1 id=\"time\"></h1></div>', type = 'custom')
    widget_3 = Widget(name = '📅', description = '', style='<link rel=\"stylesheet\" href=\"../static/date.css\"/><script type=\"text/javascript\" src=\"../static/date.js\"></script><div id=\"centerPanelDate\"><h1 id = \"date\"></h1></div>', type = 'custom')
    widget_4 = Widget(name = '🌦️', description = '', style='<link rel=\"stylesheet\" href=\"../static/weather.css\"/><script type=\"text/javascript\" src=\"../static/weather.js\"></script><div id=\"centerPanelWeather\"><h1 id=\"temperature\">One moment, we\'re getting some weathery goodness</h1><h1 id=\"sky\"></h1></div>', type = 'custom')

    widget_5 = Widget(name = 'News', description = 'Keep up to date with the latest top headlines.', type = 'custom', alias_name = 'news')

    us_data = covid_data('US')
    outputString = us_data.number_day_decreasing_confirmed()
    widget_6 = Widget(name = 'Covid-19 Cases', description='Keep up to date with the latest numbers on new COVID-19 Cases.', style='<link rel=\"stylesheet\" href=\"../static/genericWidget.css\"/><div class=\"centerPanelWidget\"><h3 class = \"genericTitle\"><center>Covid-19 Cases Update</center></h3><hr class = \"genericDivider\"><div class = \"GenericPost\"><a class = \"GenericPoster\">@Johns Hopkins CSSE</a>'+outputString+'</div>', type = 'custom')
    widget_7 = Widget(name = 'Daily Poem', description = 'A daily poem for you sourced from Poetry Foundation.', type = 'custom', alias_name = 'poems')

    db.session.add(widget_1)
    db.session.add(widget_2)
    db.session.add(widget_3)
    db.session.add(widget_4)
    db.session.add(widget_5)
    db.session.add(widget_6)
    db.session.add(widget_7)

    widget_1.admins.append(user_1)
    widget_2.admins.append(user_1)
    widget_3.admins.append(user_1)
    widget_4.admins.append(user_1)
    widget_5.admins.append(user_1)
    widget_6.admins.append(user_1)
    widget_7.admins.append(user_1)

    widget_8 = Widget(name = 'Test Widget', description = 'This is my first Test!')
    db.session.add(widget_8)
    test_post = Post(content='This is a very very long. test This is a very very long. test This is a very very long. test test** > & + = \r \n hello.', author=user_1, widget=widget_8)

    db.session.add(user_1)
    db.session.add(test_post)

    db.session.commit()

news_api.updateNews()
poem_api.getPoem()
