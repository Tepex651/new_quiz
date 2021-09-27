from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail


app = Flask(__name__)

app.config.from_object('config')


db = SQLAlchemy(app)
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# ADMIN
from app.models import Theme, Question, Answer, User, Result, Event

admin_flask = Admin(app, name='Panel')
admin_flask.add_view(ModelView(User, db.session))
admin_flask.add_view(ModelView(Result, db.session))
admin_flask.add_view(ModelView(Event, db.session))
admin_flask.add_view(ModelView(Theme, db.session))
admin_flask.add_view(ModelView(Question, db.session))
admin_flask.add_view(ModelView(Answer, db.session))

from app.main import main
from app.auth import auth
from app.admin import admin_panel

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(admin_panel)