from tangelo.models import User, Widget, Post, Subscription
from tangelo import db, app
from flask_login import current_user

def addWidget(form):
    try:
        widget = Widget(name=form.name.data,
                        description=form.description.data,
                        access_type=form.access_type.data,
                        post_type=form.post_type.data)

        widget.admins.append(current_user)
        subscription = Subscription(user=current_user, widget=widget)
        db.session.add(widget)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise Exception(e)

def getValidWidgetsPost():
    return [('Prospect', 'Prospect')]

def addPost(form):
    try:
        # check if valid widget
        widget = Widget.query.filter_by(name=form.widget_target.data).first()
        if not widget:
            raise Exception('Selected widget does not exist.')
        # check if current user can post to this widget
        # if not canPost():
        #     raise Exception('Selected widget does not exist.')
        post = Post(title=form.title.data,
                    body=form.body.data,
                    author=current_user,
                    widget=widget)
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(e)
