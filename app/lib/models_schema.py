from .models import Classroom, User, Course
from app import ma

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    
class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course
        
class ClassroomSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Classroom