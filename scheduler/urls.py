from django.conf.urls import url
from scheduler import views
from django.conf.urls import include
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'images', views.KlikoImageViewSet)
router.register(r'jobs', views.JobViewSet)


urlpatterns = [
    url(r'^images/$', views.ImageList.as_view(), name='image_list'),
    url(r'^image/create/$', views.ImageCreate.as_view(), name='image_create'),
    url(r'^image/delete/(?P<pk>\d+)/$', views.ImageDelete.as_view(), name='image_delete'),
    url(r'^image/pull/(?P<pk>\d+)/$', views.ImagePull.as_view(), name='image_pull'),
    url(r'^job/create/(?P<image_id>\d+)/$', views.schedule_image, name='job_create'),
    url(r'^job/reschedule/(?P<template_job_id>\d+)/$', views.reschedule_image, name='job_reschedule'),
    url(r'^job/delete/(?P<pk>\d+)/$', views.JobDelete.as_view(), name='job_delete'),
    url(r'^$', views.JobList.as_view(), name='job_list'),
    url(r'^rest/', include(router.urls)),
    url(r'^rest/auth/', include('rest_framework.urls', namespace='rest_framework'))
]
