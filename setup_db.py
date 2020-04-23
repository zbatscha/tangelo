from tangelo import app, db
from tangelo.models import User, Widget, Subscription, Post, AdminAssociation
from news_collector import news_object
from tangelo.WHO_RSS import covid_data

with app.app_context():
    db.drop_all()
    db.create_all()

    user_1 = User(netid='tangelo')

    widget_1 = Widget(name = "Welcome to Tangelo!", description = "")
    widget_2 = Widget(name = '🕒', description = '', style='<link rel=\\"stylesheet\\" href=\\"../static/clock.css\\"/><script type=\\"text/javascript\\" src=\\"../static/clock.js\\"></script><div id=\\"centerPanelClock\\"><h1 id=\\"time\\"></h1></div>')
    widget_3 = Widget(name = '📅', description = '', style='<link rel=\\"stylesheet\\" href=\\"../static/date.css\\"/><script type=\\"text/javascript\\" src=\\"../static/clock.js\\"></script><div id=\\"centerPanelDate\\"><h1 id = \\"date\\"></h1></div>')
    widget_4 = Widget(name = '🌦️', description = '', style='<link rel=\\"stylesheet\\" href=\\"../static/weather.css\\"/><script type=\\"text/javascript\\" src=\\"../static/weather.js\\"></script><div id=\\"centerPanelWeather\\"><h1 id=\\"temperature\\">One moment, we\'re getting some weathery goodness</h1><h1 id=\\"sky\\"></h1></div>')

    news = news_object()
    title = news.titles()[0]
    author = news.source()[0]
    url = news.urls()[0]
    widget_5 = Widget(name = 'News', description = "Keep up to date with the latest top headlines.", style='<link rel=\\"stylesheet\\" href=\\"../static/genericWidget.css\\"/><div class=\\"centerPanelWidget\\"><h3 class = \\"genericTitle\\"><center>News</center></h3><hr class = \\"genericDivider\\"><div class = \\"GenericPost\\"><a class = \\"GenericPoster\\">@'+author+'</a>'+title+'</div><a href='+url+'>Click here for more information</a></div>')

    us_data = covid_data("US")
    outputString = us_data.number_day_decreasing_confirmed()
    widget_6 = Widget(name = 'Covid-19 Cases', description="Keep up to date with the latest numbers on new COVID-19 Cases.", style='<link rel=\\"stylesheet\\" href=\\"../static/genericWidget.css\\"/><div class=\\"centerPanelWidget\\"><h3 class = \\"genericTitle\\"><center>Covid-19 Cases Update</center></h3><hr class = \\"genericDivider\\"><div class = \\"GenericPost\\"><a class = \\"GenericPoster\\">@Johns Hopkins CSSE</a>'+outputString+'</div>')

    db.session.add(widget_1)
    db.session.add(widget_2)
    db.session.add(widget_3)
    db.session.add(widget_4)
    db.session.add(widget_5)
    db.session.add(widget_6)

    widget_1.admins.append(user_1)
    widget_2.admins.append(user_1)
    widget_3.admins.append(user_1)
    widget_4.admins.append(user_1)
    widget_5.admins.append(user_1)
    widget_6.admins.append(user_1)

    post_1 = Post(content='We\'re glad you\'re here.', author=user_1, widget=widget_1)

    db.session.add(user_1)
    db.session.add(post_1)

    db.session.commit()
