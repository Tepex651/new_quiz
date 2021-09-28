import os 


CSRF_ENABLED = True
SECRET_KEY = 'Xw0G2EqGu3BNhndu0LfiXXXH8grIIAph+YFE7Y9jGqK/6KRAmTcDfDsNf55cDLvZENTLB9RUN9W7/K2/z7ovAg=='
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost/quiz'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
ADMINS = ['quiz.adm@gmail.com']
