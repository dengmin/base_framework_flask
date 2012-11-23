#! /usr/bin/env python
#coding=utf-8

from flask import Blueprint,request,url_for,redirect,render_template, \
	session,current_app
from flask import flash
from datetime import datetime
from flask_principal import identity_changed, Identity, AnonymousIdentity
from .forms import LoginForm
from .models import User
from src.database import db

app = Blueprint('account',__name__,template_folder='templates')

@app.route('/login',methods=['GET','POST'])
def login():
	form = LoginForm(username=request.args.get('username',None),
			next = request.args.get('next',None))
	if request.method == 'GET':
		return render_template('login.html',form=form)
	else:
		if form.validate_on_submit():
			user,authed = User.query.authenticate(form.username.data,form.password.data)
			if user and authed:
				if user.actived:
					session.permanent = form.remember.data
					identity_changed.send(current_app._get_current_object(),identity=Identity(user.id))
					user.last_login = datetime.now()
					db.session.commit()
					next_url = form.next.data
					if not next_url or next_url == request.path:
						next_url = url_for('front.index')
					return redirect(next_url)
				else:
					flash('account not actived!')
			else:
				flash('Sorry,invlid login,username or password error!')
		return render_template('login.html',form=form)

@app.route('/logout')
def logout():
	identity_changed.send(current_app._get_current_object(),
		identity=AnonymousIdentity())
	session.clear()
	return redirect(url_for('account.login'))

@app.route('/shutdown',methods=['POST'])
def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	return 'sever shutdown..'