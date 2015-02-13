from django.conf.urls import patterns, url


from .views import (DynamicFormView, FormsList)




schedule_url = url(r'^new/(?P<form_name>\w+)/$', DynamicFormView.as_view(),
                   name='new')
list_url = url(r'^$', FormsList.as_view(), name='list')


all_ = (
    schedule_url,
    list_url,
)

urlpatterns = patterns('', *all_)
