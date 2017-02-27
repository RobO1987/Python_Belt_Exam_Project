from django.conf.urls import url, include
from views import *

urlpatterns = [
    url(r'^$',index, name = 'index'),
    url(r'^register$', register, name = 'register'),
    url(r'^login$', login, name = 'login'),
    url(r'^clearsession$',clearsession, name = 'clearsession'),
    url(r'^quotes$',quotes, name = 'quotes'),
    url(r'^quotecontribute$',quotecontribute, name = 'quotecontribute'),
    url(r'^favquote/(?P<quote_id>\d+)$',favquote, name = 'favquote'),
    url(r'^quoteuser/(?P<quote_user_id>\d+)$',quoteuser,name = 'quoteuser'),
    url(r'^remove/(?P<fav_id>\d+)$',remove, name = 'remove')
    ]
