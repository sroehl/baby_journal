WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

PROD = False

SQLALCHEMY_TRACK_MODIFICATIONS = False
if PROD:
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@db:3306/baby_journal'
else:
  SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@db-dev:3306/baby_journal'

if PROD:
  CELERY_BROKER_URL = 'redis://redis:6379/0'
  CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
else:
  CELERY_BROKER_URL = 'redis://redis-dev:6379/0'
  CELERY_RESULT_BACKEND = 'redis://redis-dev:6379/0'
