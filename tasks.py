from tangelo import log
from celery import Celery
from celery.task import periodic_task
from datetime import timedelta
from os import environ
import news_api
import poem_api
import princetonNews_api
import academic_calendar

REDIS_URL = environ.get('REDISTOGO_URL', 'redis://localhost:6379')

celery = Celery('tasks', broker=REDIS_URL)


@periodic_task(run_every=timedelta(minutes=20))
def updateNews():
    log.info('Launching task for News Widget')
    news_api.updateNews()

@periodic_task(run_every=timedelta(hours=1))
def updatePoem():
    log.info('Launching task for Poem Widget')
    poem_api.updatePoem()

@periodic_task(run_every=timedelta(hours=1))
def updatePrincetonNews():
    log.info('Launching task for Princeton News Widget')
    princetonNews_api.updateNews()

@periodic_task(run_every=timedelta(hours=1))
def updateAcademicCalendar():
    log.info('Launching task for Academic Calendar Widget')
    academic_calendar.updateCalendar()
