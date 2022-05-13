from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired

# Form di creazione nuovo corso
class NewCourseForm(FlaskForm):
    name             = StringField('Nome del corso', validators=[DataRequired()])
    description      = TextAreaField('Descrizione')
    max_partecipants = IntegerField('Massimo numero di partecipanti')
    min_partecipants = IntegerField('Minimo numero di partecipanti')
    min_lessons      = IntegerField('Minimo numero di lezioni')
    duration         = IntegerField('Durata delle lezioni')
    category         = SelectField('Categoria', choices=[]) # Le categorie verranno aggiornate dinamicamente
    submit           = SubmitField('Conferma')