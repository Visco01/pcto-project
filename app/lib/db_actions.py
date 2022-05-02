from app import db
from sqlalchemy import exc

def insert_user(user):
    try:
        db.session().add(user)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(type(e))
        db.session.rollback()
