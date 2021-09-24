from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)

app.config.from_object('config')
# app.config['LDAP_PROVIDER_URL'] = 'ldap://192.168.0.190:389/'
# app.config['LDAP_PROTOCOL_VERSION'] = 3
app.config['LOG_FILE'] = 'application.log'

db = SQLAlchemy(app)

app.secret_key = 'some_random_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


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