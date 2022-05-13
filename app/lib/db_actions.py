from flask_login import current_user
from app import db, bcrypt
from sqlalchemy import exc
from datetime import date
from .models import User, Student, Teacher, Course, TeachersCourses, Category

def get_all_courses():
    categories = Category.query.all()
    res = []
    for category in categories:
        cat = []
        cat.append(category.c_name)
        coursesFromCategory = db.session.query(Course, User)\
                                        .filter(Course.id_course == TeachersCourses.id_course, Course.id_category == category.id_category)\
                                        .filter(TeachersCourses.id_teacher == User.id_user).all()
        cat.append(coursesFromCategory)
        res.append(cat)
    return res


def get_all_courses_from_teacher(id_user):
    return Course.query.join(TeachersCourses).filter(TeachersCourses.id_teacher==id_user).all()

def get_all_categories():
    return Category.query.all()

def insert_user(login_form):
    try:
        hashed_password = bcrypt.generate_password_hash(login_form.password.data).decode('utf-8')

        user = User(first_name=login_form.firstName.data, 
                    last_name=login_form.lastName.data, 
                    birth_date=login_form.dob.data, 
                    email=login_form.email.data)
        db.session().add(user)
        db.session.flush()

        student = Student(id_student=user.id_user, 
                          registration_date=date.today(),
                          password=hashed_password)
        db.session().add(student)
        db.session.flush()

        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()

        
def insert_course(form):
    try:
        newCourse = Course(c_name=form.name.data, 
                           description=form.description.data, 
                           creation_date=date.today(), 
                           max_partecipants=form.max_partecipants.data,
                           min_partecipants=form.min_partecipants.data,
                           min_lessons=form.min_lessons.data,
                           duration=form.duration.data,
                           id_category=form.category.data)
        db.session().add(newCourse)
        db.session.flush()

        teachers_courses = TeachersCourses(id_teacher=current_user.id_user,
                                           id_course=newCourse.id_course)
        db.session().add(teachers_courses)
        db.session.flush()

        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()



def get_user_by_email(email):
    return User.query.filter_by(email=email).first()
    
def get_student_by_id(id_user):
    return Student.query.filter_by(id_student=id_user).first()
