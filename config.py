import os
import secrets

base = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    TESTING = True
    DEBUG = False
    SECRET_KEY = secrets.token_hex(10)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(base, 'app.db')
    # SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

