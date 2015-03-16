from django.conf.urls import patterns, url


from .views import FitsView,  OverView, SomethingView, TextView


fits_url = url(r'^(?P<pk>\d+)/fits/(?P<path>[\w._/]+)/$', FitsView.as_view(),
               name='fits')

text_url = url(r'^(?P<pk>\d+)/text/(?P<path>[\w._/]+)/$', TextView.as_view(),
               name='text')

overview_url = url(r'^(?P<pk>\d+)/overview/$', OverView.as_view(),
                  name='viewer')

something_url = url(r'^something_url/(?P<pk>\d+)/(?P<path>[\w._/]+)/$',
                    SomethingView.as_view(), name='guesstype')

all_ = (
    fits_url,
    overview_url,
    something_url,
    text_url,
)

urlpatterns = patterns('', *all_)
