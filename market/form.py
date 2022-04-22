from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, DataRequired, ValidationError
from market.models import User

class RegistrationForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist!')

    def validate_email(self, email_to_check):
        email_add = User.query.filter_by(email=email_to_check.data).first()
        if email_add:
            raise ValidationError('Email Address already exist!')

    fullname = StringField(label='Full Name', validators=[Length(min=5, max=55), DataRequired()])
    username = StringField(label='Username', validators=[Length(min=5, max=25), DataRequired()])
    email = StringField(label='Valid Email Address', validators=[Email(), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6, max=18), DataRequired()])
    budget = StringField(label='Budget', validators=[DataRequired()])
    submit = SubmitField(label='Register')


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')

class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Confirm Purchase')

class SellItemForm(FlaskForm):
    submit = SubmitField(label='Confirm Sell')

