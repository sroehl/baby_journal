import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

PROD = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
if PROD:
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@db:3306/baby_journal'
else:
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@db-dev:3306/baby_journal'
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.getenv("BABY_DB_LOC"))
SQLALCHEMY_ECHO = True
