# -*- encoding:utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from flask.ext.login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
loginmanager = LoginManager()
loginmanager.init_app(app)

from qual.views.frontend import frontend

app.register_blueprint(frontend, url_prefix='')
