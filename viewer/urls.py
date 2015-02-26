from django.conf.urls import patterns, url


from .views import (FitsView)


fits_url = url(r'^(?P<path>(\w.)+)/$', FitsView.as_view(),
                     name='job_create')


all_ = (
    fits_url,
)

urlpatterns = patterns('', *all_)
