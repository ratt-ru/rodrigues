from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView


simqueue_url = url(r'^simqueue/', include('simqueue.urls'))
login_url = url(r'^accounts/login/$', login, name='login')
logout_url = url(r'^accounts/logout/$', logout, name='logout')
root_url = url(r'$', RedirectView.as_view(url=reverse_lazy('list')),
               name='root')

all_ = (simqueue_url, login_url, logout_url, root_url)
urlpatterns = patterns('', *all_)
