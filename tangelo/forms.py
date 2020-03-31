from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError
from tangelo.models import Widget
from tangelo.model_api import getValidWidgetsPost

class CreateWidget(FlaskForm):
    name = StringField('Widget Name',
                        validators=[DataRequired(message='Please provide a descriptive widget name'),
                        Length(min=2, max=30, message='Widget name must be 2-30 characters.')])
    description = StringField('Description',
                        validators=[DataRequired(), Length(max=200, message='Description limited to 200 characters :(')])
    access_type = SelectField('New Member Accessibility', choices=[('public', 'Public'),
                                        ('private', 'Private'),
                                        ('secret', 'Secret')],
                                        validators=[DataRequired()])
    post_type = SelectField('Who can post?', choices=[('public', 'All Widget Members'),
                                        ('admin', 'Me and Selected Admins')],
                                        validators=[DataRequired()])
    submit = SubmitField('Create My Widget')

    def validate_name(self, name):
        widget = Widget.query.filter_by(name=name.data).first()
        if widget:
            raise ValidationError('That widget name is taken. \
                                    Please choose a different one.')

class WidgetPost(FlaskForm):
    title = StringField('Post Title',
                        validators=[DataRequired()])
    body = StringField('Post Body', validators=[DataRequired()])
    widget_target = SelectField('Post to Widget', choices=getValidWidgetsPost(),
                                        validators=[DataRequired()])
    submit = SubmitField('Submit Post')
