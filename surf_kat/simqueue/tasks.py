import logging
from datetime import datetime
from celery import shared_task
from collections import namedtuple
import tempfile
from os import path
import os
from pytz import timezone
import docker
from requests.exceptions import RequestException
from docker.errors import DockerException
from django.conf import settings

from .models import Simulation
from .config import generate_config


logger = logging.getLogger(__name__)


docker_status = namedtuple('DockerStatus', ['status', 'logs'])


def run_docker(config):
    try:
        tempdir = tempfile.mkdtemp(dir=path.join(settings.BASE_DIR,
                                                 'tmp_results'))
        config_file = open(path.join(tempdir, 'sims.cfg'), 'w')
        config_file.write(config)
        config_file.close()
        docker_client = docker.Client(settings.DOCKER_URI)
        container_id = docker_client.create_container(image=settings.DOCKER_IMAGE,
                                                      command=settings.DOCKER_CMD,
                                                      )
        docker_client.start(container_id, binds={tempdir: {'bind': '/results',
                                                           'ro': False}})

        if docker_client.wait(container_id):
            logger.warning('simulation exited with an error')
            status = True
        else:
            logger.info('simulate finished')
            status = False
        logs = docker_client.logs(container_id).decode()

        output = path.join(tempdir, 'output.log')
        if os.access(output, os.R_OK):
            logs += "\n * content of output.log:\n"
            logs + open(output, 'r').read()

        return docker_status(status=status, logs=logs)

    except (DockerException, RequestException) as e:
        logger.error("simulation crashed: " + str(e))
        return docker_status(status=1, logs=str(e))


@shared_task
def simulate(simulation_id):
    simulation = Simulation.objects.get(pk=simulation_id)
    simulation.state = simulation.RUNNING
    simulation.log = "running..."
    simulation.started = datetime.now(timezone(settings.TIME_ZONE))
    simulation.save()
    logger.info('starting simulation %s' % simulation_id)

    config = generate_config(simulation)
    results = run_docker(config)

    if results.status:
        simulation.state = simulation.CRASHED
    else:
        simulation.state = simulation.FINISHED

    simulation.log = results.logs
    simulation.finished = datetime.now(timezone(settings.TIME_ZONE))
    simulation.save()