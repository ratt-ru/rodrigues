from django.test import TestCase
from simqueue import tasks


class TaskTest(TestCase):
    def test_simulate(self):
        tasks.simulate()

    def test_delay_simulate(self):
        tasks.simulate.delay()