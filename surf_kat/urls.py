from django.conf.urls import patterns, include, url
from django.contrib import admin
from simqueue.views import SimulationView

urlpatterns = patterns('',
    url(r'^', SimulationView.as_view(template_name='simulation.html')),

    url(r'^admin/', include(admin.site.urls)),
)
