from flask_wtf import FlaskForm
from wtforms import StringField, DateTimeField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo 

class RegistrationFrom(FlaskForm):
    firstName        = StringField('Nome', validators=[DataRequired()])
    lastName         = StringField('Cognome', validators=[DataRequired()])
    email            = EmailField('Email', validators=[DataRequired(), Email()])
    dob              = DateTimeField('Data di nascita', validators=[DataRequired()])
    password         = PasswordField('Password', validators=[DataRequired(), Length(min = 8)])
    confirm_password = PasswordField('Conferma password', validators=[DataRequired(), EqualTo('password')])
    submit           = SubmitField('Registrati')

class LoginForm(FlaskForm):
    email      = StringField('Email', validators=[DataRequired()])
    password   = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Ricordami')
    submit     = SubmitField('Accedi')