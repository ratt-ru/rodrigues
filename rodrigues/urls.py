from django.conf.urls import patterns, include, url
from django.contrib.auth.views import login, logout
from django.contrib import admin
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static


admin_url = url(r'^admin/', include(admin.site.urls))
login_url = url(r'^accounts/login/$', login, name='login')
logout_url = url(r'^accounts/logout/$', logout, name='logout')
scheduler_url = url(r'^scheduler/', include('scheduler.urls'))
root_url = url(r'^$', RedirectView.as_view(url=reverse_lazy('job_list')),
               name='root')
viewer_url = url(r'^viewer/', include('viewer.urls'))

all_ = (admin_url, login_url, logout_url, scheduler_url, root_url, viewer_url)
urlpatterns = patterns('', *all_)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
