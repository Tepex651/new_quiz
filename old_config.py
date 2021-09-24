



CSRF_ENABLED = True
SECRET_KEY = 'Xw0G2EqGu3BNhndu0LfiXXXH8grIIAph+YFE7Y9jGqK/6KRAmTcDfDsNf55cDLvZENTLB9RUN9W7/K2/z7ovAg=='

SQLALCHEMY_DATABASE_URI = 'sqlite:////flask_ldap/questions.db'
SQLALCHEMY_BINDS = {'users': 'sqlite:////flask_ldap/users.db'}
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True