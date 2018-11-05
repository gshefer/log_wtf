import random

from analyzer import analyze
from tools import imap_task
from log.logger import init_logger


def main():
    logger = init_logger(enabled=True)
    logger.info('hello world')
    elements = xrange(random.randint(10000, 30001))
    results = imap_task(analyze, elements)
    for r in results:
        logger.debug('got from subprocess %d', r)
    logger.info('bye bye')
    logger.queue_listener.stop()


if __name__ == '__main__':
    main()
