from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout


admin_url = url(r'^admin/', include(admin.site.urls))
login_url = url(r'^accounts/login/$', login, name='login')
logout_url = url(r'^accounts/logout/$', logout, name='logout')
scheduler_url = url(r'^scheduler/', include('scheduler.urls'))


all_ = (admin_url, login_url, logout_url, scheduler_url)
urlpatterns = patterns('', *all_)
