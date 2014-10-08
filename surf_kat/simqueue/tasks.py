from __future__ import absolute_import
import logging
import time
from celery import shared_task


logger = logging.getLogger(__name__)


@shared_task
def simulate(parameters={}):
    logger.warning('simulate called with parameters %s, sleeping 10 seconds!' %
                   parameters)
    time.sleep(10)
    logger.warning('simulate finished!')
    return 'kablam!'