import logging
from datetime import datetime
import tempfile
import shutil
import os

from celery import shared_task
from pytz import timezone
import docker
from django.conf import settings
import requests.exceptions

from scheduler.models import Job


logger = logging.getLogger(__name__)


@shared_task
def simulate(job_id):
    client = docker.Client(**settings.DOCKER_SETTINGS)
    client.version()

    job = Job.objects.get(pk=job_id)
    job.log = "running..."
    job.started = datetime.now(timezone(settings.TIME_ZONE))
    job.save(update_fields=["started", "log"])
    logger.info('starting job %s' % job_id)

    input = tempfile.mkdtemp(dir=settings.RESULTS_DIR,
                             prefix='input-%s-' % job_id)
    output = tempfile.mkdtemp(dir=settings.RESULTS_DIR,
                              prefix='output-%s-' % job_id)

    with open(os.path.join(input, 'parameters.json'), 'w') as sims:
        sims.write((job.config))

    logging.info("creating container from image %s" % job.docker_image)
    try:
        container = client.create_container(image=job.docker_image,
                                            command='/run.sh')
    except requests.exceptions.ConnectionError as e:
        msg = "cant create container: " + str(e)
        logging.error(msg)
        job.log += msg
        job.save()
        return

    client.start(container, binds={input: {'bind': '/input', 'ro': True},
                                   output: {'bind': '/output'}})

    status = client.wait(container)
    job.log += client.logs(container).decode()
    if status:
        msg = "simulation crashed"
        logger.warning(msg)
        job.log += msg
    else:
        msg = "simulation finished"
        logger.info(msg)
        job.log += msg
    job.finished = datetime.now(timezone(settings.TIME_ZONE))
    job.save()
    shutil.rmtree(input)


