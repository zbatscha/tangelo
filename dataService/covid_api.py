import requests
from tangelo.models import CustomPost, Widget, User
from tangelo import app, db, log
import locale
locale.setlocale(locale.LC_ALL, '')

country = 'US'
error_msg_global = "hmmm, something\'s not right."

def updateCOVIDReport():
    log.info('Starting \'COVID\' widget update...')

    covid_url = 'https://pomber.github.io/covid19/timeseries.json'

    try:
        response = requests.get(covid_url)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        log.error('Failed to update \'COVID\' widget.', exc_info=True)
        return

    country_data = data[country]
    today_confirmed = country_data[-1]['confirmed']
    yesterday_confirmed = country_data[-2]['confirmed']
    today_deaths = country_data[-1]['deaths']
    yesterday_deaths = country_data[-2]['deaths']

    post = f'Since yesterday, the US has witnessed an increase in total confirmed cases by {today_confirmed-yesterday_confirmed:n}, and an increase in total deaths by {today_deaths-yesterday_deaths:n}.'

    with app.app_context():
        covid_widget = None
        try:
            covid_widget = Widget.query.filter_by(alias_name='covid').first()
            if not covid_widget:
                log.critical('COVID widget not found')
                return
        except Exception as e:
            log.error('Error retrieving COVID widget', exc_info=True)
            return
        try:
            db.session.query(CustomPost).filter(CustomPost.widget_id==covid_widget.id).delete()
            covid_post = CustomPost(content=post, custom_author="Johns Hopkins CSSE", widget=covid_widget)
            db.session.add(covid_post)
            covid_widget.active = True
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            log.error('Error updating COVID widget')
            try:
                covid_widget.active = False
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                log.error('Error updating COVID widget active status')
    log.info('Exiting \'COVID\' widget update.')


if __name__ =='__main__':
    updateNews()
