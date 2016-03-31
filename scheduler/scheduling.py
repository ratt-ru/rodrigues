import json
import os
import socket
import tempfile
import logging

from django.conf import settings
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from scheduler.models import Job
from scheduler.tasks import run_job


logger = logging.getLogger(__name__)


def schedule_job(job, request):
    """
    schedule a simulation task, catch error if problem, log in all cases.
    args:
        job: a rodrigues job model object
        request: a Django request
    """
    try:
        async = run_job.delay(job_id=job.id)
    except (OSError, socket.error) as e:
        job.state = job.CRASHED
        error = "can't connect to broker %s: %s" % (job.id, str(e))
        messages.error(request, error)
        logger.error(error)
        job.log = error
    else:
        job.task_id = async.task_id
        job.state = job.SCHEDULED
    job.save()


def format_form(cleaned_data):
    """
    Workaround to set the uploaded file name for a InMemoryUploadedFile corrrectly.
    Args:
        cleaned_data (dict):

    Returns:
        dict:

    """
    d = {}
    for k, v in cleaned_data.items():
        if type(v) is InMemoryUploadedFile:
            d[k] = v.name
        else:
            d[k] = v
    return d


def create_job(form, request, image):
    """
    Create a job, prepare the run but don't run yet.

    Args:
        form (django.forms.Form): A Django form
        request (django.http.request.HttpRequest): A Django HTTP request
        image (str): The image to use for the job

    Returns:
        tuple: (bool indicating success, error string)

    """
    job = Job()
    job.owner = request.user
    job.config = json.dumps(format_form(form.cleaned_data))
    job.name = form.data['kliko_name']
    job.image = image
    job.save()

    # Create the placeholder for container IO
    try:
        tempdir = tempfile.mkdtemp(dir=os.path.realpath(settings.MEDIA_ROOT),
                                   prefix=str(job.id) + '-')

        # Nginx container runs as unprivileged
        os.chmod(tempdir, 0o0755)

        input_ = os.path.join(tempdir, 'input')
        output = os.path.join(tempdir, 'output')

        os.mkdir(input_)
        os.mkdir(output)
    except Exception as e:
        return False, "Can't setup working directory:\n%s" % str(e)

    for fieldname, data in request.FILES.items():
        filename = request.FILES[fieldname].name
        with open(os.path.join(input_, filename), 'wb+') as destination:
            for chunk in data.chunks():
                destination.write(chunk)

    job.results_dir = os.path.basename(tempdir)
    job.save()
    schedule_job(job, request)
    return True, ""
