#encoding: utf-8
from app import app

from indexview import (
    IndexView,
)
app.add_url_rule('/', view_func=IndexView.as_view('index'))

