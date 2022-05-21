from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, DateField, FieldList
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

class NewLessonForm(FlaskForm):
    mode             = SelectField('Modalita', choices=['online','presence','both'])
    description      = TextAreaField('Descrizione')
    date             = DateField('Data')
    classroom        = SelectField('Aula', choices =[])
    submit_single    = SubmitField('Conferma')


class NewScheduleForm(FlaskForm):
    date_m           = DateField('Data inizio')
    #day_m            = SelectField('Seleziona giorni settimana:', coerce = int, choices=[(-1,'none'),(0,'Lunedi'),(1,'Martedi'),(2,'Mercoledi'),(3,'Giovedi'),(4,'Venerdi')])
    days             = FieldList(SelectField('Seleziona giorni settimana:', coerce = int, choices=[(-1,'none'),(0,'Lunedi'),(1,'Martedi'),(2,'Mercoledi'),(3,'Giovedi'),(4,'Venerdi')]))
    description_m    = TextAreaField('Descrizione generale')
    classroom_m      = SelectField('Aula', choices =[])
    mode_m           = SelectField('Modalita', choices=['online','presence','both'])
    number_m         = IntegerField('Numero totale lezione')
    submit           = SubmitField('Conferma')