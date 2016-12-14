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

class TemplateUploadView(MethodView):

	#decorators = [login_required]

	def post(self):

		form = forms.TemplateUploadForm()

		name = form.name.data
		content = form.template.data.stream.read()

		Template.insert( name = name, body = content).execute()	
		flask.flash(_('Template %(name)s uploaded successfully', name=name) , 'success')

		return flask.redirect(flask.request.referrer or flask.url_for('index') )
##
#


class TemplateDeleteView(MethodView):

	#decorators = [login_required]

	def get(self, tid):

		try:
			template = Template.get(Template.id == tid)
			name = template.name

			Variable.delete().where(Variable.template == template).execute()
			template.delete_instance()

			flask.flash(_('Template %(name)s deleted successfully', name=name) , 'success')

		except Template.DoesNotExist, e:
#			flask.flash( repr(e), 'error' )
			app.logger.error( repr(e) )

		return flask.redirect(flask.request.referrer or flask.url_for('index') )
##
#


class TemplateDownloadView(MethodView):

	#decorators = [login_required]

	def get(self, tid):

		try:
			template = Template.get(Template.id == tid)
			name = template.name
			content = template.body

			response = flask.make_response(content)
			response.headers['Content-Disposition'] = 'attachment; filename=%s' % name

			return response

		except Template.DoesNotExist, e:
#			flask.flash( repr(e), 'error' )
			app.logger.error( repr(e) )

		return flask.redirect( flask.request.referrer or flask.url_for('index') )
##
#



