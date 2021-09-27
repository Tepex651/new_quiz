import random

from flask import Blueprint, render_template, request, session
from flask_login import current_user, login_required
from datetime import datetime
from app import db
from .models import Event, Result, Question, Answer

main = Blueprint('main', __name__)



@main.route('/profile')
@login_required
def profile():
    all_events = Event.query.all()
    events_with_user_results = {event: Result.query.filter(Result.user_id == current_user.id, Result.event_id == event.id).all() for event in all_events}
    return render_template('profile.html', all_events=all_events, events_with_user_results=events_with_user_results)


@main.route('/execute_event/<id>')
@login_required
def execute_event(id):
    event = Event.query.filter_by(id=id).first()
    random_questions = random.sample(event.theme.questions, event.number_of_questions)
    session['order_id_questions'] = [question.id for question in random_questions]
    return render_template('execute_event.html', event=event, questions=random_questions)

@main.route('/check_result/<id>', methods=['POST'])
@login_required
def check_result(id):
    event = Event.query.filter_by(id=id).first()
    questions = [Question.query.filter_by(id=id).first() for id in session['order_id_questions']]
    user_answers = {id: list(map(int, request.form.getlist(str(id)))) for id in session['order_id_questions']}
    questions_with_correct_answers = {question.id: Answer.query.filter(Answer.question_id == question.id, Answer.correct == True).all() for question in questions}
    correct_questions = [id for id in questions_with_correct_answers if Answer.query.filter(Answer.id.in_(user_answers[id])).all() == questions_with_correct_answers[id]]
    result = len(correct_questions)
    old_result = Result.query.filter(Result.event_id == event.id, Result.user_id == current_user.id).first()
    if old_result:
        if old_result.result < result:
            old_result.result = result
            old_result.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        new_result = Result(user_id=current_user.id, result=result, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), event_id=event.id)
        db.session.add(new_result)
    db.session.commit()
    return render_template('execute_event.html', event=event, questions=questions, user_answers=user_answers, result=result, correct_questions=correct_questions)