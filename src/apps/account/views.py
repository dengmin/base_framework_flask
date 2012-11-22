#! /usr/bin/env python
#coding=utf-8

from flask import Blueprint,request

app = Blueprint('account',__name__)


@app.route('/shutdown',methods=['POST'])
def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	return 'sever shutdown..'