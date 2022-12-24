# from exts import db
# from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # username
    password_hash = db.Column(db.String(128))  # hashed password
    activities = db.relationship('Activity', secondary='activity_user', backref='users', lazy='dynamic')

    def set_password(self, password):  # set password，taking password as parameter
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):  # validate password，taking password as parameter
        return check_password_hash(self.password_hash, password)  # return a bool value


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity_name = db.Column(db.String(64))
    activity_info = db.Column(db.String(512))
    price = db.Column(db.Integer)  # price
    limit = db.Column(db.Integer)  # limit
    applied = db.Column(db.Integer, default=0)  # applied number
    time = db.Column(db.DateTime)  # time of game
    deadline = db.Column(db.Date)  # time to buy tickets
    location = db.Column(db.String(64))  # location
    lon = db.Column(db.Float)  # longitude
    lat = db.Column(db.Float)  # latitude


activity_user = db.Table('activity_user',
                         db.Column('activity_id', db.Integer, db.ForeignKey('activity.id'),primary_key=True),
                         db.Column('user_id', db.Integer, db.ForeignKey('user.id'),primary_key=True),
                         )
