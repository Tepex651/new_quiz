import random

from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from flask_login import current_user, login_required
from datetime import date, datetime
from app import db
from .models import Event, Result, User, Theme, Question, Answer

main = Blueprint('main', __name__)



@main.route('/profile')
@login_required
def profile():
    all_events = Event.query.all()
    all_results = current_user.results
    return render_template('profile.html', all_events=all_events)


@main.route('/execute_event/<id>')
@login_required
def execute_event(id):
    event = Event.query.filter_by(id=id).first()
    random_questions = random.sample(event.theme.questions, event.number_of_questions)
    order_questions = [question.id for question in random_questions]
    # session['questions'] = random_questions
    return render_template('execute_event.html', theme=event.theme, questions=random_questions, order_questions=order_questions)

@main.route('/execute_event', methods=['POST'])
@login_required
def check_result():
    theme = request.form.get('theme')

    questions_id = request.form.getlist('question')
    questions = Question.query.filter(Question.id.in_(questions_id)).all()
    right_answers = Answer.query.filter(Answer.question_id.in_(questions_id), Answer.correct == True).all()

    user_answers = {id: request.form.getlist(id) for id in questions_id}
    questions_with_correct = {question.id: db.session.query(Answer.id).filter(Answer.question_id == question.id, Answer.correct == True).all() for question in questions}

    flash(questions_with_correct)
    # session['questions'] = random_questions
    return render_template('execute_event.html', theme=theme, questions=questions)