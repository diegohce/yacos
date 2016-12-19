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
#    models,
    forms,
)

from peewee import fn
from flask_babel import lazy_gettext as _
from app.models import *

class IndexView(MethodView):

	decorators = [login_required]

	def get(self):

		form = forms.TemplateUploadForm()
		
		envs = Environment.select().order_by(Environment.name)

		templates = (Template.select(Template, Variable).where(Template.enabled == True)
					.join(Variable, JOIN.LEFT_OUTER)
					.order_by(Template.name, Variable.env).aggregate_rows() )

		gglobals = Global.select().order_by(Global.name)

		return flask.render_template('index.html',
					form=form,
					gglobals=gglobals,
					templates=templates,
					envs=envs)
##
#

