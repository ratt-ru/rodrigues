from django.conf.urls import patterns, url


from .views import (FitsView)


fits_url = url(r'^(?P<path>[\w._]+)/$', FitsView.as_view(),
                     name='fits')


all_ = (
    fits_url,
)

urlpatterns = patterns('', *all_)
