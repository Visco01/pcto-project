from flask_login import current_user
from app import db, bcrypt
from sqlalchemy import exc, update
from datetime import date, timedelta
from .models import Classroom, Lesson, StudentsCourses, User, Student, Teacher, Course, TeachersCourses, Category, Token, Building
from key_generator.key_generator import generate
import datetime

TIMES = {0:datetime.time(8,45), 1:datetime.time(10,30), 2:datetime.time(12,15),3:datetime.time(14,0),4:datetime.time(15,45),5:datetime.time(17,30)} #Dizzionario costante per l'ora delle lezioni

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


def get_courses_by_student(id_student):
    coursesFromStudents = db.session.query(Course)\
                                    .filter(Course.id_course == StudentsCourses.id_course, StudentsCourses.id_student == id_student).all()

    # print(coursesFromStudents)
    return coursesFromStudents


def get_all_courses_from_teacher(id_user):
    return db.session.query(Course,Category).filter(TeachersCourses.id_teacher == id_user, Category.id_category == Course.id_category)


def get_all_categories():
    return Category.query.all()


def insert_user(login_form):
    try:
        hashed_password = bcrypt.generate_password_hash(login_form.password.data).decode('utf-8')

        user = User(first_name=login_form.firstName.data,
                    last_name=login_form.lastName.data,
                    birth_date=login_form.dob.data,
                    email=login_form.email.data,
                    password=hashed_password,
                    registration_date=date.today())
        db.session().add(user)
        db.session.flush()

        if login_form.category.data == 'Studente':
            student = Student(id_student=user.id_user)
            db.session().add(student)
        else:
            teacher = Teacher(id_teacher=user.id_user)
            db.session().add(teacher)

        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()


def insert_token(token, email):
    try:
        db.session.add(Token(token=token, email=email))
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()


def set_user_active(token):
    try:
        # Cerco il token ed abilito l'utente
        user = db.session.query(User).filter(Token.token == token, User.email == Token.email).first()
        user.is_active = True
        db.session.flush()
        # elimino il token non più necessario
        if user.is_active:
            Token.query.filter(Token.token == token).delete()

        db.session.commit()

        return user.is_active
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
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()


def delete_course_subscription(id_student, id_course):
     try:
        studentCourse = StudentsCourses.query.filter(StudentsCourses.id_student == id_student, StudentsCourses.id_course == id_course).first()
        # print(studentCourse)
        db.session.delete(studentCourse)
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


def get_subscribed_students(id_course):
    return db.session.query(StudentsCourses.id_student).select_from(StudentsCourses).filter(StudentsCourses.id_course == id_course).all()


def get_subscribed_students_data(id_course):
    return db.session.query(Student.id_student, User.first_name, User.last_name, User.email).filter(StudentsCourses.id_course == id_course, StudentsCourses.id_student == Student.id_student, Student.id_student == User.id_user ).all()


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


def update_course(id,data):
    temp = get_category_id_by_name(data["category"])
    try:
        db.session.execute(
            update(Course).
            where(Course.id_course == id).
            values(c_name = data["tittle"],
                   description = data["description"],
                   min_partecipants = data["min_subscribers"],
                   max_partecipants = data["max_subscribers"],
                   duration = data["lesson_duration"],
                   id_category = temp.id_category
                   )
        )
        db.session.flush()
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()


def get_course_category(id_course):
    return Category.query.join(Course).filter(Course.id_course == id_course).first()


def get_category_id_by_name(name):
    return Category.query.filter(Category.c_name == name).first()


def get_classrooms_by_capacity(course_capacity):
    # result = Classroom.query.filter(Classroom.capacity >= course_capacity, Classroom.capacity <= course_capacity + 5).all()
    # if len(result) == 0:
    return Classroom.query.filter(Classroom.capacity >= course_capacity).all()


def insert_lesson(form, course_id):
    key = generate(1,4,4,type_of_value = 'int').get_key()

    date = form.date.data
    time = TIMES[form.time.data]
    lesson_datetime = datetime.datetime(year=date.year, day = date.day,month= date.month, hour=time.hour, minute=time.minute)

    newLesson = Lesson(
        description = form.description.data,
        l_date = lesson_datetime,
        mode = form.mode.data,
        id_classroom = form.classroom.data,
        token = int(key),
        id_course = course_id
    )
    try:
        db.session.add(newLesson)
        db.session.flush()
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        db.session.rollback()


#Controlla la sovrapposizione delle lezioni
def check_lesson_availability(form):
    date = form.date.data
    time = TIMES[form.time.data]
    lesson_datetime = datetime.datetime(year=date.year, day = date.day,month= date.month, hour=time.hour, minute=time.minute)
    classroom = form.classroom.data

    lessons = Lesson.query.all()

    for lesson in lessons:
        if lesson_datetime == lesson.l_date and classroom == lesson.id_classroom:
            return False

    return True


def get_course_lessons(id_course):
        return db.session.query(Lesson,Classroom,Building).filter(Lesson.id_course == id_course, Lesson.id_classroom == Classroom.id_classroom, Classroom.id_building == Building.id_building).order_by(Lesson.l_date.asc()).all()


def get_classrooms_from_building(id):
    return Classroom.query.filter(Classroom.id_building == id).all()


def get_building_from_classroom(id_building):
    building = Building.query.filter(Building.id_building == id_building).first()
    if building is not None:

        return True

    return False


def get_building_from_lesson(id_course):
    first_lesson = Lesson.query.filter(Lesson.id_course == id_course).order_by(Lesson.l_date.asc()).first()

    if first_lesson is None:
        return None

    classroom = Classroom.query.filter(Classroom.id_classroom == first_lesson.id_classroom).first()
    building = Building.query.filter(Building.id_building == classroom.id_building).first()

    return building
