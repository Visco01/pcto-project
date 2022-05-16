from flask_login import current_user
from app import db, bcrypt
from sqlalchemy import exc, update
from datetime import date
from .models import StudentsCourses, User, Student, Teacher, Course, TeachersCourses, Category

def get_all_courses():
    categories = Category.query.all()
    res = []
    for category in categories:
        cat = []
        cat.append(category)
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


def is_student_already_subscribed(id_student, id_course):
    query = StudentsCourses.query.filter(StudentsCourses.id_student == id_student,
                                         StudentsCourses.id_course == id_course).first()
    if(query):
        return True
    else:
        return False


def insert_course_subscription(id_student, id_course):
    try:
        newStudentsCourses = StudentsCourses(id_student=id_student,
                                             id_course=id_course,
                                             registration_date=date.today())

        db.session().add(newStudentsCourses)
        db.session.flush()
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
        
def get_course_by_id(id_course):
    return Course.query.filer_by(id_course=id_course).first()

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()
    
def get_student_by_id(id_user):
    return Student.query.filter_by(id_student=id_user).first()

def get_course_by_id(id_course):
    return Course.query.filter(Course.id_course == id_course).first()

#ritorna ID dei studenti iscritti ad un corso
def get_subscribed_students(id_course):
    return db.session.query(StudentsCourses.id_student).select_from(StudentsCourses).filter(StudentsCourses.id_course == id_course).all()

def get_course_professor(id_course):
    query1 = TeachersCourses.query.filter(TeachersCourses.id_course == id_course).all()
    return User.query.filter(User.id_user == query1[0].id_teacher).first()


def update_course_description(id, descript):
    try:
        db.session.execute(
            update(Course).
            where(Course.id_course == id).
            values(description = descript)
        )
        db.session.flush()
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()


def update_course_name(id,tittle):
    try:
        db.session.execute(
            update(Course).
            where(Course.id_course == id).
            values(c_name = tittle)
        )
        db.session.flush()
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()