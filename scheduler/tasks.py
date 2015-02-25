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
    job = Job.objects.get(pk=job_id)
    job.log = "running..."
    job.started = datetime.now(timezone(settings.TIME_ZONE))
    job.save(update_fields=["started", "log"])
    logger.info('starting job %s' % job_id)

    temp_dir = tempfile.mkdtemp(dir=settings.RESULTS_DIR)
    input = os.path.join(temp_dir, 'input')
    output = os.path.join(temp_dir, 'output')
    os.mkdir(input)
    os.mkdir(output)
    with open(os.path.join(input, 'parameters.json'), 'w') as sims:
        sims.write((job.config))
    client = docker.Client(**settings.DOCKER_SETTINGS)
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
    logger.info('simulate finished')
    job.finished = datetime.now(timezone(settings.TIME_ZONE))
    job.save(update_fields=["finished", "log"])
    shutil.rmtree(temp_dir)


