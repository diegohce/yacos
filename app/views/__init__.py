#encoding: utf-8
from app import app


from loginview import (
	LoginView,
	LogoutView,
)
app.add_url_rule('/login', view_func=LoginView.as_view('login'))
app.add_url_rule('/logout', view_func=LogoutView.as_view('logout'))



from indexview import (
    IndexView,
)
app.add_url_rule('/', view_func=IndexView.as_view('index'))

from templateview import (
	TemplateUploadView,
	TemplateDeleteView,
	TemplateDownloadView,
	TemplateEditView,
)
app.add_url_rule('/template/upload', view_func=TemplateUploadView.as_view('template.upload'))
app.add_url_rule('/template/delete/<tid>', view_func=TemplateDeleteView.as_view('template.delete'))
app.add_url_rule('/template/download/<tid>', view_func=TemplateDownloadView.as_view('template.download'))
app.add_url_rule('/template/edit/<tid>', view_func=TemplateEditView.as_view('template.edit'))
app.add_url_rule('/template/edit/save', view_func=TemplateEditView.as_view('template.save'))

from varsenvview import (
	VarsEnvView,
	ConfigDownloadView,
)
app.add_url_rule('/variables/environment/<eid>/template/<tid>', view_func=VarsEnvView.as_view('varsenv.edit'))
app.add_url_rule('/config/download/<ename>/<tname>', view_func=ConfigDownloadView.as_view('config.download'))


