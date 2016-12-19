#encoding: utf-8

from modules import common

import flask
from flask_login import (
	UserMixin,
	AnonymousUserMixin,
#	current_user,
)

from peewee import *
from app import flask_db

#http://www.databaseanswers.org/data_models/amazon_and_starbucks/index.htm
#http://www.databaseanswers.org/data_models/amazon_and_starbucks/amazon_and_starbucks_with_ref_data.htm


#https://peewee.readthedocs.org/en/latest/peewee/models.html#field-types-table

#https://code.google.com/p/worlddb/downloads/list


class AnonUser(AnonymousUserMixin):
	pass
##
#


class User(flask_db.Model, UserMixin):
	username = CharField(unique=True)
	password = CharField()
	fullname = CharField(default='')

	class Meta:
		indexes = (
            (('username', 'password'), True),
        )

	def __unicode__(self):
		return self.username
##
#


class Environment(flask_db.Model):
	name = CharField()

	def __unicode__(self):
		return self.name
##
#


class Global(flask_db.Model):
	name  = CharField()
	value = CharField(default='')
	env   = ForeignKeyField(Environment, related_name='environments')

	class Meta:
		indexes = (
            (('name', 'env'), True),
        )

	def __unicode__(self):
		return self.name
##
#
	

class Template(flask_db.Model):
	name    = CharField(unique=True)
	body    = TextField()
	enabled = BooleanField(default=True)

	def __unicode__(self):
		return self.name
##
#


class Variable(flask_db.Model):
	name     = CharField()
	value    = TextField(null=False, default='')
	template = ForeignKeyField(Template)	
	env      = ForeignKeyField(Environment)

	def __unicode__(self):
		return self.name
##
#



def create_tables():
	flask_db.database.create_tables([
		User,
		Environment,
		Global,
		Template,
		Variable,
		], safe=True)
##
#


