from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, DateField, FieldList
from wtforms.validators import DataRequired

# Form di creazione nuovo corso
class NewCourse_Form(FlaskForm):
    name             = StringField('Nome del corso', validators=[DataRequired()])
    description      = TextAreaField('Descrizione')
    max_partecipants = IntegerField('Massimo numero di partecipanti')
    min_partecipants = IntegerField('Minimo numero di partecipanti')
    min_lessons      = IntegerField('Minimo numero di lezioni')
    duration         = IntegerField('Durata delle lezioni')
    category         = SelectField('Categoria', choices=[]) # Le categorie verranno aggiornate dinamicamente
    submit           = SubmitField('Conferma')

#Forms di creazione delle lezioni
class NewLesson_Form(FlaskForm):
    building         = SelectField('Edificio', choices =[])
    classroom        = SelectField('Aula', choices =[])
    mode             = SelectField('Modalità', choices=['Presenza','Online','Duale'])
    description      = TextAreaField('Descrizione')
    date             = DateField('Data')
    time             = SelectField('Orario', coerce = int, choices=[(0,'08:45'), (1,'10:30'), (2,'12:15'), (3,"14:00"), (4,"15:45"), (5,"17:30")])
    submit           = SubmitField('Conferma')
