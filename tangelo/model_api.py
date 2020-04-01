from tangelo.models import User, Widget, Post, Subscription
from tangelo import db, app
from flask_login import current_user

def addWidget(form):
    try:
        widget = Widget(name=form.name.data,
                        description=form.description.data,
                        post_type=form.post_type.data)

        widget.admins.append(current_user)
        subscription = Subscription(user=current_user, widget=widget)
        db.session.add(widget)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise Exception(e)

def addPost(form):
    print(form.content.data)
    print(form.widget_target.data)
    try:
        # check if valid widget
        widget = Widget.query.filter_by(id=form.widget_target.data).first()
        if not widget:
            raise Exception('Selected widget does not exist.')
        post = Post(content=form.content.data,
                    author=current_user,
                    widget=widget)
        db.session.add(post)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise Exception(e)

def getValidWidgetsPost(current_user):
    all_widgets = current_user.widgets
    choices = []
    for widget in all_widgets:
        if widget.post_type == 'public' or current_user in widget.admins:
            choices.append((widget.id, widget.name))
    print(choices)
    return choices
