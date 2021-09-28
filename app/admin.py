from datetime import datetime
from flask import Blueprint, url_for, redirect, flash, request, render_template
from flask_login import current_user, login_required
from functools import wraps

from app import db
from .models import Event, Result, User, Theme, Question, Answer



admin_panel = Blueprint('admin_panel', __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.admin is False:
            return redirect(url_for('main.profile'))
        return f(*args, **kwargs)
    return decorated_function


@admin_panel.route('/users')
@login_required
@admin_required
def users():
    all_users = User.query.all()
    columns = User.__table__.columns.keys()
    return render_template('users.html', all_users=all_users, columns=columns)


@admin_panel.route('/themes')
@login_required
@admin_required
def themes():
    all_themes = Theme.query.all()
    return render_template('themes.html', all_themes=all_themes)


@admin_panel.route('/create_theme', methods=['POST'])
@login_required
@admin_required
def create_theme():
    name_theme = request.form.get('theme')
    if name_theme == '':
        flash('Нельзя создать тему без названия')
        return redirect(url_for('admin_panel.themes'))
    theme = Theme.query.filter_by(name=name_theme).first()
    if theme:
        flash(f'Тема {name_theme} уже существует. Нельзя создать две одинаковых темы')
        return redirect(url_for('admin_panel.themes'))
    new_theme = Theme(name = name_theme)
    db.session.add(new_theme)
    db.session.commit()
    return redirect(url_for('admin_panel.themes'))


@admin_panel.route('/delete_theme/<id>')
@login_required
@admin_required
def delete_theme(id):
    delete_theme = Theme.query.filter_by(id=id).first()
    db.session.delete(delete_theme)
    db.session.commit()
    return redirect(url_for('admin_panel.themes'))


@admin_panel.route('/theme/<id>')
@login_required
@admin_required
def show_theme(id):
    theme = Theme.query.filter_by(id=id).first()
    return render_template('show_theme.html', theme=theme)


@admin_panel.route('/delete_question/<id>')
@login_required
@admin_required
def delete_question(id):
    delete_question = Question.query.filter_by(id=id).first()
    db.session.delete(delete_question)
    db.session.commit()
    return redirect(url_for('admin_panel.show_theme', id=delete_question.theme_id))


@admin_panel.route('/edit_question/<id>',  methods=['POST'])
@login_required
@admin_required
def edit_question(id):
    input_question = request.form.get('question')
    question = Question.query.filter_by(id=id).first()
    if question:
        question.name = input_question
    else:
        redirect(url_for('main.questions'))
    old_answer_id = request.form.getlist('answer_id')
    old_answer_name = request.form.getlist('answer_name')
    old_answer_correct = request.form.getlist('answer_correct')
    for list_id in range(len(old_answer_id)):
        db.session.query(Answer).filter_by(id=old_answer_id[list_id]).update(dict(name=old_answer_name[list_id],correct=True if old_answer_correct[list_id] == 'True' else False))
        
    new_answer_name = request.form.getlist('new_answer_name')
    new_answer_correct = request.form.getlist('new_answer_correct')
    if new_answer_name:
        for new_list_id in range(len(new_answer_name)):
            new_answer = Answer(question_id=id, name=new_answer_name[new_list_id], correct=True if new_answer_correct[new_list_id] == 'True' else False)
            db.session.add(new_answer)
    db.session.commit()
    return redirect(url_for('admin_panel.show_question', id=question.id))


@admin_panel.route('/create_question/<theme_id>', methods=['POST', 'GET'])
@login_required
@admin_required
def create_question(theme_id):
    if request.method == 'POST':
        new_question = Question(theme_id=theme_id, name=request.form.get('question'))
        db.session.add(new_question)
        db.session.commit()
        new_answer_name = request.form.getlist('new_answer_name')
        new_answer_correct = request.form.getlist('new_answer_correct')
        for list_id in range(len(new_answer_name)):
            new_answer = Answer(question_id=new_question.id, name=new_answer_name[list_id], correct=True if new_answer_correct[list_id] == 'True' else False)
            db.session.add(new_answer)
        db.session.commit()
        return redirect(url_for('admin_panel.show_theme', id=theme_id))
    return render_template('create_question.html', theme_id=theme_id)


@admin_panel.route('/question/<id>')
@login_required
@admin_required
def show_question(id):
    question = Question.query.filter_by(id=id).first()
    if question:
        return render_template('show_question.html', question=question)
    else:
        return redirect(url_for('admin_panel.questions'))
    

@admin_panel.route('/delete_answer/<id>')
@login_required
@admin_required
def delete_answer(id):
    delete_answer = Answer.query.filter_by(id=id).first()
    db.session.delete(delete_answer)
    db.session.commit()
    return redirect(url_for('admin_panel.show_question', id=delete_answer.question_id))


@admin_panel.route('/events')
@login_required
@admin_required
def events():
    all_events = Event.query.all()
    return render_template('events.html', all_events=all_events)


@admin_panel.route('/show_event/<id>')
@login_required
@admin_required
def show_event(id):
    event = Event.query.filter_by(id=id).first()
    all_themes = Theme.query.all()
    return render_template('show_event.html', event=event, all_themes=all_themes)

@admin_panel.route('/edit_event/<id>', methods=['POST'])
@login_required
@admin_required
def edit_event(id):
    theme_id = request.form.get('theme_id')
    theme = Theme.query.filter_by(id=theme_id).first()
    start_date = request.form.get('start_date') or None
    end_date = request.form.get('end_date') or None
    number_of_questions = request.form.get('number_of_questions')
    number_of_correct = request.form.get('number_of_correct')
    if start_date is None:
        start_date = datetime.now().date()
    if int(number_of_questions) < int(number_of_correct):
        flash('Количество вопросов должно быть больше, чем необходимое количество баллов')
    elif len(theme.questions) < int(number_of_questions):
        flash(f'В теме {theme} слишком мало вопросов. Добавьте в тему еще вопросов')
    else:
        Event.query.filter_by(id=id).update(dict(theme_id=theme_id, start_date=start_date, end_date=end_date, number_of_questions=number_of_questions, number_of_correct=number_of_correct))
        db.session.commit()
    return redirect(url_for('admin_panel.show_event', id=id))


@admin_panel.route('/create_event', methods=['POST', 'GET'])
@login_required
@admin_required
def create_event():
    if request.method == "POST":
        theme_id = request.form.get('theme_id')
        theme = Theme.query.filter_by(id=theme_id).first()
        start_date = request.form.get('start_date') or None
        end_date = request.form.get('end_date') or None
        number_of_questions = request.form.get('number_of_questions')
        number_of_correct = request.form.get('number_of_correct')
        if int(number_of_questions) < int(number_of_correct):
            flash('Количество вопросов должно быть больше, чем необходимое количество баллов')
        elif len(theme.questions) < int(number_of_questions):
            flash(f'В теме {theme} слишком мало вопросов. Добавьте в тему еще вопросов')
        else:
            new_event = Event(theme_id=theme_id, start_date=start_date, end_date=end_date, number_of_questions=number_of_questions, number_of_correct=number_of_correct)
            db.session.add(new_event)
            db.session.commit()
            return redirect(url_for('admin_panel.show_event', id=new_event.id))
    all_themes = Theme.query.all()
    return render_template('create_event.html', all_themes=all_themes)

@admin_panel.route('/results')
@login_required
@admin_required
def results():
    all_events = Event.query.all()
    return render_template('results.html', all_events=all_events)

@admin_panel.route('/result/<id>')
@login_required
@admin_required
def show_results(id):
    event = Event.query.filter_by(id=id).first()
    
    all_results = event.results
    count_users = User.query.count()
    return render_template('show_results.html', event=event, all_results=all_results, count_users=count_users, count_results=len(all_results))