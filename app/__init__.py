#encoding: utf-8

import os
import sys
import json
import logging

import flask
from flask_bootstrap import Bootstrap
from flask_login import (
							 LoginManager, 
							 login_required,
							 login_url, 
							 current_user,
							)

from flask_babel import Babel
from flask_babel import lazy_gettext as _
from playhouse.flask_utils import FlaskDB

import forms


app = flask.Flask(__name__)

app.config.update( dict(
	DATABASE             = 'sqliteext:///%s' % os.path.join(app.root_path, 'configserver.db'),
	CSRF_ENABLED         = True,
	BABEL_DEFAULT_LOCALE = 'en',
	SECRET_KEY           = 'f655c5171113e77077ccd37538473044', #python -c "import os;print os.urandom(16).encode('hex')"
))
app.config.from_pyfile(os.path.join(app.root_path, 'configserver.cfg'))
#app.config['FILES_PATH'] = os.path.join(app.root_path, 'static') #, app.config['FILES_PATH'])
#app.config['FILES_RELATIVE_PATH'] = 'files/'

flask_db = FlaskDB(app)

import models

login_manager = LoginManager()
login_manager.init_app(app)

Bootstrap(app)
babel = Babel(app)


@babel.localeselector
def get_locale():
	user = current_user 
	if user.is_authenticated:
		return user.lang
	return flask.request.accept_languages.best_match(['es', 'en'])


login_manager.anonymous_user = models.AnonUser

@login_manager.user_loader
def load_user(userid):
	try:
		u = models.User.get(models.User.id == userid)
	except models.User.DoesNotExist:
		u = None
	except Exception, e:
		app.logger.error(repr(e))
		u = None
	return u



@login_manager.unauthorized_handler
def must_login():
	return flask.redirect(login_url('login', next_url=flask.request.url))
	


#@app.errorhandler(404)
#def page_not_found(e):
#	form = forms.ContactForm()
#	return flask.render_template('404.html', contactform=form), 404


@app.route('/favicon.ico', methods=['GET'])
@app.route('/robots.txt', methods=['GET'])
def serve_robots():
	 return flask.send_from_directory(app.static_folder, flask.request.path[1:])

#Application views
from views import *

#Admin views
import admin


if __name__ == '__main__':
	pass


