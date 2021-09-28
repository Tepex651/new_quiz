from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import jwt
from time import time

from app import db, app


class User(db.Model):
    __tablename__ = 'user_profile'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    admin = db.Column(db.Boolean, default=False)
    results = relationship('Result', back_populates='user', cascade='all, delete', passive_deletes=True)

    def __repr__(self) -> str:
        return self.email

    def __init__(self, first_name, email, password):
        self.first_name = first_name
        self.email = email
        self.password = password
        
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return (self.id)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 
            'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user_profile.id', ondelete="CASCADE"))
    result = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    event_id = db.Column(db.Integer, ForeignKey('event.id', ondelete="CASCADE"))
    event = relationship('Event', back_populates='results')
    user = relationship('User', back_populates='results')

class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    theme_id = db.Column(db.Integer, ForeignKey('theme.id', ondelete='CASCADE'))
    theme = relationship('Theme', back_populates='events')
    start_date = db.Column(db.Date, default=datetime.now().date())
    end_date = db.Column(db.Date)
    number_of_questions = db.Column(db.SmallInteger, default='10')
    number_of_correct = db.Column(db.SmallInteger, default='8')
    results = relationship('Result', back_populates='event', cascade='all, delete', passive_deletes=True)


class Theme(db.Model):
    __tablename__ = 'theme'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    events = relationship('Event', back_populates='theme', cascade='all, delete', passive_deletes=True)
    questions = relationship('Question', back_populates='theme', cascade='all, delete', passive_deletes=True)
     
    def __repr__(self) -> str:
        return self.name

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True)
    theme_id = db.Column(db.Integer, ForeignKey('theme.id', ondelete="CASCADE"))
    name = db.Column(db.String(255))
    answers = relationship('Answer', back_populates='question', cascade='all, delete', passive_deletes=True)
    theme = relationship('Theme', back_populates='questions')

    def __repr__(self) -> str:
        return self.name

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, ForeignKey('question.id', ondelete="CASCADE"))
    name = db.Column(db.Text)
    correct = db.Column(db.Boolean)
    question = relationship('Question', back_populates='answers')

    def __repr__(self) -> str:
        return self.name