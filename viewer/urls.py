from django.conf.urls import patterns, url


from .views import FitsView,  ListDirView, SomethingView


fits_url = url(r'^(?P<pk>\d+)/(?P<path>[\w._]+)/$', FitsView.as_view(),
               name='fits')

listdir_url = url(r'^dirlist/(?P<pk>\d+)/$', ListDirView.as_view(),
                  name='listdir')

something_url = url(r'^something_url/(?P<pk>\d+)/(?P<path>[\w._]+)/$',
                    SomethingView.as_view(), name='guesstype')

all_ = (
    fits_url,
    listdir_url,
    something_url,
)

urlpatterns = patterns('', *all_)
