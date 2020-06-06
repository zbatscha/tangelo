# Tangelo

Welcome to Tangelo, the daily app designed for Princeton students. Have a Princeton netid? Get started at: https://tangelo.herokuapp.com/

Tangelo is our capstone project for COS 333 (Advanced Programming Techniques) taught by Professor Robert Dondero at Princeton University. A major goal of the course is to design and implement a networked three-tier system (a user interface, a database for persistent storage, and some processing between them), in teams of 3 to 5 students.

Inspired by the simplicity of bullet journals, our platform allows users to custom-build their perfect morning experience. Tangelo achieves this through a dashboard of widgets. In its most basic form, a widget is simply a feed that can display information and be moved around. By following widgets or creating their own, users can view and organize a vast array of pertinent information in real-time.

Our widgets offer the ideal balance of utility and delight, with sleek interfaces and robust functionality for the everyday experience. Have a live calendar of important academic updates or browse the Daily Prince headlines from a single dashboard interface. With widgets ranging from the uber-practical clock and weather to News updates and student events, we have something for every kind of person.

Make life simple. Get Tangelo.

# Team Members
Ziv Batscha (Project Leader), Ryan Thorpe, Fawaz Ahmad, Austin Mejia

# Demo

Coming soon!

# Install

## Basic Setup
    $ git clone https://github.com/zbatscha/tangelo.git
    $ cd tangelo
    $ python -m venv venvTangelo
    $ . venvTangelo/bin/activate
    (venvTangelo) $ pip install -r requirements.txt

## PostgreSQL Database Quickstart

Install postgresql

**Mac** 

Option 1, using Homebrew:

    $ brew install postgresql
    $ brew services start postgresql

Option 2: Visit https://postgresapp.com/.

**Windows**

Visit https://www.postgresql.org/download/windows/
# 
Development database creation:

    $ psql postgres
    postgres=# CREATE DATABASE tangelo_test;

Protip:
To easily visualize and manipulate Tangelo’s development database, we recommend installing a graphical client as well:

For Mac, Postico: https://eggerapps.at/postico/.

For Windows, pgAdmin 4: https://www.pgadmin.org/download/.

## Environment Variables
Unix Bash (Linux, Mac, etc.)

    (venvTangelo) $ export FLASK_ENV='development'
    (venvTangelo) $ export DATABASE_URL='postgresql+psycopg2://user:password@127.0.0.1:5432/tangelo_test' 
    
user and password are unique to the values set upon database connection in postico. 5432 is the default port.

Flask requires a secret key to be set. To create a secret key, we suggest Python’s built-n secrets module:

    $ python
    >>> import secrets
    >>> yourSecretKey = secrets.token_hex(16)

    (venvTangelo) $ export SECRET_KEY='yourSecretKey'

___
Setting API Keys

Tangelo is currently open for members of the Princeton community with a valid netid. To use the TigerBook API Request functionality when creating new users locally, you will need to set these two environment variables:

    (venvTangelo) $ export TIGERBOOK_USERNAME='yourNetid'
    (venvTangelo) $ export TIGERBOOK_KEY=’yourTigerbookKey’

To get your unique TigerBook API Key, login to Princeton CAS, and visit:
https://tigerbook.herokuapp.com/api/v1/getkey/. The displayed string of characters is your key.

Our news widget requires an API Key. Get yours for free here: https://newsapi.org/, and set the variable:

    (venvTangelo) $ export NEWS_KEY='yourNewsKey'
     
## Populate Database with Custom Widgets

    (venvTangelo) $ python setup_db.py

## Run Development Server

    (venvTangelo) $ python run.py port

For example, if port is set to 5000, go to http://localhost:5000.

## Automated Content Updates with Celery
Tangelo currently includes 10 custom widgets designed and administered by our team. 5 of these widgets (Academic Calendar, COVID-19, News, Poem-a-Day, Princeton University News) require server-side content updates.  To automate the process of updating tangelo administered content, we integrated a Celery Beat scheduler, allowing for script tasks to be executed at regular intervals (20-60 minutes). `tasks.py` initializes the Celery worker and task schedule. All scheduled tasks are managed by a Redis broker. To see this in action, install redis and launch the worker.

Install Redis (macOS):

    $ brew install redis

In one terminal window, start the redis server:

    (venvTangelo) $ redis-server

In another terminal window, start the worker:

    (venvTangelo) $ celery -A tasks worker -B -E --loglevel=info


## Additional Documents

[Project Overview](https://github.com/zbatscha/tangelo/docs/ProjectOverview.pdf)

[User's Guide](https://github.com/zbatscha/tangelo/docs/UserGuide.pdf)

[Programmer's Guide (High-level)](https://github.com/zbatscha/tangelo/docs/ProgrammersGuide.pdf)

[Product Evaluation](https://github.com/zbatscha/tangelo/docs/ProductEvaluation.pdf)

[Project Evaluation](https://github.com/zbatscha/tangelo/docs/ProjectEvaluation.pdf)

[Tangelo Slidedeck](https://github.com/zbatscha/tangelo/docs/TangeloSlidedeck.pdf)



