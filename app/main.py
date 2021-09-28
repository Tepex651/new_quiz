import random

from datetime import datetime
from flask import Blueprint, render_template, request, session
from flask_login import current_user, login_required

from app import db
from .models import Event, Result, Question, Answer


main = Blueprint('main', __name__)


@main.route('/profile')
@login_required
def profile():
    all_events = Event.query.all()
    all_user_results = {event: Result.query.filter_by(user_id=current_user.id, event_id=event.id).first() for event in all_events}
    return render_template('profile.html', all_events=all_events, all_user_results=all_user_results)


@main.route('/execute_event/<id>')
@login_required
def execute_event(id):
    event = Event.query.filter_by(id=id).first()
    random_questions = random.sample(event.theme.questions, event.number_of_questions)
    session['order_questions'] = [question.id for question in random_questions]
    return render_template('execute_event.html', event=event, questions=random_questions)

@main.route('/execute_event/<id>', methods=['POST'])
@login_required
def check_result(id):
    event = Event.query.filter_by(id=id).first()
    questions = [Question.query.filter_by(id=id).first() for id in session['order_questions']]
    # from form
    user_answers = {question.id: request.form.getlist(str(question.id)) for question in questions}
    # from db
    questions_with_correct = {question.id: list(map(str, Answer.query.filter(Answer.question_id == question.id, Answer.correct == True).all())) for question in questions}

    right_questions = [id for id in questions_with_correct if user_answers[id] == questions_with_correct[id]]
    result = len(right_questions)
    old_result = Result.query.filter_by(user_id=current_user.id, event_id=event.id).first()
    if old_result:
        if old_result.result < event.number_of_correct:
            old_result.result = result
            old_result.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        new_result = Result(user_id=current_user.id, result=result, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), event_id=id)
        db.session.add(new_result)
    db.session.commit()
    return render_template('execute_event.html', event=event, questions=questions, result=result, user_answers=user_answers, right_questions=right_questions)