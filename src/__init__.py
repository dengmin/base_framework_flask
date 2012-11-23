#! /usr/bin/env python
#coding=utf-8

from flask import Flask,render_template,g,request,jsonify,url_for,Markup,g,_app_ctx_stack
from werkzeug.exceptions import default_exceptions
from flaskext.uploads import configure_uploads,UploadSet, IMAGES,DEFAULTS
from src.apps.front import views as front
from src.apps.account import views as account
from src.apps.dashboard import views as admin
from src.apps.account.models import User
from flask_principal import Principal,identity_loaded,RoleNeed, UserNeed

from . import database
from .utils import import_object
from .filters import register_template_filters,error_handers
import os

def import_models():
	import_object('src.apps.account.models')

blueprints = (
	(front.app,""),
	(account.app,"/account"),
	(admin.app,'/admin'),
)

def register_blueprint(app,blueprints):
	for module,prefix in blueprints:
		app.register_blueprint(module,url_prefix=prefix)


def create_app(config=None):
	
	app = Flask(__name__,static_folder='static',template_folder='templates')

	if config:
		app.config.from_pyfile(config)

	config_identity(app)

	config_before_after_request(app)
	
	#config error handlers
	error_handers(app)

	#register template filters
	register_template_filters(app)
	
	register_context_processor(app)
	#config ext
	config_ext(app)

	database.db.init_app(app)
	database.db.app = app

	config_logging(app)

	#register blueprint
	register_blueprint(app,blueprints)
	import_models()

	return app


def config_identity(app):
	principal = Principal(app)

	@identity_loaded.connect_via(app)
	def _on_identity_loaded(sender,identity):
		g.user = User.query.from_identity(identity)

def config_before_after_request(app):

	@app.before_request
	def authenticate():
		g.user = getattr(g.identity, 'user', None)

	@app.after_request
	def after_request(response):
		for func in getattr(g, 'call_after_request', ()):
			response = func(response)
		return response

def register_context_processor(app):

	def url_for_timestamp(endpoint, **values):
		if endpoint == 'static':
			filename = values.get('filename', None)
			if filename:
				file_path = os.path.join(app.root_path,endpoint, filename)
				values['q'] = int(os.stat(file_path).st_mtime)
		return url_for(endpoint, **values)
	
	@app.context_processor
	def dated_url_for():
		return dict(url_for=url_for_timestamp)

	@app.context_processor
	def config():
		return dict(config=app.config)

def config_ext(app):
	images = UploadSet('images',IMAGES)
	docs = UploadSet('docs',DEFAULTS)
	configure_uploads(app,(images))

def config_logging(app):
	import logging,os
	from logging.handlers import RotatingFileHandler
	logfile = os.path.join(app.root_path,'logs/debug.log')

	formatter = logging.Formatter('''%(asctime)s : %(levelname)s %(pathname)s:%(lineno)d %(funcName)s: %(message)s''')

	log_handler = RotatingFileHandler(logfile,maxBytes=100000,backupCount=10)
	log_handler.setLevel(logging.DEBUG)
	log_handler.setFormatter(formatter)
	app.logger.addHandler(log_handler)
