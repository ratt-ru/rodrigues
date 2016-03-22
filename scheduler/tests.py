from django.test import TestCase
from django.conf import settings
import docker
from scheduler.tasks import pull_image


import logging
logging.basicConfig(level=logging.DEBUG)


class TaskTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = docker.Client(**settings.DOCKER_SETTINGS)

    def test_pull_image(self):
        pull_image.apply('alpine')
