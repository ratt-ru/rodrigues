import logging
from celery import shared_task
import docker
from docker.errors import DockerException
from datetime import datetime
from django.conf import settings
from simqueue.models import Simulation
from collections import namedtuple
logger = logging.getLogger(__name__)


docker_status = namedtuple('DockerStatus', ['status', 'logs'])


def run_docker():
    try:
        docker_client = docker.Client(settings.DOCKER_URI)
        container_id = docker_client.create_container(settings.DOCKER_IMAGE,
                                                      settings.DOCKER_CMD)
        docker_client.start(container_id)

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
    simulation.started = datetime.now()
    simulation.save()
    logger.info('starting simulation %s' % simulation_id)

    results = run_docker()

    if results.status:
        simulation.state = simulation.CRASHED
    else:
        simulation.state = simulation.FINISHED

    simulation.log = results.logs
    simulation.finished = datetime.now()
    simulation.save()