import datetime
from app import db, app
from itsdangerous import Serializer


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column('username', db.String(30), unique=True, index=True)
    password = db.Column('password', db.String(60))
    email = db.Column('email', db.String(120), unique=True, index=True)
    registered_on = db.Column('registered_on', db.DateTime)
    api_key = db.Column('api_key', db.String(30))

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

    def generate_auth_token(self):
        s = Serializer(app.config['SECRET_KEY'])
        token = s.dumps({'id': self.id}).split(".")[1]
        self.api_key = token
        return token


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
    diaper_size = db.Column('diaper_size', db.Integer)
    diaper_type = db.Column('type', db.String(4))

    def __init__(self, child_id, date, size, diaper_type, diaper_size):
        self.child_id = child_id
        self.date = date
        self.size = size
        self.diaper_type = diaper_type
        self.diaper_size = diaper_size

    @property
    def serialize(self):
        return {'id': self.id,
                'child_id': self.child_id,
                'date': self.date,
                'diaper_type': self.diaper_type,
                'diaper_size': self.size}


class Bottle(db.Model):
    __tablename__ = 'bottles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    child_id = db.Column('child_id', db.Integer, db.ForeignKey("children.child_id"))
    date = db.Column('date', db.DateTime)
    amount = db.Column('amount', db.Float)

    def __init__(self, child_id, date, amount):
        self.child_id = child_id
        self.date = date
        self.amount = amount

    @property
    def serialize(self):
        return {'id': self.id,
                'child_id': self.child_id,
                'date': self.date,
                'amount': self.amount}

class Food(db.Model):
    __tablename__ = 'food'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    child_id = db.Column('child_id', db.Integer, db.ForeignKey("children.child_id"))
    date = db.Column('date', db.DateTime)
    name = db.Column('name', db.String(30))

    def __init__(self, child_id, date, name):
        self.child_id = child_id
        self.date = date
        self.name = name

    @property
    def serialize(self):
        return {'id': self.id,
                'child_id': self.child_id,
                'date': self.date,
                'name': self.name}


class InventoryDiapers(db.Model):
    __tablename__ = 'inventory_diapers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey("users.id"))
    size = db.Column('size', db.Integer)
    amount = db.Column('amount', db.Float)

    def __init__(self, user_id, size, amount):
        self.user_id = user_id
        self.size = size
        self.amount = amount


class InventoryFormula(db.Model):
    __tablename__ = 'inventory_formula'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.Integer, db.ForeignKey("users.id"))
    amount = db.Column('amount', db.Integer)

    def __init__(self, user_id, amount):
        self.user_id = user_id
        self.amount = amount


class Setting(db.Model):
    __tablename__ = 'settings'
    id = db.Column(db.Integer, primary_key=True)


class Stats(db.Model):
    __tablename__ = 'stats'
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column('child_id', db.Integer, db.ForeignKey("children.child_id"))
    stat_id = db.Column('stat_id', db.Integer)
    value = db.Column('value', db.String(4000))

    def __init__(self, child_id, stat_id, value):
        self.child_id = child_id
        self.stat_id = stat_id
        self.value = value
