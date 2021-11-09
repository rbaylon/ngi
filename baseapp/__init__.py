from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from Utils.errorhandler import page_not_found, unauthorized
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
project_path = os.path.dirname(dir_path)
app = Flask(__name__)
app.config.from_pyfile('{}/config/config.cfg'.format(project_path))
db = SQLAlchemy(app)
Bootstrap(app)
migrate = Migrate(app, db, compare_type=True)
app.register_error_handler(404, page_not_found)
app.register_error_handler(401, unauthorized)


from views import default_views, ngi_views


