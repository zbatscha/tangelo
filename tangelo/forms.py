from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from tangelo.models import Widget, User

class SearchWidget(FlaskForm):
    search_text = StringField('Search available widgets.')
    submit = SubmitField('Search')

class CreateWidget(FlaskForm):
    name = StringField('Widget Name',
                        validators=[DataRequired(message='Make it memorable!'),
                        Length(min=1, max=20, message='Widget name must be 1-20 characters.')])
    description = StringField('Description',
                        validators=[DataRequired(message='What will you share with the world?'), Length(max=50, message='Description limited to 50 characters :(')])
    # access_type = SelectField('New Member Accessibility', choices=[('public', 'Public'),
    #                                     ('private', 'Private'),
    #                                     ('secret', 'Secret')],
    #                                     validators=[DataRequired()])
    # post_type = SelectField('Who can post?', choices=[('public', 'Everyone'),
    #                                     ('admin', 'Only Me')],
    #                                     validators=[DataRequired()])
    create_widget_submit = SubmitField('Create My Widget')

    def validate_name(self, name):

        widget = Widget.query.filter_by(name=name.data).first()
        if widget:
            raise ValidationError(f'\"{name.data}\" is taken. Please choose another.')

class CreatePost(FlaskForm):
    # title = StringField('Post Title',
    #                     validators=[DataRequired()])
    content = StringField('What\'s on your mind?', validators=[DataRequired()])
    widget_target = SelectField('Post to Widget', choices=[], coerce=int)
    submit = SubmitField('Submit Post')

class CreateAddTeam(FlaskForm):
    user = StringField('Enter a netid', validators=[DataRequired()])
    add_remove = SelectField('Add or remove user?', choices = [('add', 'Add'), ('remove', 'Remove')])
    widget_target = SelectField('Widgets', choices=[], coerce=int)
    submit = SubmitField('Submit change')
    def validate_user(self, user):
        username = User.query.filter_by(netid=user.data).first()
        if username is None:
            raise ValidationError('You have entered an invalid user.')
        widget = Widget.query.filter_by(id = self.widget_target.data).first()
        if widget in username.widgets and self.add_remove.data == 'add':
            raise ValidationError('User is already subscribed to this widget.')
        if widget not in username.widgets and self.add_remove.data == 'remove':
            raise ValidationError('User is not subscribed to this widget.')
