from flask import Blueprint, render_template, g, url_for, request, redirect
from flask.helpers import flash
from flask_login import current_user, login_required
from flask_login.utils import login_user, logout_user
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager, mail, app
from .models import User


auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.before_request
def get_current_user():
    g.user = current_user


def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    mail.send(msg)


@auth.route('/')
@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password, password):
            login_user(user, remember=remember)
            return redirect(url_for('main.profile'))
    flash('Неправильный логин или пароль')
    return render_template('login.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        flash('Пользователь уже зарегистрован')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, password=generate_password_hash(password, method='sha256'), first_name=first_name)
    if last_name:
        new_user.last_name = last_name
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    email = request.form.get('email')
    if request.method == 'POST':
        user = User.query.filter_by(email=email).first()
        if user:
            send_password_reset_email(user)
        flash('Проверьте почту')
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html')


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('Сброс пароля',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))


@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.profile'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 == password2:
            user.password = generate_password_hash(password1, method='sha256')
            db.session.commit()
            flash('Новый пароль установлен')
            return redirect(url_for('auth.login'))
        else:
            flash('Пароли должны совпадать')
    return render_template('reset_password.html', token=token)