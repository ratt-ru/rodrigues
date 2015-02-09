import logging
from django.test import TestCase
from . import tasks
from . import models


logger = logging.basicConfig(level=logging.DEBUG)


class TaskTest(TestCase):
    def setUp(self):
        self.simulation = models.Simulation()
        self.simulation.save()

    def test_simulate(self):
        tasks.simulate(self.simulation.id)
