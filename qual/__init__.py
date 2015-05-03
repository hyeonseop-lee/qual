# -*- encoding:utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.login import LoginManager
from flask.ext.admin import Admin

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
admin = Admin(app)
loginmanager = LoginManager(app)

from qual.views.frontend import frontend
import qual.admin

app.register_blueprint(frontend, url_prefix='')
