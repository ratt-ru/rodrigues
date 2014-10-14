from django.conf.urls import patterns, include, url
from django.contrib import admin
from simqueue.views import SimulationCreate, SimulationList, SimulationDetail
from django.contrib.auth.views import login as login_view
from django.contrib.auth.views import logout as logout_view

admin = url(r'^admin/', include(admin.site.urls))
list_ = url(r'^$', SimulationList.as_view(), name='list')
detail = url(r'^(?P<pk>\d+)/$', SimulationDetail.as_view(), name='detail')
create = url(r'^create/', SimulationCreate.as_view(), name='create')
login = url(r'^accounts/login/$', login_view, name='login')
logout = url(r'^accounts/logout/$', logout_view, name='logout')


all_ = (admin, list_, create, detail, login, logout)

urlpatterns = patterns('', *all_)
