
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Email,EqualTo
class ContactForm(FlaskForm):
    fullname = StringField(validators=[DataRequired(message='fullname should be more than 5 characters'), Length(min=5)])
    email = StringField(Email, validators=[Email()])
    message = TextAreaField()
    submit= SubmitField('Submit')
class SignupForm(FlaskForm):
    firstname = StringField(validators=[DataRequired(message='firstname is required')])
    lastname = StringField(validators=[DataRequired(message='lastname is required')])
    useremail = StringField(Email, validators=[Email()])
    password = PasswordField(validators=[DataRequired(message='Please enter your password')])
    confirmpassword = PasswordField(validators=[EqualTo('password')])
    submit= SubmitField('Submit')
    