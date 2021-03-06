from ics import Calendar
import requests
import datetime
from tangelo import app, db, log
from tangelo.models import CustomPost, Widget, User
from operator import itemgetter

MAX_EVENTS = 10

def updateCalendar():
    log.info('Starting \'Academic Calendar\' widget update...')
    url = "https://registrar.princeton.edu/feeds/events/ical.ics"

    try:
        response = requests.get(url)
        response.raise_for_status()
        c = Calendar(response.text)
    except requests.exceptions.HTTPError as err:
        log.error("Error updating academic calendar widget", exc_info=True)
        return
    info = []
    for event in c.events:
        info.append({'event_name': event.name, 'start_month': date_extraction(str(event.begin))[0], 'start_day': date_extraction(str(event.begin))[1], 'start_year': date_extraction(str(event.begin))[2]})

    sorted_info = sorted(info, key=itemgetter('start_year', 'start_month', 'start_day'))
    current_month = datetime.datetime.today().month
    current_day = datetime.datetime.today().day
    current_year = datetime.datetime.today().year
    i = 0

    for s in sorted_info:
        if s['start_year'] >= current_year:
            break
        i += 1

    j = i
    while sorted_info[j]['start_month'] < current_month:
        j += 1

    m = j
    while sorted_info[m]['start_day'] < current_day:
        m += 1

    k = m
    next_ten_events = []
    while k < 10 + m:
        next_ten_events.append(sorted_info[k])
        if k + 1 > len(sorted_info): break
        k += 1

    with app.app_context():
        pton_calendar = None
        try:
            pton_calendar = Widget.query.filter_by(alias_name='pton_calendar').first()
            if not pton_calendar:
                log.critical('Pton Calendar Widget not found')
                return
        except Exception:
            log.error('Error retrieving pton calendar widget', exc_info=True)

        try:
            db.session.query(CustomPost).filter(CustomPost.widget_id==pton_calendar.id).delete()
            t = len(next_ten_events) - 1
            while t >= 0:
                e = next_ten_events[t]
                content_string = str(e['event_name'])
                day = str(e['start_day'])

                if len(day) == 1:
                    day = "0" + day

                author_string = str(e['start_month']) + "/" + day + "/" + str(e['start_year'])
                calendar_event = CustomPost(content=content_string, custom_author=author_string, widget = pton_calendar)
                db.session.add(calendar_event)
                t -= 1
            pton_calendar.active = True
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            log.error('Error updating Pton Calendar Widget')
            log.error(e)
            try:
                pton_calendar.active = False
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                log.error('Error updating Pton Calendar Widget active status')
    log.info('Exiting \'Academic Calendar\' widget update.')

def date_extraction(event_date):
    year = str(event_date[0:4])
    month = str(event_date[5:7])
    day = str(event_date[8:10])

    if month[0] == '0':
        month = month[1]
    if day[0] == '0':
        day = day[1]
    
    return [int(month), int(day), int(year)]

if __name__ == "__main__":
    updateCalendar()
