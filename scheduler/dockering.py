import logging


logger = logging.getLogger(__name__)


def run_docker(client, image_name, input, output):
    """
    Run the actual container and do housekeeping.

    :returns: crashed (bool), log, container
    """
    log = ""

    try:
        container = client.create_container(image=image_name,
                                            command='/run.sh')
    except Exception as e:
        error = "can't create container: " + str(e)
        logging.error(error)
        log += error
        return True, log, False

    try:
        client.start(container, binds={input: {'bind': '/input', 'ro': True},
                                       output: {'bind': '/output'}})
    except Exception as e:
        error = "can't start container: " + str(e)
        logging.error(error)
        log += error
        return True, log, False

    status = client.wait(container)
    if status:
        logger.error('simulation crashed')
        log += client.logs(container).decode()
        return status, log, container

    logger.info('simulate finished')
    return status, log, container

