import sqlalchemy
from sqlalchemy import *
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
    teacher = relationship("Teacher", back_populates='user', uselist=True,  cascade="all, delete, delete-orphan")
    student = relationship("Student", back_populates='user', uselist=True,  cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<User(id_user='%d', first_name='%s', last_name='%s')>" % (self.id_user, self.first_name, self.last_name)


class Teacher(Base):
    __tablename__ = 'teachers'

    id_teacher = Column(Integer, ForeignKey(User.id_user), primary_key=True)
    user = relationship("User", back_populates='teacher')


class Student(Base):
    __tablename__ = 'students'

    id_student = Column(Integer, ForeignKey(User.id_user), primary_key=True)
    registration_date = Column(Date)
    password = Column(String)
    user = relationship("User", back_populates='student')


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

#mancano le restanti tabelle


'''

TEST INSERIMENTO CORSO (CON CATEGORIA GIà CREATA) -> FUNZIONA

Category.__tablename__
Course.__tablename__
engine = get_engine()
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)

test_course = Course(c_name='PO1', description='DESC', creation_date='2022-04-23',
                     max_partecipants=30, min_partecipants=10, min_lessons=3,
                     duration=20, id_category=1)

try:
    session.add(test_course)
    session.commit()
except exc.SQLAlchemyError as e:
    session.rollback()
finally:
    session.close()
'''
