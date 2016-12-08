#encoding: utf-8

import flask
from flask.views import MethodView

from flask_login import (
    login_required,
    current_user,
    login_user,
)
from app import (
    app,
    models,
    forms,
)

from peewee import fn
from flask_babel import lazy_gettext as _


class IndexView(MethodView):

	#decorators = [login_required]

	def get(self):

		return flask.render_template('index.html')
#






