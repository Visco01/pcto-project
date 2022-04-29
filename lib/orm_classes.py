from sqlalchemy import *
import enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import exc
from conn import get_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id_user = Column(Integer, primary_key = true)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(Date)
    email = Column(String)
    teacher = relationship("Teacher", back_populates='user', uselist=False,  cascade="all, delete, delete-orphan")
    student = relationship("Student", back_populates='user', uselist=False,  cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User(id_user='%d', first_name='%s', last_name='%s')>" % (self.id_user, self.first_name, self.last_name)


class Teacher(Base):
    __tablename__ = 'teachers'

    id_teacher = Column(Integer, ForeignKey(User.id_user), primary_key=True)
    user = relationship("User", back_populates='teacher')
    courses = relationship('TeachersCourses', secondary = 'teachers_courses')


class Student(Base):
    __tablename__ = 'students'

    id_student = Column(Integer, ForeignKey(User.id_user), primary_key=True)
    registration_date = Column(Date)
    password = Column(String)
    user = relationship("User", back_populates='student')
    certificates = relationship('Certificate', secondary = 'certificates')
    courses = relationship('StudentsCourses', secondary = 'students_courses')
    lessons = relationship('StudentsLessons', secondary = 'students_lessons')
    surveys = relationship('Surveys', secondary = 'surveys')


class Category(Base):
    __tablename__ = 'categories'

    id_category = Column(Integer, primary_key=True)
    c_name = Column(String)
    courses = relationship("Course", foreign_keys=lambda: Course.id_category)


class Course(Base):
    __tablename__ = 'courses'

    id_course = Column(Integer, primary_key=True)
    c_name = Column(String)
    description = Column(String)
    creation_date = Column(Date)
    max_partecipants = Column(Integer)
    min_partecipants = Column(Integer)
    min_lessons = Column(Integer)
    duration = Column(Integer)
    id_category = Column(Integer, ForeignKey(Category.id_category))
    certificates = relationship('Certificate', secondary = 'certificates')
    lessons = relationship('Lesson', foreign_keys=lambda: Lesson.id_course)
    students = relationship('StudentsCourses', secondary = 'students_courses')
    surveys = relationship('Surveys', secondary = 'surveys')
    teachers = relationship('TeachersCourses', secondary = 'teachers_courses')

class Building(Base):
    __tablename__ = 'buildings'

    id_building = Column(Integer, primary_key=True)
    b_name = Column(Integer)
    classrooms = relationship("Classroom", foreign_keys=lambda: Classroom.id_building)

class Certificate(Base):
    __tablename__ = 'certificates'

    id_certificate = Column(Integer, primary_key=True)
    certification_date = Column(Date)
    id_student = Column(Integer, ForeignKey(Student.id_student))
    id_course = Column(Integer, ForeignKey(Course.id_course))


class Classroom(Base):
    __tablename__ = 'classrooms'

    id_classroom = Column(Integer, primary_key=True)
    c_name = Column(String)
    capacity = Column(Integer)
    id_building = Column(Integer, ForeignKey(Building.id_building))
    lessons = relationship('Lesson', foreign_keys=lambda: Lesson.id_classroom)


class LessonMode(enum.Enum):
    one = 'online'
    two = 'presence'
    three = 'both'


class Lesson(Base):
    __tablename__ = 'lessons'

    id_lesson = Column(Integer, primary_key=True)
    token = Column(Integer)
    l_date = Column(Date)
    description = Column(String)
    mode = Column(Enum(LessonMode))
    id_course = Column(Integer, ForeignKey(Course.id_course))
    id_classroom = Column(Integer, ForeignKey(Classroom.id_classroom))
    students = relationship('StudentsLessons', secondary = 'students_lessons')

class StudentsCourses(Base):
    __tablename__ = 'students_courses'

    id_student = Column(Integer, ForeignKey(Student.id_student), primary_key=True)
    id_course = Column(Integer, ForeignKey(Course.id_course), primary_key=True)
    registration_date = Column(Date)


class StudentsLessons(Base):
    __tablename__ = 'students_lessons'

    id_student = Column(Integer, ForeignKey(Student.id_student), primary_key=True)
    id_lesson = Column(Integer, ForeignKey(Lesson.id_lesson), primary_key=True)


class Surveys(Base):
    __tablename__ = 'surveys'

    id_survey = Column(Integer, primary_key=True)
    vote = Column(Integer)
    description = Column(String)
    id_student = Column(Integer, ForeignKey(Student.id_student))
    id_course = Column(Integer, ForeignKey(Course.id_course))


class TeachersCourses(Base):
    __tablename__ = 'teachers_courses'

    id_teacher = Column(Integer, ForeignKey(Teacher.id_teacher), primary_key=True)
    id_course = Column(Integer, ForeignKey(Course.id_course), primary_key=True)

#da verificare la correttezza delle relazioni
