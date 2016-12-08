#encoding: utf-8

import os

import models
from app import app

import flask
from jinja2 import Markup
from flask_admin import Admin #,form
from flask_admin.contrib.peewee import ModelView
#from peewee import *
#from modules import common


import wtforms as wtf



admin = Admin(app, 'Config Server admin area', template_mode='bootstrap3') 
admin.add_view(ModelView(models.User))
admin.add_view(ModelView(models.Environment))
admin.add_view(ModelView(models.Global))
admin.add_view(ModelView(models.Template))
admin.add_view(ModelView(models.Variable))

