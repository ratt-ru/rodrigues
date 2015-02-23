import logging
from datetime import datetime
import socket
import tempfile
import shutil

from celery import shared_task
from django.contrib import messages
from pytz import timezone
import docker
from docker.errors import DockerException
from django.conf import settings
from requests import RequestException, ConnectionError

from .models import Job
from .dockering import prepare_dockerfile, run_docker, extract_files


logger = logging.getLogger(__name__)


@shared_task
def simulate(simulation_id):
    simulation = Job.objects.get(pk=simulation_id)
    simulation.state = simulation.RUNNING
    simulation.console = "running..."
    simulation.started = datetime.now(timezone(settings.TIME_ZONE))
    simulation.save(update_fields=["started", "console"])
    logger.info('starting simulation %s' % simulation_id)

    temp_dir = tempfile.mkdtemp(dir=settings.RESULTS_DIR)
    prepare_dockerfile(temp_dir, simulation)
    client = docker.Client(settings.DOCKER_URI)
    simulation_name = 'simulation_' + str(simulation.id)
    try:
        failed, console, container = run_docker(client=client,
                                                dockerfile_dir=temp_dir,
                                                image_name=simulation_name,
                                                simulation=simulation)
    except (DockerException, RequestException, ConnectionError) as e:
        logging.error("can't start container: " + str(e))

    if failed:
        simulation.state = simulation.CRASHED
    else:
        simulation.state = simulation.FINISHED
    simulation.console = console
    simulation.finished = datetime.now(timezone(settings.TIME_ZONE))
    if container:
        extract_files(client, temp_dir, container, simulation)
    simulation.save(update_fields=["finished", "log", "console"
                                   "results_uvcov"])
    shutil.rmtree(temp_dir)


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
        simulation.log = error
        simulation.save()
    else:
        simulation.task_id = async.task_id
        simulation.save(update_fields=["task_id"])
        simulation.set_scheduled()