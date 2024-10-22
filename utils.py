import re
import jwt
import datetime
from flask import current_app

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def create_jwt_token(username):
    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_jwt_token(token):
    return jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
