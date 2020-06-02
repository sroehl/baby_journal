import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

PROD = True

SQLALCHEMY_TRACK_MODIFICATIONS = False

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.getenv("BABY_DB_LOC"))
SQLALCHEMY_ECHO = False
