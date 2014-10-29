import logging
from datetime import datetime
from celery import shared_task
from collections import namedtuple
import tempfile
import tarfile
import os
import io
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


docker_status = namedtuple('DockerStatus', ['status', 'logs', 'result_dir'])


files = (
    ('results-uvcov.png', 'results_uvcov'),
    ('results.dirty.fits', 'results_dirty'),
    ('results.model.fits', 'results_model'),
    ('results.residual.fits', 'results_residual'),
    ('results.restored.fits', 'results_restored'),
)


def docker_copy(docker_client, container_id, path, target="."):
    """
    Copy is not implemented in docker-py, so we do it ourself.

    args:
        docker_client: a docker client object
        container_id: ID of the container to copy from
        path: path to the file in the container
        target: folder where to put the file
    """
    response = docker_client.copy(container_id, path)
    buffer = io.BytesIO()
    buffer.write(response.data)
    buffer.seek(0)
    tar = tarfile.open(fileobj=buffer, mode='r|')
    tar.extractall(path=target)


def run_docker(config, simulation):
    try:
        result_dir = tempfile.mkdtemp(dir=settings.RESULTS_DIR)
        input_dir = tempfile.mkdtemp(dir=settings.RESULTS_DIR)
        tempdir_name = os.path.basename(result_dir)
        config_file = open(os.path.join(input_dir, 'sims.cfg'), 'w')
        config_file.write(config)
        config_file.close()
        docker_client = docker.Client(settings.DOCKER_URI)
        container_id = docker_client.create_container(image=settings.DOCKER_IMAGE,
                                                      command=settings.DOCKER_CMD,
                                                      )
        docker_client.start(container_id, binds={input_dir: {'bind': '/input',
                                                             'ro': False}})

        if docker_client.wait(container_id):
            logger.warning('simulation exited with an error')
            status = True
        else:
            logger.info('simulate finished')
            status = False
        logs = docker_client.logs(container_id).decode()

        # logfile is same as stdout but with more detail
        try:
            docker_copy(docker_client, container_id,
                        path='/results/' + 'output.log', target=result_dir)
        except (DockerException, RequestException) as e:
            logger.error(str(e))
            logging.error('cant find output.log inside container')
        else:
            logs = open(os.path.join(result_dir, 'output.log'), 'r').read()

        for filename, fieldname in files:
            try:
                docker_copy(docker_client, container_id,
                            path='/results/' + filename, target=result_dir)
            except (DockerException, RequestException) as e:
                logger.error(str(e))
                logging.error('cant find %s inside container' % filename)
            else:
                fullpath = os.path.join(result_dir, filename)
                field = getattr(simulation, fieldname)
                field.save(filename, File(open(fullpath, 'rb')))
                simulation.save(update_fields=[fieldname])

        return docker_status(status=status, logs=logs, result_dir=tempdir_name)

    except (DockerException, RequestException) as e:
        error = "Running container failed: " + str(e)
        logger.error(error)
        return docker_status(status=1, logs=error, result_dir=tempdir_name)



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
    simulation.result_dir = results.result_dir
    simulation.save(update_fields=["finished", "log", "state", "result_dir",
                                   "results_uvcov"])
    return simulation.state


def schedule_simulation(simulation, request):
    """
    schedule a simulation task, catch error if problem, log in all cases.
    """
    try:
        async = simulate.delay(simulation_id=simulation.id)
    except OSError as e:
            error = "can't start simulation %s: %s" % (simulation.id,
                                                       str(e))
            messages.error(request, error)
            logger.error(error)
            simulation.set_crashed(error)
    else:
        simulation.task_id = async.task_id
        simulation.save(update_fields=["task_id"])
        simulation.set_scheduled()