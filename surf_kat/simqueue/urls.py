from django.conf.urls import patterns, include, url
from django.contrib import admin

from simqueue.views import (SimulationCreate, SimulationList, SimulationDetail,
                            Reschedule, SimulationDelete)


admin_url = url(r'^admin/', include(admin.site.urls))

list_url = url(r'^$', SimulationList.as_view(), name='list')

create_url = url(r'^create/', SimulationCreate.as_view(), name='create')

delete_url = url(r'^delete/(?P<pk>\d+)/$', SimulationDelete.as_view(),
                 name='delete')

detail_url = url(r'^detail/(?P<pk>\d+)/$', SimulationDetail.as_view(),
                 name='detail')

reschedule_url = url(r'^reschedule/(?P<pk>\d+)/$', Reschedule.as_view(),
                     name='reschedule')


all_ = (admin_url, list_url, create_url, detail_url, reschedule_url, delete_url)
urlpatterns = patterns('', *all_)
