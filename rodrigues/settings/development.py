from .base import *
from docker.utils import kwargs_from_env


DOCKER_SETTINGS = kwargs_from_env()

# required foor boot2docker
if 'tls' in DOCKER_SETTINGS:
    DOCKER_SETTINGS['tls'].assert_hostname = False
