import io
import logging
import os
import shutil
import tarfile

from django.conf import settings
from django.core.files import File
from docker.errors import DockerException
from requests import RequestException

from .config import generate_config


logger = logging.getLogger(__name__)


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


def prepare_dockerfile(directory, simulation):
    """
    prepares a docker config from simulation object in directory
    """
    dockerfile = open(os.path.join(directory, 'Dockerfile'), 'w')
    dockerfile.write('FROM %s\nADD /sims.cfg /\n' % settings.DOCKER_IMAGE)

    with open(os.path.join(directory, 'sims.cfg'), 'w') as sims:
        sims.write(generate_config(simulation))

    if simulation.sky_model:
        shutil.copyfile(simulation.sky_model.file.name,
                        os.path.join(directory, 'sky_model'))
        dockerfile.write('ADD sky_model /\n')

    if simulation.tdl_conf:
        shutil.copyfile(simulation.tdl_conf.file.name,
                        os.path.join(directory, 'tdl_conf'))
        dockerfile.write('ADD tdl_conf /\n')

    dockerfile.close()


def run_docker(client, dockerfile_dir, image_name, simulation):
    """
    Run the actual container and do housekeeping.

    :rtype : False, console, container
    """
    console = ""

    for row in client.build(path=dockerfile_dir, tag=image_name):
        logger.info(row)
        console += row
        simulation.console = console
        simulation.save()

    container = client.create_container(image=image_name,
                                        command=settings.DOCKER_CMD)
    client.start(container)

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


