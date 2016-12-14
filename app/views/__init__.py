#encoding: utf-8
from app import app

from indexview import (
    IndexView,
)
app.add_url_rule('/', view_func=IndexView.as_view('index'))

from templateview import (
	TemplateUploadView,
	TemplateDeleteView,
	TemplateDownloadView,
)
app.add_url_rule('/template/upload', view_func=TemplateUploadView.as_view('template.upload'))
app.add_url_rule('/template/delete/<tid>', view_func=TemplateDeleteView.as_view('template.delete'))
app.add_url_rule('/template/download/<tid>', view_func=TemplateDownloadView.as_view('template.download'))

from varsenvview import (
	VarsEnvView,
)
app.add_url_rule('/variables/environment/<eid>/template/<tid>', view_func=VarsEnvView.as_view('varsenv.edit'))


