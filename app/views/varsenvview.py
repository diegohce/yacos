#encoding: utf-8

import flask
from flask.views import MethodView

from flask_login import (
    login_required,
#    current_user,
#    login_user,
)
from app import (
    app,
#    models,
    forms,
)

from peewee import fn
from flask_babel import lazy_gettext as _
from app.models import *

import re



class VarsEnvView(MethodView):

	#decorators = [login_required]

	def get(self, eid, tid):
		
		envs = Environment.select().order_by(Environment.name)

		environment = Environment.get(Environment.id == eid)
		template    = Template.get(Template.id == tid)
		gglobals    = Global.select().order_by(Global.name)

		templatebody = template.body
		vars_from_template = self.__parse_template(templatebody)


		try:
			variables = (Variable.select()
                         .where(Variable.template == template, 
                                Variable.env == environment) )
		except Variable.DoesNotExist:
			variables = []

		variables_d = dict.fromkeys([ v.strip() for v in vars_from_template ], '')

		for v in variables:
			variables_d[ v.name ] = v.value

		resolved_globals = self.__resolve_globals(environment, variables_d)
		variables_d.update( resolved_globals )

		return flask.render_template('variables.html',
					variables_d=variables_d,
					vars_from_template=vars_from_template,
					variables=variables,
					gglobals=gglobals,
					envs=envs)
	##
	#

	def post(self):
		return flask.redirect( flask.request.referrer or flask.url_for('index') )


	def __parse_template(self, body):
		m = re.findall('\{\{([a-z,A-Z,_,.,0-9, ]*)\}\}', body)
#		print m
		return m

	def __resolve_globals(self, environment, variables_d):
	
		gg_d = {}
		for var_name in filter(lambda v: v.startswith('global.'), variables_d):
			try:
				gg = Global.get(Global.name == var_name[len('global.'):], Global.env == environment)
				gg_d[ var_name ] = gg.value
			except Global.DoesNotExist, e:
				app.logger.debug( repr(e) )
		return gg_d			

##
#




##encoding: utf-8
#
#
#import re
#
#with open('checkout_message_client.txt') as f:
#	c = unicode(f.read().decode('utf-8'))
#
#with open('template1.conf') as f:
#	c = unicode(f.read().decode('utf-8'))
#
#
#m = re.findall('(\{\{[a-z,A-Z,_,.,0-9,]*\}\})', c)
#print m
#
#

