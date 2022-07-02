from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, EmailField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.lib.db_actions import get_user_by_email
import re

#Form di registrazione
class Registration_Form(FlaskForm):
    firstName        = StringField('Nome', validators=[DataRequired()])
    lastName         = StringField('Cognome', validators=[DataRequired()])
    email            = EmailField('Email', validators=[DataRequired(), Email()])
    dob              = DateField('Data di nascita', validators=[DataRequired()])
    password         = PasswordField('Password', validators=[DataRequired(), Length(min = 8)])
    confirm_password = PasswordField('Conferma password', validators=[DataRequired(), EqualTo('password')])
    category         = SelectField('Categoria', choices=['Studente', 'Professore'])
    submit           = SubmitField('Registrati')

    #Validazione personalizzata della email
    def validate_email(self, email):
        user = get_user_by_email(email.data)
        if user:
            raise ValidationError('Email già registrata')

    #Validazione personalizzata del dominio delle email tramite regex
    def validate(self):
        rv = FlaskForm.validate(self)

        if self.category.data == 'Professore' and re.search('^[A-Za-z0-9._%+-]+@(?!unive.it)[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$', self.email.data):
            self.email.errors.append('Email non valida per un professore')
            return False
        return rv

#Form di login
class Login_Form(FlaskForm):
    email      = StringField('Email', validators=[DataRequired(), Email()])
    password   = PasswordField('Password', validators=[DataRequired()])
    submit     = SubmitField('Accedi')
