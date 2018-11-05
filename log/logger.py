import logging
import multiprocessing
from multiprocessing import queues

from log.consts import (MAIN_PROCESS_NAME, CONSOLE_LEVEL, CONSOLE_FMT, CONSOLE_DATE_FMT,
                        LOGGER_NAME, LOGGER_LEVEL)
from log.filters.level_filter import LevelFilter
from log.handlers.queue_handler import QueueHandler, QueueListener


def _gen_console_handler(fmt, datefmt, level):
    # Sometimes code gets stuck:
    stream_handler = logging.StreamHandler()

    # Never failed:
    # stream_handler = logging.FileHandler('app_log.txt', mode='w')

    console_formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    stream_handler.setFormatter(console_formatter)
    stream_handler.setLevel(level)
    stream_handler.addFilter(LevelFilter(level))
    return stream_handler


def _create_logger_main_process():
    logging.captureWarnings(True)

    logger_instance = logging.getLogger(LOGGER_NAME)
    logger_instance.setLevel(LOGGER_LEVEL)

    console_handler = _gen_console_handler(fmt=CONSOLE_FMT, datefmt=CONSOLE_DATE_FMT,
                                           level=CONSOLE_LEVEL)

    logger_instance.queue = multiprocessing.Queue()
    logging.root.addHandler(QueueHandler(queue=logger_instance.queue))

    logger_instance.queue_listener = QueueListener(logger_instance.queue, console_handler)
    logger_instance.queue_listener.start()

    return logger_instance


def _create_logger_sub_process(queue):
    if not isinstance(queue, queues.Queue):
        raise ValueError('queue must be a {0} instance. got: {1}'.format(queues.Queue.__name__, type(queue).__name__))

    logging.captureWarnings(True)
    logger_instance = logging.getLogger(LOGGER_NAME)
    logger_instance.setLevel(LOGGER_LEVEL)
    logging.root.addHandler(QueueHandler(queue=queue))

    return logger_instance


def _create_disabled_logger():
    logger_instance = logging.getLogger(LOGGER_NAME)
    logger_instance.addHandler(logging.NullHandler())

    return logger_instance


def init_logger(enabled, *args, **kwargs):
    if not enabled:
        logger_instance = logging.getLogger(LOGGER_NAME)
        logger_instance.setLevel(LOGGER_LEVEL)
        return logger_instance

    if multiprocessing.current_process().name == MAIN_PROCESS_NAME:
        return _create_logger_main_process()

    return _create_logger_sub_process(*args, **kwargs)


# Define a global variable for the logger, still, anytime we can get it via logging.getLogger
logger = _create_disabled_logger()
