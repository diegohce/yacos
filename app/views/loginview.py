#encoding: utf-8

import flask
from flask.views import MethodView

from flask_login import (
    login_required,
    current_user,
    login_user,
	logout_user,
)
from app import (
    app,
#    models,
    forms,
)

from peewee import fn
from flask_babel import lazy_gettext as _
from app.models import *

class LoginView(MethodView):

	#decorators = [login_required]

	def get(self):

		form = forms.LoginForm()
		
		return flask.render_template('login.html',
					form=form)


	def post(self):

		form = forms.LoginForm()

		try:
			user = User.get(User.username == form.username.data,
							User.password == form.password.data)
		except User.DoesNotExist:
			flask.flash(_('Bad username/password'), 'error')
			return flask.redirect( flask.url_for('login') )

		login_user(user)

		return flask.redirect( flask.url_for('index') )
##
#

class LogoutView(MethodView):

	decorators = [login_required]

	def get(self):

		logout_user()
		return flask.redirect( flask.url_for('login') )
##
#


