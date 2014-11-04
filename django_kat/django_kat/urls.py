from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.views.generic import RedirectView
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


admin_url = url(r'^admin/', include(admin.site.urls))
simqueue_url = url(r'^simqueue/', include('simqueue.urls'))
login_url = url(r'^accounts/login/$', login, name='login')
logout_url = url(r'^accounts/logout/$', logout, name='logout')
root_url = url(r'^$', RedirectView.as_view(url=reverse_lazy('list')),
               name='root')


all_ = (admin_url, simqueue_url, login_url, logout_url, root_url)
urlpatterns = patterns('', *all_)


#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)