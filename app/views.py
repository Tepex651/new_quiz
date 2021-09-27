# 2 РАЗНЫХ ФУНКЦИИ

import datetime
import random

from flask import request, render_template, flash, redirect, url_for, Blueprint, g
from flask_login import current_user, login_user, logout_user, login_required

from app import login_manager, db, app
from app.models import User, LoginForm

auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.before_request
def get_current_user():
    g.user = current_user




















# @auth.route('/home')
# def home():
#     lists = List.query.all()
#     random_list = random.sample(lists, 10)
#     global global_list_options
#     global_list_options = {}
#     for x in random_list:
#         option = Option.query.filter(Option.list_id == x.id)
#         a = []
#         for y in option:
#             a.append(y)
#             global_list_options[x] = a
#     return render_template('/home.html', global_list_options=global_list_options)


# @auth.route('/home', methods=['POST'])
# def user_post():
#     try:
#         global_list_options
#     except NameError:
#         return redirect(url_for('auth.home'))
#     date = datetime.date.today()
#     choice = request.form.getlist('choice')

#     # User_answers
#     user_answers = Option.query.filter(Option.id.in_(choice)).all()

#     user_right_answers = []
#     false_answers = []
#     for x in user_answers:
#         if x.result == True:
#             user_right_answers.append(x.id)
#         elif x.result == False:
#             false_answers.append(x.id)

#     result = 0
#     jj = 0
#     for i in global_list_options:
#         jj = 0
#         for j in global_list_options[i]:
#             if j.result == False and j.id in false_answers:
#                 jj = 0
#                 break
#             elif j.result == True and j.id in user_right_answers:
#                 jj = 1
#         result = result + jj

#     user = User.query.filter(User.username == current_user.username).first()
#     user.result = result
#     user.date_testing = date
#     db.session.commit()
#     return render_template('/home.html', result=result, user_right_answers=user_right_answers,
#                            false_answers=false_answers, user_answers=user_answers,
#                            global_list_options=global_list_options)


# @auth.route('/')
# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('auth.home'))

#     form = LoginForm(request.form)

#     if request.method == 'POST' and form.validate():
#         username = request.form.get('username')
#         username = username.lower()
#         password = request.form.get('password')

#         try:
#             User.try_login(username, password)
#             app.logger.info(f'{username} has been connect')
#         except Exception as e:
#             flash(e)
#             flash('Неправильный логин или пароль', 'danger')
#             app.logger.warning(f'Incorrect username or pass from - {username}')
#             return render_template('login.html', form=form)

#         user = User.query.filter_by(username=username).first()

#         if not user:
#             user = User(username, password)
#             if user.username == 'admin':
#                 user.admin = True
#             db.session.add(user)
#             db.session.commit()
#         login_user(user)
#         # flash('Successfully', 'success')
#         return redirect(url_for('auth.home'))

#     if form.errors:
#         flash(form.errors, 'danger')

#     return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
