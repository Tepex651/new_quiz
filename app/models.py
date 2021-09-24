from flask import flash
from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relation, relationship
from wtforms import StringField, PasswordField
from datetime import datetime
from wtforms.validators import InputRequired
from app import db


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

# def get_ldap_connection():
#     conn = ldap.initialize(app.config['LDAP_PROVIDER_URL'])
#     bind_dn = "cn=admin,ou=ASZI,dc=ast,dc=local"
#     bind_pwd = "admin"
#     conn.simple_bind(bind_dn, bind_pwd)
#     conn.result()
#     return conn


# class User(db.Model):
#     __bind_key__ = 'user_'
#     id = db.Column(db.Integer, primary_key=True)
#     cn = db.Column(db.String(100))
#     username = db.Column(db.String(6))
#     result = db.Column(db.Float)
#     date_testing = db.Column(db.DateTime)
#     admin = db.Column(db.Boolean)

#     def __init__(self, username, password):
#         self.username = username

#     def is_admin(self):
#         return self.admin

#     @staticmethod
#     def try_login(username, password):
#         conn = get_ldap_connection()
#         user_dn = ''
#         user_search = conn.search('ou=ASZI,dc=ast,dc=local', ldap.SCOPE_SUBTREE,
#                                   '(&(objectClass=user)(sAMAccountName=%s))' % (username), ["dn"])
#         actual_user_tuple = conn.result(user_search)
#         user_dn = actual_user_tuple[1][0][0]
#         user_cn = user_dn.split(',')[0].split('=')[1]
#         if user_dn != "":
#             conn.simple_bind_s(user_dn, password)
#         return user_cn

#     def is_authenticated(self):
#         return True

#     def is_active(self):
#         return True

#     def is_anonymous(self):
#         return True

#     def get_id(self):
#         return (self.id)


# class List(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     question = db.Column(db.Text)
#     options = db.relationship('Option', backref='list', lazy='select')

#     def __repr__(self):
#         return f'{self.question}'


# class Option(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     opt = db.Column(db.Text)
#     result = db.Column(db.Boolean, default=False)
#     list_id = db.Column(db.Integer, db.ForeignKey('list.id'))


# class LoginForm(FlaskForm):
#     email = StringField('Почта', [InputRequired()], render_kw={"placeholder": "Логин"})
#     password = PasswordField('Пароль', [InputRequired()], render_kw={"placeholder": "Пароль"})


