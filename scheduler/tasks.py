import logging
from datetime import datetime
from os import path

from celery import shared_task
from pytz import timezone
import docker
import json
from django.conf import settings
from django.core.mail import send_mail
import requests.exceptions

from scheduler.models import Job, KlikoImage


logger = logging.getLogger(__name__)

mail_body = """
Your RODRIGUES job has %s.

ID: %s
name: %s
started: %s
finished: %s
duration: %s


%s
"""


def crashed(job, msg):
    job.log += msg
    job.state = job.CRASHED
    job.finished = datetime.now(timezone(settings.TIME_ZONE))
    job.save()
    logger.error(msg)
    body = mail_body % ('crashed', job.id, job.name, job.started,
                        job.finished, job.duration(), job.log)
    try:
        send_mail('Your RODRIGUES job %s has crashed' % job.id, body,
                  settings.SERVER_EMAIL, [job.owner.email], fail_silently=False)
    except ConnectionRefusedError as e:
        logging.error("Job crashed, but can't send email: " + str(e))


@shared_task
def run_job(job_id):
    job = Job.objects.get(pk=job_id)
    job.log = "running...\n"
    job.state = job.RUNNING
    job.started = datetime.now(timezone(settings.TIME_ZONE))
    job.save()
    logger.info('starting job %s' % job_id)

    client = docker.Client(**settings.DOCKER_SETTINGS)

    try:
        client.version()
    except requests.exceptions.ConnectionError as e:
        msg = "Can't connect to docker daemon:\n%s\n" % str(e)
        crashed(job, msg)
        raise

    storage = path.join(path.realpath(settings.MEDIA_ROOT), job.results_dir)
    host_storage = path.join(path.realpath(settings.HOST_STORAGE), job.results_dir)

    with open(path.join(storage, 'input/parameters.json'), 'w') as f:
        f.write((job.config))

    logging.info("creating container from image %s" % job.docker_image)
    try:
        container = client.create_container(image=job.docker_image,
                                            host_config=client.create_host_config(
                                                binds=[
                                                    host_storage + '/input:/input:ro',
                                                    host_storage + '/output:/output:rw',
                                                    ]))
    except (requests.exceptions.ConnectionError,
            requests.exceptions.HTTPError) as e:
        msg = "cant create container: %s" % str(e)
        crashed(job, msg)
        raise

    try:
        if hasattr(settings, 'CONTAINER'):
            client.start(container)
        else:
            client.start(container)
    except requests.exceptions.HTTPError as e:
        msg = "can't start container: %s" % str(e)
        crashed(job, msg)
        raise

    state = client.wait(container)
    job.log += client.logs(container).decode()
    if state != 0:
        msg = "simulation crashed (state %s)" % state
        crashed(job, msg)
    else:
        msg = "simulation finished"
        logger.info(msg)
        job.state = job.FINISHED
        job.log += msg
        job.finished = datetime.now(timezone(settings.TIME_ZONE))
        job.save()
        body = mail_body % ('finished', job.id, job.name, job.started,
                            job.finished, job.duration(), job.log)
        try:
            send_mail('Your RODRIGUES job %s has finished' % job.id, body,
                    settings.SERVER_EMAIL, [job.owner.email], fail_silently=False)
        except ConnectionRefusedError as e:
            logger.error("can't sent email: " + str(e))


@shared_task
def pull_image(kliko_image_id):
    client = docker.Client(**settings.DOCKER_SETTINGS)

    try:
        client.version()
    except requests.exceptions.ConnectionError as e:
        msg = "Can't connect to docker daemon:\n%s\n" % str(e)
        logger.error(msg)
        raise

    kliko_image = KlikoImage.objects.get(pk=kliko_image_id)
    kliko_image.state = kliko_image.PULLING
    kliko_image.save()

    errors = ""

    for line in client.pull(kliko_image.repository, kliko_image.tag, stream=True):
        line = json.loads(line.decode('utf-8'))
        if 'error' in line:
            errors += line['error']
            logging.error(line['error'])
        elif 'status' in line:
            logging.info(line['status'])
        else:
            raise Exception('unknown return code')

    if errors:
        kliko_image.state = kliko_image.NOT_PULLED
        kliko_image.error_message = errors
    else:
        kliko_image.last_updated = datetime.now(timezone(settings.TIME_ZONE))
        kliko_image.state = kliko_image.PULLED
    kliko_image.save()
