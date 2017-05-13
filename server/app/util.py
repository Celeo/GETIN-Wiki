from functools import wraps

from flask import request
from flask_restful import abort
from jose import jwt

from .shared import config
from .models import User


def get_user_from_token():
    try:
        token = request.headers['Authorization']
        token_data = jwt.decode(token, config['SECRET_KEY'])
        return User.query.filter_by(name=token_data['name']).first()
    except:
        return None


def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            if get_user_from_token():
                return f(*args, **kwargs)
            abort(401)
        except:
            abort(401)
    return wrapper


def restrict_editor(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            user = get_user_from_token()
            if user and (user.editor or user.admin):
                return f(*args, **kwargs)
            abort(401)
        except:
            abort(401)
    return wrapper


def restrict_admin(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            user = get_user_from_token()
            if user and user.admin:
                return f(*args, **kwargs)
            abort(401)
        except:
            abort(401)
    return wrapper
