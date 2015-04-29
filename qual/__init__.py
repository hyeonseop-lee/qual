# -*- encoding:utf-8 -*-
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.migrate import Migrate
from qual.views.frontend import frontend

app = Flask(__name__)
app.register_blueprint(frontend, url_prefix='')

db = SQLAlchemy(app)

migrate = Migrate(app, db)

from qual import models
