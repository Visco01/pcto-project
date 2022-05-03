from app import db, bcrypt
from sqlalchemy import exc
from datetime import date
from .models import User, Student

def insert_user(form):
    try:
        encoded = form.password.data.encode('utf-8')
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        user = User(first_name=form.firstName.data, last_name=form.lastName.data, birth_date=form.dob.data, email=form.email.data)
        db.session().add(user)
        db.session.flush()

        student = Student(id_student=user.id_user, registration_date=date.today(), password=hashed_password)
        db.session().add(student)
        db.session.flush()

        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()


def get_user_by_email(form):
    user = User.query.filter_by(email=form.email.data).first()

    if(not user):
        return False
    else:
        return user


def get_student(user):
        student = Student.query.filter_by(id_student=user.id_user).first()
        return student
