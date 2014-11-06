import logging
from datetime import datetime
from celery import shared_task
from collections import namedtuple
import tempfile
import tarfile
import os
import io
import json
import socket
import shutil
from django.contrib import messages
from pytz import timezone
import docker
from requests.exceptions import RequestException
from docker.errors import DockerException
from django.conf import settings
from django.core.files import File

from .models import Simulation
from .config import generate_config


logger = logging.getLogger(__name__)


docker_status = namedtuple('DockerStatus', ['status', 'logs'])


# (filename in container, field in database)
files = (
    ('results-uvcov.png', 'results_uvcov'),
    ('results.dirty.fits', 'results_dirty'),
    ('results.model.fits', 'results_model'),
    ('results.residual.fits', 'results_residual'),
    ('results.restored.fits', 'results_restored'),
    ('output.log', ''),
)


def docker_copy(client, container_id, path, target="."):
    """
    Copy is not implemented in docker-py, so we do it ourself.

    args:
        client: a docker client object
        container_id: ID of the container to copy from
        path: path to the file in the container
        target: folder where to put the file
    """
    logger.info("copying %s from container to %s" % (path, target))
    response = client.copy(container_id, path)
    buffer = io.BytesIO()
    buffer.write(response.data)
    buffer.seek(0)
    tar = tarfile.open(fileobj=buffer, mode='r|')
    tar.extractall(path=target)


def run_docker(config, simulation):
    """
    Run the actual container and do housekeeping.
    """
    try:
        temp_dir = tempfile.mkdtemp(dir=settings.RESULTS_DIR)
        client = docker.Client(settings.DOCKER_URI)

        cmd = "/runner.py '%s'" % json.dumps({'sims.cfg': config})
        logging.error(cmd)
        container_id = client.create_container(image=settings.DOCKER_IMAGE,
                                               command=cmd,
                                               )
        client.start(container_id)

        if client.wait(container_id):
            logger.warning('simulation exited with an error')
            status = True
        else:
            logger.info('simulate finished')
            status = False

        logs = client.logs(container_id).decode()

        for filename, fieldname in files:
            try:
                docker_copy(client, container_id,
                            path='/results/' + filename, target=temp_dir)
            except (DockerException, RequestException) as e:
                logger.error(str(e))
                logging.error('cant find %s inside container' % filename)
            else:
                if filename == 'output.log':
                    logs = open(os.path.join(temp_dir, 'output.log'), 'r').read()
                else:
                    fullpath = os.path.join(temp_dir, filename)
                    field = getattr(simulation, fieldname)
                    field.save(filename, File(open(fullpath, 'rb')))
                    logger.info('copied %s to %s' % (filename, field.file))
                    simulation.save(update_fields=[fieldname])

        shutil.rmtree(temp_dir)
        return docker_status(status=status, logs=logs)

    except (DockerException, RequestException) as e:
        error = "Running container failed: " + str(e)
        logger.error(error)
        return docker_status(status=1, logs=error)



@shared_task
def simulate(simulation_id):
    simulation = Simulation.objects.get(pk=simulation_id)
    simulation.state = simulation.RUNNING
    simulation.log = "running..."
    simulation.started = datetime.now(timezone(settings.TIME_ZONE))
    simulation.save(update_fields=["started", "log", "state"])
    logger.info('starting simulation %s' % simulation_id)

    config = generate_config(simulation)
    results = run_docker(config, simulation)

    if results.status:
        simulation.state = simulation.CRASHED
    else:
        simulation.state = simulation.FINISHED

    simulation.log = results.logs
    simulation.finished = datetime.now(timezone(settings.TIME_ZONE))
    simulation.save(update_fields=["finished", "log", "state", "results_uvcov"])
    return simulation.state


def schedule_simulation(simulation, request):
    """
    schedule a simulation task, catch error if problem, log in all cases.
    """
    try:
        async = simulate.delay(simulation_id=simulation.id)
    except (OSError, socket.error) as e:
        error = "can't start simulation %s: %s" % (simulation.id,
                                                   str(e))
        messages.error(request, error)
        logger.error(error)
        simulation.set_crashed(error)
    else:
        simulation.task_id = async.task_id
        simulation.save(update_fields=["task_id"])
        simulation.set_scheduled()