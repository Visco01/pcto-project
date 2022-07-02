from app import db, login_manager
from flask_login import UserMixin

db.Model.metadata.reflect(bind=db.engine, schema='pcto_db')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table__ = db.Model.metadata.tables['pcto_db.users']

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
