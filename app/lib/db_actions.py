from app import db, bcrypt
from sqlalchemy import exc
from datetime import date
from .models import User, Student, Teacher, Course, TeachersCourses, Category

def get_all_course():
    return Course.query.all()

def get_all_courses_from_teacher(id_user):
    return Course.query.join(TeachersCourses).filter(TeachersCourses.id_teacher==id_user).all()

def get_all_categories():
    return Category.query.all()

def insert_user(login_form):
    try:
        # encoded = form.password.data.encode('utf-8')
        hashed_password = bcrypt.generate_password_hash(login_form.password.data).decode('utf-8')

        user = User(first_name=login_form.firstName.data, last_name=login_form.lastName.data, birth_date=login_form.dob.data, email=login_form.email.data)
        db.session().add(user)
        db.session.flush()

        student = Student(id_student=user.id_user, registration_date=date.today(), password=hashed_password)
        db.session().add(student)
        db.session.flush()

        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()
    
def get_student_by_id(id_user):
    return Student.query.filter_by(id_student=id_user).first()
