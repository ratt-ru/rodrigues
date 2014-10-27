from django.conf.urls import patterns, url


from simqueue.views import (SimulationCreate, SimulationList, SimulationDetail,
                            Reschedule, SimulationDelete, SimulationConfig,
                            SimulationImage)




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


image_url = url(r'^image/(?P<pk>\d+)/$', SimulationImage.as_view(),
                name='image')


all_ = (
    list_url,
    create_url,
    detail_url,
    reschedule_url,
    delete_url,
    config_url,
    image_url,
)

urlpatterns = patterns('', *all_)
