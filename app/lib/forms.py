from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, EmailField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .db_actions import get_user_by_email
class RegistrationFrom(FlaskForm):
    firstName        = StringField('Nome', validators=[DataRequired()])
    lastName         = StringField('Cognome', validators=[DataRequired()])
    email            = EmailField('Email', validators=[DataRequired(), Email()])
    dob              = DateField('Data di nascita', validators=[DataRequired()])
    password         = PasswordField('Password', validators=[DataRequired(), Length(min = 8)])
    confirm_password = PasswordField('Conferma password', validators=[DataRequired(), EqualTo('password')])
    submit           = SubmitField('Registrati')

    def validate_email(self, email):
        user = get_user_by_email(email.data)
        if user:
            raise ValidationError('Email già registrata')
class LoginForm(FlaskForm):
    email      = StringField('Email', validators=[DataRequired(), Email()])
    password   = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Ricordami')
    submit     = SubmitField('Accedi')

class LoginFormProf(FlaskForm):
    login    = StringField('??', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit   = SubmitField('Accedi')

class newCourseForm(FlaskForm):
    name             = StringField('Nome del corso', validators=[DataRequired()])
    description      = StringField('Descrizione')
    max_partecipants = IntegerField('Massimo numero di partecipanti')
    min_partecipants = IntegerField('Minimo numero di partecipanti')
    min_lessons      = IntegerField('Minimo numero di lezioni')
    duration         = IntegerField('Durata delle lezioni')
    category         = SelectField('Categoria', choices=[])
    submit           = SubmitField('Crea')