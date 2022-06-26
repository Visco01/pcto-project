from app import db, login_manager
from flask_login import UserMixin

db.Model.metadata.reflect(bind=db.engine, schema='pcto_db')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['pcto_db.users']

    # override metodo get_id() di UserMixin
    def get_id(self):
        return (self.id_user)


class Student(db.Model):
    __table__ = db.Model.metadata.tables['pcto_db.students']


class Teacher(db.Model):
    __table__ = db.Model.metadata.tables['pcto_db.teachers']


class Category(db.Model):
    __table__ = db.Model.metadata.tables['pcto_db.categories']


class Course(db.Model):
    __table__ = db.Model.metadata.tables['pcto_db.courses']


class Building(db.Model):
    __table__ = db.Model.metadata.tables['pcto_db.buildings']


class Certificate(db.Model):
    __table__ = db.Model.metadata.tables['pcto_db.certificates']


class Classroom(db.Model):
    __table__ = db.Model.metadata.tables['pcto_db.classrooms']


class Lesson(db.Model):
    __table__ = db.Model.metadata.tables['pcto_db.lessons']


class StudentsCourses(db.Model):
    __table__ = db.Model.metadata.tables['pcto_db.students_courses']


class StudentsLessons(db.Model):
    __table__ = db.Model.metadata.tables['pcto_db.students_lessons']


class Surveys(db.Model):
    __table__ = db.Model.metadata.tables['pcto_db.surveys']


class TeachersCourses(db.Model):
    __table__ = db.Model.metadata.tables['pcto_db.teachers_courses']

class Token(db.Model):
    __table__ = db.Model.metadata.tables['pcto_db.tokens']


'''
class User(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    email = db.Column(db.String)
    #teacher = db.relationship("Teacher", back_populates='user', uselist=False,  cascade="all, delete, delete-orphan")
    #student = db.relationship("Student", back_populates='user', uselist=False,  cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User(id_user='%d', first_name='%s', last_name='%s')>" % (self.id_user, self.first_name, self.last_name)

class Teacher(db_model):
    __tablename__ = 'teachers'

    id_teacher = db.Column(db.Integer, db.ForeignKey(User.id_user), primary_key=True)
    user = db.relationship("User", back_populates='teacher')
    courses = db.relationship('TeachersCourses', secondary = 'teachers_courses')


class Student(db_model):
    __tablename__ = 'students'

    id_student = db.Column(db.Integer, db.ForeignKey(User.id_user), primary_key=True)
    registration_date = db.Column(db.Date)
    password = db.Column(db.String)
    user = db.relationship("User", back_populates='student')
    certificates = db.relationship('Certificate', secondary = 'certificates')
    courses = db.relationship('StudentsCourses', secondary = 'students_courses')
    lessons = db.relationship('StudentsLessons', secondary = 'students_lessons')
    surveys = db.relationship('Surveys', secondary = 'surveys')


class Category(db_model):
    __tablename__ = 'categories'

    id_category = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String)
    courses = db.relationship("Course", foreign_keys=lambda: Course.id_category)


class Course(db_model):
    __tablename__ = 'courses'

    id_course = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String)
    description = db.Column(db.String)
    creation_date = db.Column(db.Date)
    max_partecipants = db.Column(db.Integer)
    min_partecipants = db.Column(db.Integer)
    min_lessons = db.Column(db.Integer)
    duration = db.Column(db.Integer)
    id_category = db.Column(db.Integer, db.ForeignKey(Category.id_category))
    certificates = db.relationship('Certificate', secondary = 'certificates')
    lessons = db.relationship('Lesson', foreign_keys=lambda: Lesson.id_course)
    students = db.relationship('StudentsCourses', secondary = 'students_courses')
    surveys = db.relationship('Surveys', secondary = 'surveys')
    teachers = db.relationship('TeachersCourses', secondary = 'teachers_courses')


class Building(db_model):
    __tablename__ = 'buildings'

    id_building = db.Column(db.Integer, primary_key=True)
    b_name = db.Column(db.Integer)
    classrooms = db.relationship("Classroom", foreign_keys=lambda: Classroom.id_building)


class Certificate(db_model):
    __tablename__ = 'certificates'

    id_certificate = db.Column(db.Integer, primary_key=True)
    certification_date = db.Column(db.Date)
    id_student = db.Column(db.Integer, db.ForeignKey(Student.id_student))
    id_course = db.Column(db.Integer, db.ForeignKey(Course.id_course))


class Classroom(db_model):
    __tablename__ = 'classrooms'

    id_classroom = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String)
    capacity = db.Column(db.Integer)
    id_building = db.Column(db.Integer, db.ForeignKey(Building.id_building))
    lessons = db.relationship('Lesson', foreign_keys=lambda: Lesson.id_classroom)


class LessonMode(enum.Enum):
    one = 'online'
    two = 'presence'
    three = 'both'


class Lesson(db_model):
    __tablename__ = 'lessons'

    id_lesson = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Integer)
    l_date = db.Column(db.Date)
    description = db.Column(db.String)
    mode = db.Column(db.Enum(LessonMode))
    id_course = db.Column(db.Integer, db.ForeignKey(Course.id_course))
    id_classroom = db.Column(db.Integer, db.ForeignKey(Classroom.id_classroom))
    students = db.relationship('StudentsLessons', secondary = 'students_lessons')

class StudentsCourses(db_model):
    __tablename__ = 'students_courses'

    id_student = db.Column(db.Integer, db.ForeignKey(Student.id_student), primary_key=True)
    id_course = db.Column(db.Integer, db.ForeignKey(Course.id_course), primary_key=True)
    registration_date = db.Column(db.Date)


class StudentsLessons(db_model):
    __tablename__ = 'students_lessons'

    id_student = db.Column(db.Integer, db.ForeignKey(Student.id_student), primary_key=True)
    id_lesson = db.Column(db.Integer, db.ForeignKey(Lesson.id_lesson), primary_key=True)


class Surveys(db_model):
    __tablename__ = 'surveys'

    id_survey = db.Column(db.Integer, primary_key=True)
    vote = db.Column(db.Integer)
    description = db.Column(db.String)
    id_student = db.Column(db.Integer, db.ForeignKey(Student.id_student))
    id_course = db.Column(db.Integer, db.ForeignKey(Course.id_course))


class TeachersCourses(db_model):
    __tablename__ = 'teachers_courses'

    id_teacher = db.Column(db.Integer, db.ForeignKey(Teacher.id_teacher), primary_key=True)
    id_course = db.Column(db.Integer, db.ForeignKey(Course.id_course), primary_key=True)

#da verificare la correttezza delle relazioni
'''
