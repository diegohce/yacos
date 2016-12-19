#encoding: utf-8

import os

import models
from app import app

import flask
#from jinja2 import Markup
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.peewee import ModelView

from flask_login import (
    current_user,
)


class SecureModelView(ModelView):

	def is_accessible(self):
		if current_user.is_authenticated and current_user.username == 'admin':
			return True
		return flask.abort(404)


class SecureAdminIndexView(AdminIndexView):

	def is_accessible(self):
		if current_user.is_authenticated and current_user.username == 'admin':
			return True
		return flask.abort(404)



admin = Admin(app, 'Config Server admin area', template_mode='bootstrap3', index_view=SecureAdminIndexView()) 
admin.add_view(SecureModelView(models.User))
admin.add_view(SecureModelView(models.Environment))
admin.add_view(SecureModelView(models.Global))
admin.add_view(SecureModelView(models.Template))
admin.add_view(SecureModelView(models.Variable))

