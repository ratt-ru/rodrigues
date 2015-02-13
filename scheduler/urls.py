from django.conf.urls import patterns, url


from .views import (ScheduleForm, ListForm)




schedule_url = url(r'^new/(?P<form_name>\w+)/$',
                   ScheduleForm.as_view(), name='new')

list_url = url(r'^$',
                   ListForm.as_view(), name='list')


all_ = (
    schedule_url,
    list_url,
)

urlpatterns = patterns('', *all_)
