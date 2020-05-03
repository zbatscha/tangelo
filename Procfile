web: gunicorn tangelo:app
worker: celery -A tasks worker -B -E --loglevel=info
