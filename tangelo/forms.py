from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange
from tangelo.models import Widget, User

class CreateWidget(FlaskForm):
    name = StringField('Widget Name',
                        validators=[DataRequired(message='Make it memorable!'),
                        Length(min=1, max=25, message='Widget name must be 1-25 characters.')],
                        render_kw={'maxlength': 25})
    description = StringField('Description',
                        validators=[DataRequired(message='What will you share with the world?'), Length(max=60, message='Description limited to 60 characters :(')], render_kw={'maxlength': 60})
    create_widget_submit = SubmitField('Create My Widget')

    def validate_name(self, name):
        proposed_name = name.data.strip()
        if not proposed_name:
            raise ValidationError(f'\"{proposed_name}\" must not be empty.')
        widget = Widget.query.filter(Widget.name.ilike(proposed_name)).first()
        if widget:
            raise ValidationError(f'\"{proposed_name}\" is taken.')
