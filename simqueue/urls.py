from django.conf.urls import patterns, url


from .views import (SimulationCreate, SimulationList, SimulationDetail,
                    Reschedule, SimulationDelete, SimulationConfig,
                    SimulationFits)




create_url = url(r'^create/', SimulationCreate.as_view(), name='create')

delete_url = url(r'^delete/(?P<pk>\d+)/$', SimulationDelete.as_view(),
                 name='delete')

detail_url = url(r'^detail/(?P<pk>\d+)/$', SimulationDetail.as_view(),
                 name='detail')

config_url = url(r'^config/(?P<pk>\d+)/$', SimulationConfig.as_view(),
                 name='config')

reschedule_url = url(r'^reschedule/(?P<pk>\d+)/$', Reschedule.as_view(),
                     name='reschedule')

list_url = url(r'^$', SimulationList.as_view(), name='list')

fits_url = url(r'^fits/(?P<pk>\d+)/(?P<field>\w+)/$', SimulationFits.as_view(),
               name='fits')


all_ = (
    list_url,
    create_url,
    detail_url,
    reschedule_url,
    delete_url,
    config_url,
    fits_url,
)

urlpatterns = patterns('', *all_)
