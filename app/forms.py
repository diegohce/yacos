#encoding: utf-8


from flask_wtf import FlaskForm as Form
from wtforms.fields import html5
from wtforms import (
	TextField, TextAreaField, SelectField, 
	SubmitField, HiddenField, validators,
	FileField
)
from flask_babel import lazy_gettext as _



def make_dyna_form(fields_d, submit_text='Submit'):
	class F(Form):
		pass

	for f_name in fields_d:
		setattr(F, f_name, TextField(f_name, validators=[validators.required()]))

	setattr(F, 'submit', SubmitField(submit_text))

	return F



class TemplateUploadForm(Form):
	name     = TextField(_('Template name'), validators=[validators.required()])
	template = FileField(''                , validators=[validators.required()])

	submit   = SubmitField(_('Upload'))



#class ContactForm(Form):
#	name             = TextField('Name'                , validators=[validators.required()])
#	twitter_account  = TextField('Twitter account'     , validators=[validators.required()])
#	email            = html5.EmailField('Email address', validators=[validators.required(), validators.Email()])
#	suggestion       = TextAreaField('Message'         , validators=[validators.required(), validators.length(max=200)])
#	submit           = SubmitField('Send')
#
#
#
#
#class SaveTweetForm(Form):
#	link_or_id = TextField(_('Tweet link'), validators=[validators.required()]) 
#	category   = SelectField(_('Category'), choices=[] )
#	submit     = SubmitField(_('Save'))
#
#
#
#class NewCategoryForm(Form):
#	name   = TextField(_('Category name'), validators=[validators.required(), validators.length(max=20)])
#	submit = SubmitField(_('Create'))
#
#class EditCategoryForm(Form):
#	cat_id   = HiddenField('', validators=[validators.required()])
#	old_name = HiddenField('', validators=[validators.required()])
#	name     = TextField(_('Category name'), validators=[validators.required()])
#	submit   = SubmitField(_('Save'))
#
#
#class MoveToCategoryForm(Form):
#	tweet_id = HiddenField('', validators=[validators.required()])
#	category = SelectField(_('Category'), choices=[] )
#	submit   = SubmitField(_('Move'))
#
#
#class ChangeUserTimelineForm(Form):
#	tw_user = TextField('', validators=[validators.required()])
#
#class SearchTimelineForm(Form):
#	q = TextField('', validators=[validators.required()])
#
#
#
