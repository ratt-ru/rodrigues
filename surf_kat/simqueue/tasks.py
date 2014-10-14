import logging
from datetime import datetime
from celery import shared_task
from collections import namedtuple
import tempfile
from os import path

from pytz import timezone
import docker
from docker.errors import DockerException
from django.conf import settings

from simqueue.models import Simulation


logger = logging.getLogger(__name__)


docker_status = namedtuple('DockerStatus', ['status', 'logs'])


def run_docker(config):
    try:
        tempdir = tempfile.mkdtemp()
        docker_client = docker.Client(settings.DOCKER_URI)
        container_id = docker_client.create_container(settings.DOCKER_IMAGE,
                                                      settings.DOCKER_CMD,
                                                      volumes=['/results']
                                                      )
        docker_client.start(container_id, binds={tempdir: {'bind': '/results',
                                                           'ro': False}})

        config_file = open(path.join(tempdir, 'sims.cfg'), 'w')
        config_file.write(config)
        config_file.close()

        if docker_client.wait(container_id):
            logger.warning('simulation crashed')
            status = True
        else:
            logger.info('simulate finished')
            status = False
        return docker_status(status=status, logs=docker_client.logs(container_id))
    except DockerException as e:
        return docker_status(status=1, logs=str(e))


@shared_task
def simulate(simulation_id):
    simulation = Simulation.objects.get(pk=simulation_id)
    simulation.state = simulation.RUNNING
    simulation.started = datetime.now(timezone(settings.TIME_ZONE))
    simulation.save()
    logger.info('starting simulation %s' % simulation_id)

    config = simulation.config()
    results = run_docker(config)

    if results.status:
        simulation.state = simulation.CRASHED
    else:
        simulation.state = simulation.FINISHED

    simulation.log = results.logs
    simulation.finished = datetime.now(timezone(settings.TIME_ZONE))
    simulation.save()