import os

from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_openid import OpenID
from flask_sqlalchemy import SQLAlchemy
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME,\
        MAIL_PASSWORD


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
mail = Mail(app)

# enable logging
if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler(filename='tmp/microblog.log', mode='a',
                                       maxBytes=1 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s:'
                                                '%(message)s [in'
                                                '%(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')


from app import views, models
