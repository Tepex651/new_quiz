from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_admin.helpers import flash_errors
from flask_login import current_user, login_required
from datetime import date, datetime
from app import db
from .models import Event, User, Theme, Question, Answer

main = Blueprint('main', __name__)



@main.route('/profile')
@login_required
def profile(): 
    all_questions = Question.query.all()
    all_answers = Answer.query.all()
    return render_template('profile.html', all_questions=all_questions, all_answers=all_answers, first_name=current_user.first_name)



    