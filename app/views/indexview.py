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
#m = re.findall('(\{\{[a-z,A-Z,_,.,0-9]*\}\})', c)
#print m
#
#



