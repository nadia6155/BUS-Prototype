from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, HiddenField, StringField, PasswordField, BooleanField, SelectField
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.datetime import DateField, TimeField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, EqualTo, NumberRange, ValidationError, Email, Optional, Length
from app import db
from app.models import User
import datetime


class ChooseForm(FlaskForm):
    choice = HiddenField('Choice')
    hobby_or_interest = HiddenField('either')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

def password_policy(form, field):
    message = """A password must be at least 8 characters long, and have an
                uppercase and lowercase letter, a digit, and a character which is
                neither a letter or a digit"""
    if len(field.data) < 8:
        raise ValidationError(message)
    flg_upper = flg_lower = flg_digit = flg_non_let_dig = False
    for ch in field.data:
        flg_upper = flg_upper or ch.isupper()
        flg_lower = flg_lower or ch.islower()
        flg_digit = flg_digit or ch.isdigit()
        flg_non_let_dig = flg_non_let_dig or not ch.isalnum()
    if not (flg_upper and flg_lower and flg_digit and flg_non_let_dig):
        raise ValidationError(message)

class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('', 'Select a role'), ('Admin', 'Admin'), ('Staff', 'Staff'), ('Student', 'Student')])
    phone = StringField('Phone Number', validators=[Optional()])
    password = PasswordField('Password', validators=[DataRequired(), password_policy])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    # def validate_username(form, field):
    #     q = db.select(User).where(User.username==field.data)
    #     if db.session.scalar(q):
    #         raise ValidationError("Username already taken, please choose another")

    def validate_email(form, field):
        q = db.select(User).where(User.email==field.data)
        if db.session.scalar(q):
            raise ValidationError("Email address already taken, please choose another")

class EditPersonalDetailsForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional()])
    age = IntegerField('Age', validators=[Optional()])
    emergency_name = StringField('Emergency Name', validators=[Optional()])
    emergency_phone = StringField('Emergency Contact Number', validators=[Optional()])
    submit = SubmitField('Submit')
    edit = HiddenField('Edit', default='-1')  # default = -1 means to CREATE/ADD


class AddHobbiesAndInterestsForm(FlaskForm):
    hobbies = SelectMultipleField('Select your hobbies', choices=[
                                                      ('Badminton', 'Badminton'),
                                                      ('Cooking', 'Cooking'),
                                                      ('Dancing', 'Dancing'),
                                                      ('Football', 'Football'),
                                                      ('Swimming', 'Swimming')], validators=[DataRequired()])

    interests = SelectMultipleField('Select your interests', choices=[
                                                          ('Public Speaking', 'Public Speaking'),
                                                          ('Blogging', 'Blogging'),
                                                          ('Vlogging', 'Vlogging'),
                                                          ('Reading', 'Reading'),
                                                          ('Photography', 'Photography')], validators=[DataRequired()])
    submit = SubmitField('Add Hobbies and Interests')

# meeting booking form
class ScheduleMeetingForm(FlaskForm):
    date = SelectField('Choose Date', choices=[], validators=[DataRequired()])
    time_slot = SelectField('Choose Time',choices=[('09:00 AM', '09:00 AM'),('10:00 AM', '10:00 AM'),('11:00 AM', '11:00 AM'),('12:00 PM', '12:00 PM'),('02:00 PM', '02:00 PM'),('03:00 PM', '03:00 PM')],validators=[DataRequired()])
    submit = SubmitField('Confirm Meeting')

# event calender form
class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    start_time = DateTimeLocalField('Start Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    end_time = DateTimeLocalField('End Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[Optional()])
    mode = SelectField('Mode', choices=[('Online', 'Online'), ('In-person', 'In-person')], validators=[DataRequired()])
    link = StringField('Online Link', validators=[Optional()])
    category = SelectField('Category', choices=[('University', 'University'), ('Society', 'Society'), ('Uni Support', 'Uni Support')], validators=[DataRequired()])
    submit = SubmitField('Add Event')
