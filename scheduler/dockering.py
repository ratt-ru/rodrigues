
import io
import logging
import os
import shutil
import tarfile

from django.conf import settings
from django.core.files import File
from docker.errors import DockerException
from requests import RequestException



logger = logging.getLogger(__name__)


# (filename in container, field in database)
files = (
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


def prepare_dockerfile(directory, job):
    """
    prepares a docker config from job object in directory
    """
    dockerfile = open(os.path.join(directory, 'Dockerfile'), 'w')
    dockerfile.write('FROM %s\nADD /parameters.json /\n' % job.docker_image)

    with open(os.path.join(directory, 'parameters.json'), 'w') as sims:
        sims.write((job.config))

    dockerfile.close()


def run_docker(client, dockerfile_dir, image_name, simulation):
    """
    Run the actual container and do housekeeping.

    :rtype : False, console, container
    """
    console = ""

    try:
        rows = client.build(path=dockerfile_dir, tag=image_name)
        for row in rows:
            logger.info(row)
            console += row
            simulation.console = console
            simulation.save()
    except Exception as e:
        error = "can't build container: " + str(e)
        logging.error(error)
        console += error
        return True, console, False

    try:
        container = client.create_container(image=image_name,
                                            command='/run.sh')
    except Exception as e:
        error = "can't create container: " + str(e)
        logging.error(error)
        console += error
        return True, console, False

    try:
        client.start(container)
    except Exception as e:
        error = "can't start container: " + str(e)
        logging.error(error)
        console += error
        return True, console, False

    # capture logs
    for line in client.attach(container=container, stream=True,
                              logs=True, stderr=True, stdout=True):
        row = line.decode()
        logger.info(row)
        console += row
        simulation.console = console
        simulation.save()

    if client.wait(container):
        logger.error('simulation crashed')
        return True, console, container

    logger.info('simulate finished')
    return False, console, container


# (filename in container, field in database)
files = (
    ('results-uvcov.png', 'results_uvcov'),
    ('results.dirty.fits', 'results_dirty'),
    ('results.model.fits', 'results_model'),
    ('results.residual.fits', 'results_residual'),
    ('results.restored.fits', 'results_restored'),
    ('output.log', 'log'),
)


def extract_files(client, temp_dir, container, simulation):
    """
    Extract files from a container

    :param client: Docker client
    :param temp_dir:  where to put the files
    :param container: from which container to take the files
    :param simulation: which simulation Django object to update
    """

    for filename, fieldname in files:
        try:
            docker_copy(client, container['Id'],
                        path='/results/' + filename, target=temp_dir)
        except (DockerException, RequestException) as e:
            logger.error(str(e))
            logging.error('cant find %s inside container' % filename)
        else:
            fullpath = os.path.join(temp_dir, filename)
            field = getattr(simulation, fieldname)
            field.save(filename, File(open(fullpath, 'rb')))
            logger.info('copied %s to %s' % (filename, field.file))
            simulation.save(update_fields=[fieldname])
