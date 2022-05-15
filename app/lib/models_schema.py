from .models import User, Course
from app import ma

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    
class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course