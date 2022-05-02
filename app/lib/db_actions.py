from app import db, bcrypt
from sqlalchemy import exc
from .models import User, Student

def insert_user(form):
    try:
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(first_name=form.firstName.data, last_name=form.lastName.data, birth_date=form.dob.data, email=form.email.data)
        db.session().add(user)
        db.session.flush()

        student = Student(id_student=user.id_user, registration_date='2022-05-02', password=hashed_password)
        db.session().add(student)
        db.session.flush()

        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
