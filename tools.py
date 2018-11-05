import logging
import multiprocessing


from contextlib2 import closing

from log.consts import LOGGER_NAME
from log.logger import init_logger, logger


def imap_task(task, data):
    logger.debug('spawning processes...')
    with closing(multiprocessing.Pool(initializer=init_logger,
                                      initargs=(True, logging.getLogger(LOGGER_NAME).queue,))) as pool:

        results = pool.imap_unordered(task, data)
    pool.join()
    logger.debug('fetching results...')

    for result in results:
        if isinstance(result, Exception):
            logger.critical('sub process got an error', exc_info=result)
            raise result
        yield result
    logger.debug('done multiprocess...')
