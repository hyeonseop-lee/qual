# -*- encoding:utf-8 -*-

from flask import Flask
from flask.ext.script import Manager, Server
from flask.ext.migrate import MigrateCommand
import settings
from qual import app

app.config.from_object(settings)
manager = Manager(app)

manager.add_command("runserver", Server(host="0.0.0.0", port=8888, use_debugger=True))
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
