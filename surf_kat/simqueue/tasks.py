import logging
from datetime import datetime
from celery import shared_task
from collections import namedtuple
import tempfile
import os
from pytz import timezone
import docker
from requests.exceptions import RequestException
from docker.errors import DockerException
from django.conf import settings
from django.core.files import File

from .models import Simulation
from .config import generate_config



logger = logging.getLogger(__name__)


docker_status = namedtuple('DockerStatus', ['status', 'logs', 'result_dir'])


def run_docker(config):
    try:
        tempdir = tempfile.mkdtemp(dir=settings.RESULTS_DIR)
        tempdir_name = os.path.basename(tempdir)
        config_file = open(os.path.join(tempdir, 'sims.cfg'), 'w')
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

        output = os.path.join(tempdir, 'output.log')
        if os.access(output, os.R_OK):
            logs += "\n * content of output.log:\n"
            logs += open(output, 'r').read()

        return docker_status(status=status, logs=logs, result_dir=tempdir_name)

    except (DockerException, RequestException) as e:
        logger.error("simulation crashed: " + str(e))
        return docker_status(status=1, logs=str(e), result_dir=tempdir_name)


def store_files(simulation, result_dir):
    """
    Store result files in database (if the exist)

    :param simulation: django simulation model object
    :param result_dir: full path to result dir
    """
    files = (
        ('results-uvcov.png', 'results_uvcov'),
        ('results.dirty.fits', 'results_dirty'),
        ('results.model.fits', 'results_model'),
        ('results.residual.fits', 'results_residual'),
        ('results.restored.fits', 'results_restored'),
    )

    for filename, fieldname in files:
        fullpath = os.path.join(result_dir, filename)

        if os.access(fullpath, os.R_OK):
            field = getattr(simulation, fieldname)
            field.save(filename, File(open(fullpath, 'rb')))
        else:
            logger.warning('no %s file for task %s' % (filename, simulation.id))
    simulation.save(update_fields=[f[1] for f in files])


@shared_task
def simulate(simulation_id):
    simulation = Simulation.objects.get(pk=simulation_id)
    simulation.state = simulation.RUNNING
    simulation.log = "running..."
    simulation.started = datetime.now(timezone(settings.TIME_ZONE))
    simulation.save(update_fields=["started", "log", "state"])
    logger.info('starting simulation %s' % simulation_id)

    config = generate_config(simulation)
    results = run_docker(config)

    if results.status:
        simulation.state = simulation.CRASHED
    else:
        simulation.state = simulation.FINISHED

    simulation.log = results.logs
    simulation.finished = datetime.now(timezone(settings.TIME_ZONE))
    simulation.result_dir = results.result_dir

    store_files(simulation, os.path.join(settings.RESULTS_DIR,
                                         results.result_dir))

    simulation.save(update_fields=["finished", "log", "state", "result_dir",
                                   "results_uvcov"])
    return simulation.state