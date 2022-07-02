from .models import Classroom, User, Course
from app import ma

#utility utilizzata per rendere serializzabili le classi ORM

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course

class ClassroomSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Classroom
