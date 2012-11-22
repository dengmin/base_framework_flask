#! /usr/bin/env python
#coding=utf-8

from flask.ext.script import Manager,Server,Shell

from src import create_app
from src.database import db

manager = Manager(create_app('settings.py'))

@manager.shell
def make_shell_context():
	return dict()

manager.add_command('runserver',Server(host="0.0.0.0", port=9000))

@manager.command
def syncdb():
	db.create_all()
	
@manager.command
def dropall():
    """drop all tables"""
    db.drop_all()


if __name__ == "__main__":
	manager.run()
