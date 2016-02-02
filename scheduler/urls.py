from django.conf.urls import patterns, url


from .views import (schedule_image, ImageList, JobDelete, JobReschedule,  JobList)


images_list_url = url(r'^images/$', ImageList.as_view(), name='container_list')

job_create_url = url(r'^job/create/(?P<image_id>\d+)/$', schedule_image, name='job_create')

job_delete_url = url(r'^job/delete/(?P<pk>\d+)/$', JobDelete.as_view(), name='job_delete')

job_reschedule_url = url(r'^job/reschedule/(?P<pk>\d+)/$', JobReschedule.as_view(), name='job_reschedule')

job_list_url = url(r'^$', JobList.as_view(), name='job_list')


all_ = (
    images_list_url,
    job_create_url,
    job_delete_url,
    job_reschedule_url,
    job_list_url,
)

urlpatterns = patterns('', *all_)
