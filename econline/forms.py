from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, SubmitField
from wtforms.fields.html5 import TimeField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from econline.models import Admin, Election
from flask_login import current_user
from datetime import datetime


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
    
    
class NewAdminForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    
    def validate_username(self, email):
        user = Admin.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is not available')
            
            
class NewElectionForm(FlaskForm):
    name = StringField('Election Name', validators=[DataRequired(), Length(min=2, max=30)])
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.now())
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.now())
    start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()], default=datetime.now())
    end_time = TimeField('End Time', format='%H:%M', validators=[DataRequired()], default=datetime.now())
    
    def validate_name(self, name):
        election = Election.query.filter_by(name=name.data).first()
        if election:
            raise ValidationError('That Election already exists!')
            
    def validate_start_date(self, start_date):
        if start_date.data < datetime.date(datetime.now()):
            raise ValidationError('Choose a date in the future')
    
    def validate_end_date(self, end_date):
        if end_date.data < datetime.date(datetime.now()):
            raise ValidationError('Choose a date in the future')
            
    def validate_dates(self, start_date, end_date):
        if start_date.data < end_date.data:
            raise ValidationError('Please check the dates!')


class EditElectionNameForm(FlaskForm):
    name = StringField('Election Name', validators=[DataRequired(), Length(min=2, max=30)])
    submit_name = SubmitField('Submit Edit')
    
    def validate_name(self, name):
        election = Election.query.filter_by(name=name.data).first()
        if election:
            raise ValidationError('That Election already exists!')


class EditElectionDateForm(FlaskForm):
    start_date = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.now())
    end_date = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()], default=datetime.now())
    start_time = TimeField('Start Time', format='%H:%M', validators=[DataRequired()], default=datetime.now())
    end_time = TimeField('End Time', format='%H:%M', validators=[DataRequired()], default=datetime.now())
    submit_date = SubmitField('Submit Edit')
    
    def validate_start_date(self, start_date):
        if start_date.data < datetime.date(datetime.now()):
            raise ValidationError('Choose a date in the future')
    
    def validate_end_date(self, end_date):
        if end_date.data < datetime.date(datetime.now()):
            raise ValidationError('Choose a date in the future')
            
    def validate_dates(self, start_date, end_date):
        if start_date.data < end_date.data:
            raise ValidationError('Please check the dates!')
            

class AddCandidateForm(FlaskForm):
    name = StringField('Candidate Name', validators=[DataRequired(), Length(min=2, max=100)])
    portfolio = SelectField(u'Portfolio', choices=[('President', 'President'), ('Vice President', 'Vice Preisdent'), ('Treasurer', 'Treasurer')])
    image_file = FileField('Candidate Picture', validators=[FileAllowed(['jpg', 'png'])])
    campus = SelectField(u'Campus', choices=[('Main', 'Main Campus'), ('City', 'City Campus')])
    
    
class ImportVotersForm(FlaskForm):
    voters = FileField('Import Voters', validators=[DataRequired(), FileAllowed(['csv'])])
    submit_voters = SubmitField('Import')