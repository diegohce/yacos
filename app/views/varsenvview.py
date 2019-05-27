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

	decorators = [login_required]

	def get(self, eid, tid):
		
		environment = Environment.get(Environment.id == eid)
		template    = Template.get(Template.id == tid)
		gglobals    = Global.select().order_by(Global.name)

		templatebody = template.body
		vars_from_template = self.__parse_template(templatebody)
		vars_defaults = self.__parse_defaults(templatebody)

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


		VariablesForm = forms.make_dyna_form(variables_d, submit_text=_('Save'))
		form = VariablesForm(**variables_d)


		return flask.render_template('variables.html',
					form=form,
					variables_d=variables_d,
					vars_from_template=vars_from_template,
					vars_defaults=vars_defaults,
					variables=variables,
					gglobals=gglobals,
					environment=environment)
	##
	#


	def post(self, eid, tid):

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


		VariablesForm = forms.make_dyna_form(variables_d, submit_text=_('Save'))

		form = VariablesForm()

		with flask_db.database.transaction():
			for f in form:
				if f.name == 'submit' or f.name == 'csrf_token' or f.name.startswith('global.'):
					continue
#				try:
				affected_rows = Variable.update(value = f.data).where( Variable.name == f.name, Variable.env == environment, Variable.template == template).execute()
				app.logger.debug('Variables update')
				if affected_rows == 0:
					Variable.insert(value = f.data, name = f.name, env = environment, template = template).execute()
					app.logger.debug('Variables insert')
#				except Variable.DoesNotexist:
#					Variable.insert(value = f.data, name = f.name, env = environment, template = template).execute()
#					app.logger.debug('Variables insert')
				
		flask.flash(_('Variables saved'), 'info')
	
		return flask.redirect( flask.request.referrer or flask.url_for('index') )


	def __parse_template(self, body):
#		m = re.findall('\{\{([a-z,A-Z,_,.,0-9, ]*)\}\}', body)
		m = re.findall('\{\{(.*)\}\}', body)
		
		ret = []
		for v in m:
			v_name , sep, dummy = v.partition('|')
			ret.append(v_name)
#		print ret

		return ret


	def __parse_defaults(self, body):
		m = re.findall('\{\{(.*)\}\}', body)
		
		ret = {}
		for v in m:
			v_name , sep, defa = v.partition('|')
			ret[v_name.strip()] = defa.strip()

		return ret


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


class ConfigDownloadView(MethodView):

	#decorators = [login_required]

	def get(self, ename, tname):

		auth = flask.request.authorization

		if auth is None:
			response = flask.make_response('Login required', 401)
			response.headers['WWW-Authenticate'] = 'Basic realm="Login Required"'

		elif not self.__validate_user(auth):
			response = flask.make_response('Login failed', 401)

		else:
			
			try:
				template = Template.get(Template.name == tname)
			except Template.DoesNotExist:
				return 'Template Not found', 404
			
			try:
				environment = Environment.get(Environment.name == ename)
			except Template.DoesNotExist:
				return 'Environment Not found', 404

			config = self.__render_config(template, environment)

			response = flask.make_response(config)
			response.headers['Content-Type'] = 'text/plain'
			
		return response


	def __render_config(self, template, environment):
	
		gglobals  = Global.select().where(Global.env == environment)
		variables = (Variable.select()
                     .where(Variable.template == template,
                            Variable.env == environment) )

		gglobals_d = {}
		for g in gglobals:
			gglobals_d[ g.name ] = g.value

		variables_d = {}
		variables_d['global'] = gglobals_d
		for v in variables:
			variables_d[ v.name ] = v.value

		render = flask.render_template_string( template.body, **variables_d )
		return render
	##									
	#

	def __validate_user(self, auth):
		try:
			User.get(User.username == auth.username, 
					User.password == auth.password)
		except User.DoesNotExist:
			return False
		return True
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

