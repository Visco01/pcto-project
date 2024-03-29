from functools import wraps
from app.lib.db_actions import *
from flask import redirect


def teacher_required(f):
    """Garantisce che l'utente che ha effettuato il login sia un professore"""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if get_student_by_id(current_user.id_user):
            return redirect('/student/dashboard', code=302)
        return f(*args, **kwargs)
    return decorated_function
