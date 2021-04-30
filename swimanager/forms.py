from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, DateTimeField, SelectField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import DateField


class LoginForm(FlaskForm):
    email = StringField('Email', render_kw={"placeholder": "myname@example.com"},
        validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log in')

class NewMeetForm(FlaskForm):
    meet_name = SelectField('Meet Type', choices = [('IF','Inter-Faculty'),
                            ('IFF','Inter-Faculty Freshers')], validators = [DataRequired()])
    start_date = DateField('Date', format='%Y-%m-%d', render_kw={"placeholder": "mm/dd/yyyy"})
    # end_date = DateField('End Date', format='%Y-%m-%d', render_kw={"placeholder": "mm/dd/yyyy"})
    location = SelectField('Location', choices = [('ncc','NCC Pool'),
                            ('police','Police Pool Complex, Narahenpita'),
                            ('ananda','Ananda College Pool'),
                            ('thurstan','Thurstan College Pool'),
                            ('royal','Royal College Pool'),
                            ('nalanda','Nalanda College Pool'),
                            ('ssc','SSC pool')], validators=[DataRequired()])
    ucscm = BooleanField('UCSC')
    medm = BooleanField('Faculty of Medicine')
    scim = BooleanField('Faculty of Science')
    mgtm = BooleanField('Faculty of Management')
    tecm = BooleanField('Faculty of Technology')
    nurm = BooleanField('Faculty of Nursing')
    srim = BooleanField('Sripalee')
    lawm = BooleanField('Faculty of Law')
    artm = BooleanField('Faculty of Arts')
    ucscl = BooleanField('UCSC')
    medl = BooleanField('Faculty of Medicine')
    scil = BooleanField('Faculty of Science')
    mgtl = BooleanField('Faculty of Management')
    tecl = BooleanField('Faculty of Technology')
    nurl = BooleanField('Faculty of Nursing')
    sril = BooleanField('Sripalee')
    lawl = BooleanField('Faculty of Law')
    artl = BooleanField('Faculty of Arts')
    submit = SubmitField('Create Meet')

