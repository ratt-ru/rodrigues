from django.conf.urls import patterns, url
from .views import (schedule_image, ImageList, ImageDelete, ImagePull,
                    JobDelete, ImageCreate, reschedule_image,  JobList)

image_list_url = url(r'^images/$', ImageList.as_view(), name='image_list')

image_create_url = url(r'^image/create/$', ImageCreate.as_view(), name='image_create')

image_delete_url = url(r'^image/delete/(?P<pk>\d+)/$', ImageDelete.as_view(), name='image_delete')

image_pull_url = url(r'^image/pull/(?P<pk>\d+)/$', ImagePull.as_view(), name='image_pull')

job_create_url = url(r'^job/create/(?P<image_id>\d+)/$', schedule_image, name='job_create')

job_reschedule_url = url(r'^job/reschedule/(?P<template_job_id>\d+)/$', reschedule_image, name='job_reschedule')

job_delete_url = url(r'^job/delete/(?P<pk>\d+)/$', JobDelete.as_view(), name='job_delete')

job_list_url = url(r'^$', JobList.as_view(), name='job_list')


all_ = (
    image_list_url,
    image_create_url,
    image_delete_url,
    image_pull_url,
    job_create_url,
    job_delete_url,
    job_reschedule_url,
    job_list_url,
)

urlpatterns = patterns('', *all_)
