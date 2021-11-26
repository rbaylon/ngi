import uuid
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from Utils.errorhandler import page_not_found, unauthorized
from flask_sessionstore import Session
from flask_session_captcha import FlaskSessionCaptcha

dir_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.dirname(dir_path)
app = Flask(__name__)
app.config.from_pyfile('{}/config/config.cfg'.format(project_path))
db = SQLAlchemy(app)
Bootstrap(app)
migrate = Migrate(app, db, compare_type=True)
app.register_error_handler(404, page_not_found)
app.register_error_handler(401, unauthorized)
app.config['CAPTCHA_ENABLE'] = True
app.config['CAPTCHA_LENGTH'] = 5
app.config['CAPTCHA_WIDTH'] = 160
app.config['CAPTCHA_HEIGHT'] = 60
app.config['SESSION_TYPE'] = 'sqlalchemy'
Session(app)
captcha = FlaskSessionCaptcha(app)

from views import default_views, ngi_views


