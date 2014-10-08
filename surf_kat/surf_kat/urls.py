from django.conf.urls import patterns, include, url
from django.contrib import admin
from simqueue.views import SimulationView


admin = url(r'^admin/', include(admin.site.urls))
simul = url(r'^', SimulationView.as_view(template_name='simulation.html',
                                         success_url='/'))

urlpatterns = patterns('',
                       admin,
                       simul,
)
