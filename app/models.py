import datetime
from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('username', db.String(30), unique=True, index=True)
    password = db.Column('password', db.String(60))
    email = db.Column('email', db.String(120), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.datetime.utcnow()

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False


class Child(db.Model):
    __tablename__ = 'children'
    child_id = db.Column('child_id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey("users.id"))
    child_name = db.Column('name', db.String(30))

    def __init__(self, user_id, child_name):
        self.user_id = user_id
        self.child_name = child_name


class Diaper(db.Model):
    __tablename__ = 'diapers'
    id = db.Column('diaper_id', db.Integer, primary_key=True)
    child_id = db.Column('child_id', db.Integer, db.ForeignKey("children.child_id"))
    date = db.Column('date', db.DateTime)
    size = db.Column('size', db.String(11))
    diaper_type = db.Column('type', db.String(4))

    def __init__(self, child_id, date, size, diaper_type):
        self.child_id = child_id
        self.date = date
        self.size = size
        self.diaper_type = diaper_type


class Bottle(db.Model):
    __tablename__ = 'bottles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    child_id = db.Column('child_id', db.Integer, db.ForeignKey("children.child_id"))
    date = db.Column('date', db.DateTime)
    amount = db.Column('amount', db.Integer)

    def __init__(self, child_id, date, amount):
        self.child_id = child_id
        self.date = date
        self.amount = amount


class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)
