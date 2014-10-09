import logging
import time
from celery import shared_task
from simqueue.models import Simulation

logger = logging.getLogger(__name__)


@shared_task
def simulate(simulation_id):
    simulation = Simulation.objects.get(pk=simulation_id)
    simulation.state = simulation.RUNNING
    simulation.save()
    logger.info('starting simulation %s' % simulation_id)
    time.sleep(50)
    logger.info('simulate finished!')
    simulation.state = simulation.FINISHED
    simulation.save()